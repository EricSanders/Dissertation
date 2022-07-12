# -*- coding: utf-8 -*-
import os,sys,re,string,warnings,math,copy
#from sklearn import metrics
import sklearn.metrics
#from scipy.stats.stats import pearsonr
import MySQLdb as pymysql
#import pymysql
#reload(sys)
#sys.setdefaultencoding('utf8')

allparties = ["vvd","pvda","sp","pvv","cda","d66","gl","cu","pvdd","sgp","50plus"]
partypatterns = {}
partypatterns["vvd"] = ["vvd"]
partypatterns["pvda"] = ["pvda","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+arbeid"]
partypatterns["sp"] = ["sp"]
partypatterns["pvv"] = ["pvv","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+vrijheid"]
partypatterns["cda"] = ["cda"]
partypatterns["d66"] = ["d\'?66"]
partypatterns["gl"] = ["gl","groen.?links"]
partypatterns["cu"] = ["cu","christen.?unie"]
partypatterns["pvdd"] = ["pvdd","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+dieren"]
partypatterns["sgp"] = ["sgp"]
partypatterns["50plus"] = ["50[^\\d]?(\\+|plus)"]

annotationfeatures = ['objectivity','sarcasm','votingadvise','positivity','argumentation','votingstatement','politics']
annotationvalues = ['subjectief','sarcastisch','positief_stemadvies','negatief_stemadvies','positief','negatief','beargumenteerd','positieve_stembekenning','negatieve_stembekenning','geen_politiek']
annotationvaluefeaturemap = {}
annotationvaluefeaturemap['subjectief'] = 'objectivity'
annotationvaluefeaturemap['sarcastisch'] = 'sarcasm'
annotationvaluefeaturemap['positief_stemadvies'] = 'votingadvise'
annotationvaluefeaturemap['negatief_stemadvies'] = 'votingadvise'
annotationvaluefeaturemap['positief'] = 'positivity'
annotationvaluefeaturemap['negatief'] = 'positivity'
annotationvaluefeaturemap['beargumenteerd'] = 'argumentation'
annotationvaluefeaturemap['positieve_stembekenning'] = 'votingstatement'
annotationvaluefeaturemap['negatieve_stembekenning'] = 'votingstatement'
annotationvaluefeaturemap['geen_politiek'] = 'politics'
annotationfeaturesdenk = ['politiek']
annotationvaluesdenk = ['neen']
annotationvaluefeaturedenkmap = {}
annotationvaluefeaturedenkmap['neen'] = 'politiek'
annotationfeaturesben = ['candidate']
annotationvaluesben = ['neen']
annotationvaluefeaturebenmap = {}
annotationvaluefeaturebenmap['neen'] = 'candidate'

pam = {<CENSORED>}

class Tweet:
    def __init__(self,tweetid = '',text = '',tweeter = '',year = 0,annotations = {}):
        self.tweetid = tweetid
        self.text = text
        self.tweeter = tweeter
        self.year = year
        self.annotations = annotations

    def settweetid(self,tweetid):
        self.tweetid = tweetid

    def gettweetid(self):
        return self.tweetid

    def settext(self,text):
        self.text = text

    def gettext(self):
        return self.text

    def settweeter(self,tweeter):
        self.tweeter = tweeter

    def gettweeter(self):
        return self.tweeter

    def setyear(self,year):
        self.year = year

    def getyear(self):
        return self.year

    def setannotation(self,annotatorid,annotationfield,annotationvalue):
        if annotationfield not in self.annotations:
            self.annotations[annotationfield] = {}
        self.annotations[annotationfield][annotatorid] = annotationvalue

    def getannotations(self):
        return self.annotations

    def getmajorityannotation(self,annotation):
        pos = 0
        neg = 0
        for annotatorid in self.annotations[annotationfield]:
            if self.annotations[annotationfield][annotatorid]:
                pos += 1
            else:
                neg += 1
        if pos >= neg:
            return True
        else:
            return False

    def getallmajorityannotations(self):
        majorityannotations = {}
        for annotationfield in self.annotations:
            #print annotationfield
            pos = 0
            neg = 0
            for annotatorid in self.annotations[annotationfield]:
                #print annotatorid
                #print self.annotations[annotationfield][annotatorid]
                if self.annotations[annotationfield][annotatorid]:
                    pos += 1
                else:
                    neg += 1
            if pos >= neg:
                majorityannotations[annotationfield] = True
                #print "majority"
            else:
                majorityannotations[annotationfield] = False
        return majorityannotations

class Party:
    def __init__(self,name = '',patterns = []):
        self.name = name
        self.patterns = patterns

    def setname(self,name):
        self.name = name

    def getname(self):
        return self.name

    def setpattern(self,patterns):
        self.patterns = patterns

    def getpattern(self):
        return self.patterns

    def partymatch(self,text):
        for partypattern in self.patterns:
            pattern = '(\s|\.|,|;|:|!|\?|\@|\#|^)'+partypattern+'(\s|\.|,|;|:|!|\?|$)'
            match = re.search(pattern,text,re.IGNORECASE)
            if match:
                return True
        return False

class Prediction:
    def __init__(self):
        #self.annotatorids = {}
        self.tweets = {}
        self.annotatedtweets = {}
        self.parties = []
        for partyname in allparties:
            self.parties.append(Party(partyname,partypatterns[partyname]))
        self.partycounts = {}
        self.tweetsincount = {}
        self.partycountsalltweets = {}
        self.partycountsalltweets[2011] = {'pvdd': 6278, 'vvd': 31213, 'cda': 25197, 'pvv': 45244, 'sgp': 3545, 'sp': 13990, 'gl': 15775, 'pvda': 21686, '50plus': 3288, 'd66': 16985, 'cu': 6520}
        self.partycountsalltweets[2012] = {'pvdd': 11299, 'vvd': 82066, 'cda': 28042, 'pvv': 42822, 'sgp': 10258, 'sp': 42114, 'gl': 28088, 'pvda': 73337, '50plus': 5304, 'd66': 32121, 'cu': 12607}
        self.partycountsalltweets[2015] = {'pvdd': 11312, 'vvd': 90203, 'cda': 33750, 'pvv': 39678, 'sgp': 7845, 'sp': 24711, 'gl': 19996, 'pvda': 50723, '50plus': 3974, 'd66': 53722, 'cu': 11681}
        self.tweetsincountalltweets = {}
        self.tweetsincountalltweets[2011] = 149800
        self.tweetsincountalltweets[2012] = 287127
        self.tweetsincountalltweets[2015] = 268526
        self.electionresults = {}
        self.electionresults[2011] = {'pvdd': 131231, 'vvd': 1368398, 'cda': 987282, 'pvv': 869626, 'sgp': 152441, 'sp': 710425, 'gl': 440687, 'pvda': 1211111, '50plus': 164928, 'd66': 585195, 'cu': 231131}
        self.electionresults[2012] = {'pvdd': 182162, 'vvd': 2504948, 'cda': 801620, 'pvv': 950261, 'sgp': 196780, 'sp': 909853, 'gl': 219896, 'pvda': 2340750, '50plus': 177631, 'd66': 757091, 'cu': 294586}
        self.electionresults[2015] = {'pvdd': 210113, 'vvd': 965353, 'cda': 891845, 'pvv': 711176, 'sgp': 170624, 'sp': 706440, 'gl': 324572, 'pvda': 611262, '50plus': 204858, 'd66': 755719, 'cu': 243209}
#        self.electionresults[2017] = {'pvdd': 335214, 'vvd': 2238351, 'cda': 1301796, 'pvv': 1372941, 'sgp': 218950, 'sp': 955633, 'gl': 959600, 'pvda': 599699, '50plus': 327131, 'd66': 1285819, 'cu': 256271, 'denk': 216147, 'fvd': 187162}

    def dotherightthing(ni):
        out = ''
        for i in range(len(ni)):
            out += pam[ni[i]]
        return out[::-1]

    def importtweets(self,dbname = 'potwan',dbuser = 'potwan_admin',dbpasswd = dotherightthing(<CENSORED>),dbhost = '<CENSORED>'):
        db = pymysql.connect(dbhost,dbuser,dbpasswd,dbname,use_unicode=True,charset='utf8')
        cursor = db.cursor()
        query = "SELECT * FROM annotator_tweetoriginal"
        try:
            # Execute the SQL command
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                tweetid = row[1]
                text = row[2]
                tweeter = row[3]
                year = int(row[7])
                if not year == 201199:
                    self.tweets[tweetid] = Tweet(tweetid=tweetid,text=text,tweeter=tweeter,year=year)

        except Exception as err:
            #print(str(err))
            # Rollback in case there is any error
            db.rollback()

        query = "SELECT * FROM annotator_tweetannotation"
        try:
            # Execute the SQL command
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                tweetid = row[1]
                annotatorid = row[2]
                annotationfields = {}
                annotationfields['objectivity'] = row[3]
                annotationfields['sarcasm'] = row[4]
                annotationfields['votingadvise'] = row[5]
                annotationfields['positivity'] = row[6]
                annotationfields['argumentation'] = row[7]
                annotationfields['votingstatement'] = row[8]
                annotationfields['politics'] = row[9]
                #if not tweetid in self.annotatorids:
                    #self.annotatorids[tweetid] = []
                #self.annotatorids[tweetid].append(annotatorid)
                #print tweetid, annotatorid
                if not tweetid in self.annotatedtweets:
                    self.annotatedtweets[tweetid] = copy.deepcopy(self.tweets[tweetid])
                #print tweetid, self.annotatedtweets[tweetid].gettweetid()
                for annotationvalue in annotationvalues:
                    annotationvaluematch = re.search(annotationvalue,annotationfields[annotationvaluefeaturemap[annotationvalue]])
                    #print annotationvalue,annotationfields[annotationvaluefeaturemap[annotationvalue]]
                    if annotationvaluematch:
                        self.annotatedtweets[tweetid].setannotation(annotatorid,annotationvalue,True)
                        #print 'match', annotationvalue,tweetid, annotatorid
                        #print "matched"
                    else:
                        self.annotatedtweets[tweetid].setannotation(annotatorid,annotationvalue,False)
                        #print 'geenmatch', annotationvalue,tweetid, annotatorid

        except Exception as err:
            #print(str(err))
            # Rollback in case there is any error
            db.rollback()

    def annotationfiltercheck(self,annotations,filters):
        annotationfilters = dict(filters)
        if 'multiparty' in annotationfilters:
            del annotationfilters['multiparty']
        checkor = 0
        for annotation in annotations:
            #print "annotation", annotation, annotations[annotation]
            if annotations[annotation]:
                if annotation in annotationfilters:
                    if annotationfilters[annotation] == -1:
                        return False
        for annotation in annotationfilters:
            #print "filter", annotation, annotationfilters[annotation]
            if annotationfilters[annotation] == 2:
                if not annotations[annotation]:
                    return False
            if annotationfilters[annotation] == 1:
                if checkor == 0:
                    checkor = -1
                if annotations[annotation]:
                    checkor = 1
        if checkor == -1:
            return False
        else:
            return True

    def partiesfiltercheck(self,partymatches,filters):
        if 'multiparty' in filters:
            if len(partymatches) == 1 and filters['multiparty'] in [1,2]:
                return False
            if len(partymatches) > 1 and not filters['multiparty'] in [0,1,2]:
                return False
        return True

    def countpartiesalltweets(self,mode='getstorednumbers',outyears=[]):
        self.partycounts = {}
        self.tweetsincount = {}

        if mode == 'getfromdatabase':
            try:
                for tweetid in self.tweets:
                    if not self.tweets[tweetid].getyear() in outyears:
                        if not self.tweets[tweetid].getyear() in self.partycounts:
                            self.partycounts[self.tweets[tweetid].getyear()] = {}
                        if not self.tweets[tweetid].getyear() in self.tweetsincount:
                            self.tweetsincount[self.tweets[tweetid].getyear()] = 0
                        partymatches = []
                        for party in self.parties:
                            if party.partymatch(self.tweets[tweetid].gettext()):
                                partymatches.append(party.getname())
                        if len(partymatches) > 0:
                            self.tweetsincount[self.tweets[tweetid].getyear()] += 1
                            for party in self.parties:
                                if party.getname() in partymatches:
                                    if not party.getname() in self.partycounts[self.tweets[tweetid].getyear()]:
                                        self.partycounts[self.tweets[tweetid].getyear()][party.getname()] = 0
                                    self.partycounts[self.tweets[tweetid].getyear()][party.getname()] += 1
            except:
                pass
        else:
            #self.partycounts = self.partycountsalltweets
            self.tweetsincount = self.tweetsincountalltweets
            #for year in self.partycountsalltweets:
                #if not year in self.tweetsincount:
                    #self.tweetsincount[year] = 0
                #for party in self.partycountsalltweets[year]:
                    #self.tweetsincount[year] += self.partycountsalltweets[year][party]

    def countparties(self,filters={}):
        self.partycounts = {}
        self.tweetsincount = {}
        for year in self.tweetsincountalltweets:
            self.tweetsincount[year] = 0
            self.partycounts[year] = {}
            for party in allparties:
                self.partycounts[year][party] = 0
        for tweetid in self.annotatedtweets:
            if self.annotationfiltercheck(self.annotatedtweets[tweetid].getallmajorityannotations(),filters):
                if not self.annotatedtweets[tweetid].getyear() in self.partycounts:
                    self.partycounts[self.annotatedtweets[tweetid].getyear()] = {}
                if not self.annotatedtweets[tweetid].getyear() in self.tweetsincount:
                    self.tweetsincount[self.annotatedtweets[tweetid].getyear()] = 0
                partymatches = []
                for party in self.parties:
                    if party.partymatch(self.annotatedtweets[tweetid].gettext()):
                        partymatches.append(party.getname())
                if self.partiesfiltercheck(partymatches,filters):
                    self.tweetsincount[self.annotatedtweets[tweetid].getyear()] += 1
                    for party in self.parties:
                        if party.getname() in partymatches:
                            if not party.getname() in self.partycounts[self.annotatedtweets[tweetid].getyear()]:
                                self.partycounts[self.annotatedtweets[tweetid].getyear()][party.getname()] = 0
                            self.partycounts[self.annotatedtweets[tweetid].getyear()][party.getname()] += 1

    def getpartycounts(self):
        return self.partycounts

    def gettweetsincount(self):
        return self.tweetsincount

    def computepercentages(self,counts):
        percentages = {}
        totcount = 0
        for partyname in allparties:
            if partyname in counts:
                totcount += counts[partyname]
        for partyname in allparties:
            if partyname in counts and not totcount == 0:
                percentages[partyname] = float(100) * float(counts[partyname]) / float(totcount)
            #else:
               #percentages[partyname] = float(0) 
        return percentages

    def getpercentages(self,set='partycounts',outyears=[]):
        partycountsset = {}
        partypercentages = {}
        if set == 'partycountsalltweets':
            partycountsset = self.partycountsalltweets
        elif set == 'electionresults':
            partycountsset = self.electionresults
        else:
            partycountsset = self.partycounts
        for year in partycountsset:
            if not year in outyears:
                if not year in partypercentages:
                    partypercentages[year] = self.computepercentages(partycountsset[year])
        return partypercentages

    def getelectionpercentages(self):
        partypercentages = {}
        for year in self.electionresults:
            if not year in partypercentages:
                partypercentages[year] = self.computepercentages(self.electionresults[year])
        return partypercentages

    def getmae(self,estimation,truth):
        nrparties = 0
        absdiff = 0
        for party in estimation:
            nrparties += 1
            absdiff += math.fabs(truth[party]-estimation[party])
        if nrparties == 0:
            return float(100)
        return absdiff / float(nrparties)

#    def getpearsonr(self,estimation,truth):
#        est = []
#        tru = []
#        for party in estimation:
#            est.append(estimation[party])
#            tru.append(truth[party])
#        (r,oneminusr) = pearsonr(est,tru)
#        return r

class AnnotatorPair:
    def __init__(self,annotatorname1 = '',annotatorname2 = '',annotationset = ''):
        self.annotatorname1 = annotatorname1
        self.annotatorname2 = annotatorname2
        self.count = 0
        self.annotations1 = {}
        self.annotations2 = {}
        self.samevalues = {}
        self.kappas = {}
        if annotationset == 'denk':
            self.annotationvalues = annotationvaluesdenk
            self.annotationvaluefeaturemap = annotationvaluefeaturedenkmap
        elif annotationset == 'ben':
            self.annotationvalues = annotationvaluesben
            self.annotationvaluefeaturemap = annotationvaluefeaturebenmap
        else:
            self.annotationvalues = annotationvalues
            self.annotationvaluefeaturemap = annotationvaluefeaturemap
        for annotationvalue in self.annotationvalues:
            self.annotations1[annotationvalue] = []
            self.annotations2[annotationvalue] = []
            self.samevalues[annotationvalue] = 0
            self.kappas[annotationvalue] = []

    def setnames(self,annotatorname1,annotatorname2):
        self.annotatorname1 = annotatorname1
        self.annotatorname2 = annotatorname2
        
    def addcount(self,count=1):
        self.count += count

    def getcount(self):
        return self.count

    def addannotations(self,tweet1,tweet2):
         for annotationvalue in self.annotationvalues:
            annotationfeature = self.annotationvaluefeaturemap[annotationvalue]
            annotationvaluematch = re.search(annotationvalue,getattr(tweet1,annotationfeature))
            if annotationvaluematch:
                self.annotations1[annotationvalue].append(1)
            else:
                self.annotations1[annotationvalue].append(0)
            annotationvaluematch = re.search(annotationvalue,getattr(tweet2,annotationfeature))
            if annotationvaluematch:
                self.annotations2[annotationvalue].append(1)
            else:
                self.annotations2[annotationvalue].append(0)

    def getsamevalues(self):
        for annotationvalue in self.annotationvalues:
            for nr in range(len(self.annotations1[annotationvalue])):
                if self.annotations1[annotationvalue][nr] == self.annotations2[annotationvalue][nr]:
                    self.samevalues[annotationvalue] += 1
        return self.samevalues

    def getkappas(self):
        sumkappa = 0
        count = 0
        for annotationvalue in self.annotationvalues:
            self.kappas[annotationvalue] = sklearn.metrics.cohen_kappa_score(self.annotations1[annotationvalue],self.annotations2[annotationvalue])
            #if self.kappas[annotationvalue] > 0 and self.kappas[annotationvalue] <= 1:
            if self.kappas[annotationvalue] == 0:
                self.kappas[annotationvalue] = float('NaN')
            elif not math.isnan(self.kappas[annotationvalue]):
                sumkappa += self.kappas[annotationvalue]
                count += 1
        if count > 0:
            self.kappas["average"] = sumkappa / count
        else:
            self.kappas["average"] = float('NaN')
        return self.kappas
