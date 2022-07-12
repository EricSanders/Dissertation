import subprocess
import datetime
import json
import csv
import pymysql
import re
import random
from collections import OrderedDict

def computescores(tp,fp,fn,tn):
    precision = float('NaN')
    if tp + fp > 0:
        precision = tp / (tp + fp)
    recall = float('NaN')
    if tp + fn > 0:
        recall = tp / (tp + fn)
    f1 = float('NaN')
    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    return (precision,recall,f1)

def computeproportionalamounts(total1nr,total2nr,transcribed1nr,transcribed2nr):

        transcribed1correctednr = 0
        transcribed2correctednr = 0
        if total1nr >= total2nr:
            if total1nr > 0:
                transcribed2correctednr = int(transcribed1nr * (total2nr / total1nr))
                if transcribed2correctednr > transcribed2nr:
                    transcribed2correctednr = transcribed2nr
                    transcribed1correctednr = int(transcribed2nr * (total1nr / total2nr))
                else:
                    transcribed1correctednr = transcribed1nr
        else:
            if total2nr > 0:
                transcribed1correctednr = int(transcribed2nr * (total1nr / total2nr))
                if transcribed1correctednr > transcribed1nr:
                    transcribed1correctednr = transcribed1nr
                    transcribed2correctednr = int(transcribed1nr * (total2nr / total1nr))
                else:
                    transcribed2correctednr = transcribed2nr

        return(transcribed1correctednr,transcribed2correctednr)

class Tweet:
    def __init__(self, tweetid = '', tweetdatetime= '', retweettotweetid = '', replytotweetid = '', replytotweeter = '', text = '', tweeterid = '', tweetername = '', tweeter = '', tweeterlocation = '', urls = []):

        self.variables = {}
        self.variables['tweetid'] = tweetid
        self.variables['tweetdatetime'] = tweetdatetime
        if tweetdatetime:
            self.variables['tweetdate'] = tweetdatetime.date()
            self.variables['tweettime'] = tweetdatetime.time()
            self.variables['tweethour'] = tweetdatetime.hour
        self.variables['retweettotweetid'] = retweettotweetid
        self.variables['replytotweetid'] = replytotweetid
        self.variables['replytotweeter'] = replytotweeter
        self.variables['text'] = re.sub('[\r\n]+','<NL>',text)
        self.variables['tweeterid'] = tweeterid
        self.variables['tweetername'] = tweetername
        self.variables['tweeter'] = tweeter
        self.variables['tweeterlocation'] = tweeterlocation
        self.urls = urls
        self.matches = {}
        self.annotations = {}
        self.annotatorids = []
        
    def set(self,key,value):
        if key == 'tweetdatetime':
            tweetdatetime = datetime.datetime.strptime(value,"%a %b %d %H:%M:%S %z %Y")
            self.variables['tweetdatetime'] = tweetdatetime
            self.variables['tweetdate'] = tweetdatetime.date()
            self.variables['tweethour'] = tweetdatetime.hour
        else:
            self.variables[key] = value

    def get(self,key):
        if key in self.variables:
            return self.variables[key]
        else:
            return 'NULL'

    def gettokens(self,token,prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)',postpattern='(\s|\.|,|;|:|!|\?|$)',ignorecase=True,applyprepostpattern=True):
        matchpattern = token
        if applyprepostpattern:
            matchpattern = prepattern+'('+token+')'+postpattern
        if ignorecase:
            matches = re.findall('('+matchpattern+')',self.variables['text'],re.IGNORECASE)
        else:
            matches = re.findall('('+matchpattern+')',self.variables['text'])
        if matches:
            return matches
        else:
            return []
                    
    def patternmatch(self,patterns,errorpatterns,prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)',postpattern='(\s|\.|,|;|:|!|\?|$)',ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=False):
        matched = False
        nrmatchedkeys = 0
        for key in patterns:
            nrpatternmatches = 0
            nrerrorpatternmatches = 0
            for pattern in patterns[key]:
                matchpattern = pattern
                if applyprepostpattern:
                    matchpattern = prepattern+'('+pattern+')'+postpattern
                if ignorecase:
                    matches = re.findall('('+matchpattern+')',self.variables['text'],re.IGNORECASE)
                else:
                    matches = re.findall('('+matchpattern+')',self.variables['text'])
                if matches:
                    nrpatternmatches += len(matches)
                    self.addmatch(key,pattern)

            if key in errorpatterns:
                for errorpattern in errorpatterns[key]:
                    matcherrorpattern = errorpattern
                    if errorapplyprepostpattern:
                        matcherrorpattern = prepattern+'('+errorpattern+')'+postpattern
                    if ignorecase:
                        errormatches = re.findall('('+matcherrorpattern+')',self.variables['text'],re.IGNORECASE)
                    else:
                        errormatches = re.findall('('+matcherrorpattern+')',self.variables['text'])
                    if errormatches:
                        nrerrorpatternmatches += len(errormatches)

            #if nrpatternmatches > nrerrorpatternmatches:
            if nrpatternmatches > 0  and not nrerrorpatternmatches > 0:
                matched = True
                nrmatchedkeys += 1
                #for match in matches:
                    #self.addmatch(key,match[2])

        #return matched
        #self.getmatches()
        return nrmatchedkeys

    def geturls(self):
        return self.urls
    
    def addmatch(self,key,pattern):
        if key not in self.matches:
            self.matches[key] = []
        self.matches[key].append(pattern)

    def getmatches(self):
        return self.matches
        #for key in self.matches:
            #print(key)
            #for pattern in self.matches[key]:
                #print('  ' + str(pattern))

    def getparties(self):
        return self.getmatches().keys()       

    def removeparty(self,party):
        if party in self.matches:
            del(self.matches[party])
     
    def setannotation(self,annotatorid,annotationfield,annotationvalue):
        if annotationfield not in self.annotations:
            self.annotations[annotationfield] = {}
        self.annotations[annotationfield][annotatorid] = annotationvalue
        if not annotatorid in self.annotatorids:
            self.annotatorids.append(annotatorid)

    def getannotations(self):
        return self.annotations

    def getannotationvalue(self,annotationlabel,decidingannotatorid=''):
        returnvalue = ''
        if annotationlabel in self.annotations:
            currentvalues = []
            for annotatorid in self.annotations[annotationlabel]:
                value = self.annotations[annotationlabel][annotatorid]
                currentvalues.append(value)
                if decidingannotatorid == annotatorid:
                    returnvalue = value
            if not decidingannotatorid:
                returnvalue = max(set(currentvalues),key=currentvalues.count)
        else:
            print("annotationlabel "+annotationlabel+" does not exist")    
        return returnvalue

class TweetCorpus:
    def __init__(self):

        pass

    def gettweets(self):
        tweets = []
        for tweetid in self.tweets:
            tweets.append(self.tweets[tweetid])
        return tweets

    def gettweetdates(self):
        tweetdates = []
        for tweetid in self.tweets:
            tweetdate = self.tweets[tweetid].get('tweetdate')
            if not tweetdate in tweetdates and not tweetdate == 'NULL':
                tweetdates.append(tweetdate)
        return tweetdates

    def gettweethours(self):
        tweethours = []
        for tweetid in self.tweets:
            tweethour = self.tweets[tweetid].get('tweethour')
            if not tweethour in tweethours and not tweethour == 'NULL':
                tweethours.append(tweethour)
        return tweethours

    def getuserlocations(self):
        userlocations = {}
        for tweetid in self.tweets:
            userlocation = self.tweets[tweetid].variables['tweeterlocation']
            if not userlocation in userlocations:
                userlocations[userlocation] = 0
            userlocations[userlocation] += 1

        return userlocations

    def removetweet(self,tweet):
        tweetid = tweet.get('tweetid')
        del(self.tweets[tweetid])
    
    def filteronpatterns(self,patterns,errorpatterns={},prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)',postpattern='(\s|\.|,|;|:|!|\?|$)',ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=False,removemismatch=True):
        nonmatchingtweetids = []
        for tweetid in self.tweets:
            if not self.tweets[tweetid].patternmatch(patterns,errorpatterns,prepattern,postpattern,applyprepostpattern,errorapplyprepostpattern,ignorecase):
                nonmatchingtweetids.append(tweetid)
            #else:
                #self.tweets[tweetid].getmatches()
        if removemismatch:
            for tweetid in nonmatchingtweetids:
                del self.tweets[tweetid]

        #for tweetid in self.tweets:
            #self.tweets[tweetid].getmatches()
            
        #print(len(self.tweets))
    
    def writecsvfile(self,csvfilename):
        csvfile = open(csvfilename,'w')
        csvwriter = csv.writer(csvfile,delimiter=";")
        for tweetid in self.tweets:
            tweet = self.tweets[tweetid]
            text = tweet.get('text')
            tweeter = tweet.get('tweeter')
            tweetdatetime = tweet.get('tweetdatetime')
            replytotweetid = tweet.get('replytotweetid')
            retweettotweetid = tweet.get('retweettotweetid')
            urls = '__'.join(tweet.geturls())
            parties = '__'.join(tweet.getparties())
            csvwriter.writerow([tweetid,text,tweeter,tweetdatetime,replytotweetid,retweettotweetid,urls,parties])
        #text = re.sub('\n','<NL>',pymysql.escape_string(jsondict['text']))
        #pass
        
class TweetCorpusNonAnnotated(TweetCorpus):
    def __init__(self):
       #self.tweets = OrderDict()
       self.tweets = {}

    def clear(self):
       self.tweets = {}

    def readcsvfile(self,csvfilename):
        csvfile = open(csvfilename)
        csvreader = csv.reader(csvfile,delimiter=";")
        for row in csvreader:
            tweetid = row[0]
            text = row[1]
            tweeter = row[2]
            tweetdatetime = datetime.datetime.strptime(row[3].replace('+00:00','+0000'),"%Y-%m-%d %H:%M:%S%z")
            replytotweetid = row[4]
            retweettotweetid = row[5]
            urls = row[6].split('__')
            parties = row[7].split('__')
            tweet = Tweet(tweetid = tweetid, tweetdatetime = tweetdatetime, retweettotweetid = retweettotweetid, replytotweetid = replytotweetid, replytotweeter = '', text = text, tweeterid = '', tweetername = '', tweeter = tweeter, tweeterlocation = '', urls = urls)
            for party in parties:
                tweet.addmatch(party,'???')
                #print(party)
            self.tweets[tweetid] = tweet

            
    def readjsonfile(self,jsonfilename):
        correcttweetnr = 0
        errortweetnr = 0
        doubletweetnr = 0
        linenr = 0
        jsonfile = open(jsonfilename)
        for jsonline in jsonfile:
            urls = []
            linenr += 1
            try:
            #if 1 == 1:
                jsondict = json.loads(jsonline)
                text = pymysql.escape_string(jsondict['text'])
                tweetid = jsondict['id_str']
                datetimestring = jsondict['created_at']
                tweetdatetime = datetime.datetime.strptime(datetimestring,"%a %b %d %H:%M:%S %z %Y")
                tweeterid = jsondict['user']['id_str']
                tweetername = jsondict['user']['name']
                tweeter = jsondict['user']['screen_name']
                if tweetid in self.tweets:
                    #print(tweetid + " already seen")
                    if self.tweets[tweetid].variables['tweeter'] != tweeter:
                        print("tweetid same, but tweeter differs!")
                    doubletweetnr += 1
                tweeterlocation = jsondict['user']['location']
                try:
                    retweettotweetid = jsondict['retweeted_status']['id_str']
                except:
                    retweettotweetid = 'NULL'
                try:
                    replytotweetid = re.sub('None','NULL',jsondict['in_reply_to_status_id_str'])
                except:
                    replytotweetid = 'NULL'
                try:
                    replytotweeter = re.sub('None','NULL',jsondict['in_reply_to_screen_name'])
                except:
                    replytotweeter = 'NULL'
                try:
                    entitiesurls = jsondict['entities']['urls']
                    if entitiesurls:
                        for entry in entitiesurls:
                            url = entry['url']
                            urls.append(url)
                except:
                    urls = []

                tweet = Tweet(tweetid = tweetid, tweetdatetime = tweetdatetime, retweettotweetid = retweettotweetid, replytotweetid = replytotweetid, replytotweeter = replytotweeter, text = text, tweeterid = tweeterid, tweetername = tweetername, tweeter = tweeter, tweeterlocation = tweeterlocation, urls = urls)
                self.tweets[tweetid] = tweet
                correcttweetnr += 1
            except:
            #else:
                errortweetnr += 1
                #print(jsonfilename,linenr)

        return correcttweetnr, errortweetnr, doubletweetnr
                
    def readgzfiles(self,firstdatehour,lastdatehour,pathname='/vol/bigdata2/datasets2/twitter'):

        startdatehour = datetime.datetime.strptime(firstdatehour,"%Y%m%d%H") # starting time
        enddatehour = datetime.datetime.strptime(lastdatehour,"%Y%m%d%H") # ending time
        datehour = startdatehour

        while datehour <= enddatehour:
            jsonfilename = "tweets_" + datehour.strftime("%Y%m%d%H")
            storedzipfilename = pathname + "/" + datehour.strftime("%Y%m%d%H")[:6] + "/" + datehour.strftime("%Y%m%d%H")[:8] + "-" + datehour.strftime("%Y%m%d%H")[-2:] + ".out.gz"
            zipfilename = jsonfilename + ".gz"

            command = "cp"
            #print command,storedzipfilename,zipfilename
            subprocess.call([command,storedzipfilename,zipfilename])

            command = "gunzip"
            argument = "-f"
            #print command,argument,zipfilename
            subprocess.call([command,argument,zipfilename])

            #print(jsonfilename)
            try:
                correcttweetnr, errortweetnr, doubletweetnr = self.readjsonfile(jsonfilename)
                #print(len(self.tweets))
                print(datehour,correcttweetnr, errortweetnr, doubletweetnr)
            except:
                print(datehour,"Could not read json file")
                
            command = "rm"
            #print command,jsonfilename
            subprocess.call([command,jsonfilename])

            datehour = datehour + datetime.timedelta(hours=1)


            
class TweetCorpusAnnotated(TweetCorpus):
    def __init__(self):
        self.tweets = OrderedDict()
        #self.tweets = {}
        self.trainset = []
        self.devtestset = []
        self.testset = []

    def clear(self):
        self.tweets = OrderedDict()
        #self.tweets = {}
        self.trainset = []
        self.devtestset = []
        self.testset = []

    def __add__(self,other):
        newcorpus = TweetCorpusAnnotated()
        newcorpus.tweets.update(self.tweets)
        newcorpus.tweets.update(other.tweets)
        return newcorpus

    def readmysql(self,db,keylabel,annotationkeylabel='',aliases={}):
        labelnames = {}
        values = {}

        try:
            tweetdb = pymysql.connect(host=db['host'], user=db['user'], passwd=db['passwd'],db=db['dbname'])
        except:
            raise ValueError("Error in opening dbase")
        try:
            cur = tweetdb.cursor()
            cur.execute("SELECT * FROM "+db['tablename'])
            results = cur.fetchall()
            columnnr = 0
            for desc in cur.description:
                labelnames[columnnr] = desc[0]
                columnnr += 1
            for row in results:
                for columnnr in range(len(labelnames)):
                    values[labelnames[columnnr]] = row[columnnr]
                    if labelnames[columnnr] == keylabel:
                        keylabelvalue = values[labelnames[columnnr]]
                    if labelnames[columnnr] == annotationkeylabel:
                        annotationkeylabelvalue = values[labelnames[columnnr]]
                    if labelnames[columnnr] == 'text':
                        #print(values[labelnames[columnnr]])
                        values[labelnames[columnnr]] = re.sub('[\r\n]+','<NL>',values[labelnames[columnnr]])
                        #print(values[labelnames[columnnr]])
                if keylabel in values:
                    if not keylabelvalue in self.tweets:
                        self.tweets[keylabelvalue] = Tweet()
                    for columnnr in range(len(labelnames)):
                        labelname = labelnames[columnnr]
                        if labelname in aliases:
                            #print(labelname)
                            labelname = aliases[labelname]
                            #print(labelname,labelnames[columnnr])
                        if annotationkeylabel in values:
                            self.tweets[keylabelvalue].setannotation(annotationkeylabelvalue,labelname,values[labelnames[columnnr]])
                        else:
                            self.tweets[keylabelvalue].set(labelname,values[labelnames[columnnr]])                                         

        except:
            raise ValueError("Error in reading dbase")

        try:
            tweetdb.close()
        except:
            pass

    def shuffle(self,seed=1):
        random.seed(seed)
        keys = list(self.tweets)
        random.shuffle(keys)
        for key in keys:
            self.tweets.move_to_end(key)
        
    def annotationsummary(self,requestedannotationfields=[],decidingannotatorid=''):
        annotatorids = {}
        values = {}
        nrannotations = {}
        annotatorcombinations = {}
        for tweetid in self.tweets:
            for annotationfield in self.tweets[tweetid].getannotations():
                if len(requestedannotationfields) > 0 and annotationfield in requestedannotationfields:
                    currentvalues = []
                    currentannotators = []
                    if not annotationfield in values:
                        values[annotationfield] = {}
                    for annotatorid in self.tweets[tweetid].annotations[annotationfield]:
                        currentannotators.append(annotatorid)
                        if not annotatorid in annotatorids:
                            annotatorids[annotatorid] = 0
                        annotatorids[annotatorid] += 1
                        value = self.tweets[tweetid].annotations[annotationfield][annotatorid]
                        #if decidingannotatorid == annotatorid:
                            #if not value in values[annotationfield]:
                                #values[annotationfield][value] = 0
                            #values[annotationfield][value] += 1
                        currentvalues.append(value)
                    currentannotators.sort()
                    annotatorcombination = ",".join(currentannotators)
                    if not annotatorcombination in annotatorcombinations:
                        annotatorcombinations[annotatorcombination] = 0
                    annotatorcombinations[annotatorcombination] += 1
                    nrcurrentannotations = len(currentvalues)
                    if not nrcurrentannotations in nrannotations:
                        nrannotations[nrcurrentannotations] = 0
                    nrannotations[nrcurrentannotations] += 1
                    #if not decidingannotatorid:
                        #mostfrequentvalue = max(set(currentvalues),key=currentvalues.count)
                        #if not mostfrequentvalue in values[annotationfield]:
                            #values[annotationfield][mostfrequentvalue] = 0
                        #values[annotationfield][mostfrequentvalue] += 1

                    annotationvalue = self.tweets[tweetid].getannotationvalue(annotationfield,decidingannotatorid)
                    if not annotationvalue in values[annotationfield]:
                        values[annotationfield][annotationvalue] = 0
                    values[annotationfield][annotationvalue] += 1

        return(annotatorids,annotatorcombinations,nrannotations,values)

    def gettokensets(self,word,decidingannotationfield,decidingannotatorid):
        tokensets = []
        for tweetid in self.tweets:
            for annotationfield in self.tweets[tweetid].getannotations():
                if annotationfield == decidingannotationfield:
                    for annotatorid in self.tweets[tweetid].annotations[annotationfield]:
                        if annotatorid == decidingannotatorid:
                            value = self.tweets[tweetid].annotations[annotationfield][annotatorid]
                            patterns = self.tweets[tweetid].gettokens(word)
                            keeptoken = ''
                            for (bla1,bla2,token,bla3) in patterns:
                                if (any(x.isupper() for x in token)):
                                    keeptoken = token
                                elif not keeptoken:
                                    keeptoken = token
                            tokensets.append((keeptoken,value))
        return tokensets
    
    def removenunannotated(self,decidingannotatorid=''):
        nonannotatedtweetids = []
        for tweetid in self.tweets:
            if len(self.tweets[tweetid].annotations) == 0:
                nonannotatedtweetids.append(tweetid)
            elif decidingannotatorid:
                if not decidingannotatorid in self.tweets[tweetid].annotatorids:
                    nonannotatedtweetids.append(tweetid)
        for tweetid in nonannotatedtweetids:
            del self.tweets[tweetid]

    def select_matchallfilters(self,filters):
        subcorpus = TweetCorpusAnnotated()
        for tweetid in self.tweets:
            select = True
            for (variable,value) in filters:
                if variable in self.tweets[tweetid].variables:
                    if not self.tweets[tweetid].variables[variable] == value:
                        select = False
                else:
                    select = False
            if select:
                subcorpus.tweets[tweetid] = self.tweets[tweetid]
        return subcorpus

    def select_matchanyfilter(self,filters):
        subcorpus = TweetCorpusAnnotated()
        for tweetid in self.tweets:
            select = False
            for (variable,value) in filters:
                if variable in self.tweets[tweetid].variables:
                    if self.tweets[tweetid].variables[variable] == value:
                        select = True
            if select:
                subcorpus.tweets[tweetid] = self.tweets[tweetid]
        return subcorpus

    def part(self,nr):
        subcorpus = TweetCorpusAnnotated()
        counter = 0
        for tweetid in self.tweets:
            if counter < nr:
                subcorpus.tweets[tweetid] = self.tweets[tweetid]
            counter += 1
        return subcorpus
        
    def createtraintestset(self,trainsetsize=0,testsetsize=0,devtestsetsize=0,trainsetperc=90,testsetperc=10,devtestsetperc=0):
        totnrtweets = len(self.tweets)
        if trainsetperc + testsetperc + devtestsetperc > 100:
            print("trainsetperc + testsetperc + devtestsetperc higher than 100")
            exit(1)
        if not trainsetsize:
            trainsetsize = int(totnrtweets*trainsetperc/100)
        if not testsetsize:
            testsetsize = int(totnrtweets*testsetperc/100)
        if not devtestsetsize:
            devtestsize = int(totnrtweets*devtestsetperc/100)
        if trainsetsize + testsetsize + devtestsize > totnrtweets:
            print("trainsetsize + testsetsize + devtestsetsize higher than number of tweets")
            exit(1) 
        tweetids = list(self.tweets.keys())
        random.shuffle(tweetids)
        for tweetid in tweetids:
            if len(self.trainset) < trainsetsize:
                self.trainset.append(tweetid)
            elif len(self.testset) < testsetsize:
                self.testset.append(tweetid)
            else:
                self.devtestset.append(tweetid)
                
    def writetextandlabels(self,annotationlabel='',outputfilename='output',decidingannotatorid='',minimumpercentageperlabel=0):
        textperlabel = {}
        textandlabel = []
        textandlabelselection = []
        notweets = {}
        minnrtweets = 999999999999
        maxnrtweetsperlabel = 9999999999999
        for tweetid in self.tweets:
            text = self.tweets[tweetid].get('text')
            label = annotationlabel+"_"+self.tweets[tweetid].getannotationvalue(annotationlabel,decidingannotatorid)
            #print(text,annotationvalue)
            if not label in textperlabel:
                textperlabel[label] = []
            textperlabel[label].append(text)
            textandlabel.append((text,label))
        for label in textperlabel:
            notweets[label] = 0
            print(label,len(textperlabel[label]))
            if len(textperlabel[label]) < minnrtweets:
                minnrtweets = len(textperlabel[label])
        if minimumpercentageperlabel:
            maxnrtweetsperlabel = int(minnrtweets * 100 / minimumpercentageperlabel / len(textperlabel))
            print(maxnrtweetsperlabel)
                
        outputfiletext = open(outputfilename+'.txt',"w")
        outputfilelabels = open(outputfilename+'.labels',"w")
        #for nr in range(0,maxnrtweetsperlabel):
            #for label in textperlabel:
                #text = textperlabel[label][nr]
        for (text,label) in textandlabel:
            if notweets[label] < maxnrtweetsperlabel:
                textandlabelselection.append((text,label))
                notweets[label] += 1
        random.shuffle(textandlabelselection)
        for (text,label) in textandlabelselection:
            outputfiletext.write(text+"\n")
            outputfilelabels.write(label+"\n")
