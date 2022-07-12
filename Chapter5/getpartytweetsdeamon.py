#!/usr/bin/python
#
# Gets tweets from twiqs once every hour and stores party counts in mysql database
import requests
import datetime
import time
import re
import MySQLdb
import codecs
import os
import subprocess
import string

import json

singlepartybool = True
#singlepartybool = False
if singlepartybool == True:
    twiqsoutputfilename = 'TwiqsOutput_singlepartytweets'
else:
    twiqsoutputfilename = 'TwiqsOutput_multipartytweets'


denkfouten = ('ik\\s+denk','denk\\s+ik','denk\\s+je','denk\\s+jij','denk\\s+na','denk\\s+dat','denk\\s+da','denk\\s+dit','denk\\s+aan','denk\\s+niet','denk\\s+het','denk\\s+dan','denk\\s+mee','denk\\s+eens','denk\\s+alleen','denk\\s+ook','denk\\s+even','denk\\s+ff','denk\\s+hier','denk\\s+daar','denk\\s+er','denk\\s+als','denk\\s+over','denk\\s+maar','aan\\s+denk','denk\\s+bij','denk\\s+weer','denk\\s+wel','denk\\s+te','denk\\s+nog','denk\\s+een','denk\\s+nu')

unixstartdate = datetime.datetime(1970,1,1)

def checktrueparty(tweet):
    trueparty = True
    for denkfout in denkfouten:
        denkfoutmatch = re.search(denkfout,tweet,re.IGNORECASE)
        if denkfoutmatch:
            #print 'Denkfout: ' + denkfout, tweet
            trueparty = False
    
    return trueparty


def gettweets2dbase(datehour,partypatterns,twiqs,db,storeindb=True,singleparty=False):

    if singleparty == True:
        addstring = 'singlepartytweets'
    else:
        addstring = 'multipartytweets'

    dbasetable = 'elections170315_' + addstring

    searchtime = datehour.strftime("%Y%m%d%H") + "-" + (datehour + datetime.timedelta(hours=1)).strftime("%Y%m%d%H")

    #alltweetsf = codecs.open('TwiqsOutput/alltweets'+datehour.strftime("%Y%m%d%H")+'.txt', encoding='utf-8', mode='w+')
    #partytweetsf = codecs.open('TwiqsOutput/partytweets'+datehour.strftime("%Y%m%d%H")+'.txt', encoding='utf-8', mode='w+')
    partymatchesf = codecs.open(twiqsoutputfilename + '/partymatches'+datehour.strftime("%Y%m%d%H")+'.txt', encoding='utf-8', mode='w+')
    
    partycount = {}
    totcount = 0
    linenr = 0
    notok = 0

    try:
        command = "curl"
        address = "https://" + twiqs['username'] + ":" + twiqs['passwd'] + "@" + twiqs['url'] + "?year=" + datehour.strftime("%Y") + "&month=" + datehour.strftime("%m") + "&day=" + datehour.strftime("%d") + "&hour=" + datehour.strftime("%H")
        jsonfilename = "tweets_" + addstring + "_" + datehour.strftime("%Y%m%d%H")
        zipfilename = jsonfilename + ".gz"

        print command,address,zipfilename

        zipfile = open(zipfilename,"w")
        subprocess.call([command,address],stdout=zipfile)
        zipfile.close()

        command = "gunzip"
        argument = "-f"
        #print command,argument,zipfilename
        subprocess.call([command,argument,zipfilename])

        jsonfile = open(jsonfilename)
        for jsonline in jsonfile:
            linenr += 1
            retweettotweetid= 'null'
            jsondict = json.loads(jsonline)
            tweettext = re.sub('\n','<NL>',jsondict['text'])
            tweetid = jsondict['id']
            userid = jsondict['user']['id']
            username = jsondict['user']['name']
            tweettimestamp_ms = int(jsondict['timestamp_ms'])
            tweetdatetime = unixstartdate + datetime.timedelta(0,0,0,tweettimestamp_ms)
            tweetdate = tweetdatetime.strftime("%Y-%m-%d")
            tweettime = tweetdatetime.strftime("%H:%M:%S")
            replytotweetid = jsondict['in_reply_to_user_id_str']
            try:
                retweettotweetid = jsondict['retweeted_status']['id']
            except:
                pass
                #print "no retweet"

            #print userid,tweetid,tweetdate,tweettime,replytotweetid,retweettotweetid,username,tweettext

            try:
                tweetlist = (str(userid),str(tweetid),str(tweetdate),str(tweettime),str(replytotweetid),str(retweettotweetid),username,tweettext)
                #print linenr, "ok"
            except:
                #print linenr, "something wrong with list"
                notok += 1
                #print tweettext
            #tweetlist = ("a","b","c")

            try:
                line = "\t".join(tweetlist)
                #print line
            except:
                print "something wrong with line"

            #alltweetsf.write((line+'\n'))
            parts = line.split('\t')
            try:
                tweetid = parts[1]
                retweet_to_tweet_id = parts[5] # null if none
                username = parts[6]
                tweet = parts[7]
                #print tweetid,retweet_to_tweet_id,username,tweet
                if retweet_to_tweet_id == 'null':
                    thistweetpartycount = 0
                    for party in partypatterns:
                        for partypattern in partypatterns[party]:
                            pattern = '(\s|\.|,|;|:|!|\?|\@|\#|^)'+partypattern+'(\s|\.|,|;|:|!|\?|$)'
                            partymatch = re.search(pattern,tweet,re.IGNORECASE)
                            if partymatch and checktrueparty(tweet):
                                thistweetpartycount += 1

                    if thistweetpartycount == 1 or (thistweetpartycount > 1 and singleparty == False):
                        for party in partypatterns:
                            for partypattern in partypatterns[party]:
                                pattern = '(\s|\.|,|;|:|!|\?|\@|\#|^)'+partypattern+'(\s|\.|,|;|:|!|\?|$)'
                                partymatch = re.search(pattern,tweet,re.IGNORECASE)
                                if partymatch and checktrueparty(tweet):
                                    totcount += 1
                                    #partytweetsf.write((line+'\n'))
                                    partymatchesf.write((party+'\t'+tweet+'\n'))
                                    if party in partycount:
                                        partycount[party] += 1
                                    else:
                                        partycount[party] = 1
            except:
                pass

        if storeindb:
            tweetdb = MySQLdb.connect(host=db['host'], user=db['user'], passwd=db['passwd'],db=db['dbname'])
            cur = tweetdb.cursor()
            day = datehour.strftime("%Y%m%d")
            hour = datehour.strftime("%H") 
            for party in partycount:
                count = partycount[party]
                #print party, partycount[party]
                try:
                    cur.execute("INSERT INTO " + dbasetable + " (party, day, hour, nrtweets) VALUES ('%s','%s','%s','%d') " % (party, day, hour, count) )
                    tweetdb.commit()
                except:
                    tweetdb.rollback()

            tweetdb.close()
            print 'Stored in db'
        else:
            print 'Not stored in db'

        command = "rm"
        #argument = "-f"
        #command = "gzip"
        argument = "-f"
        #print command,argument,jsonfilename
        subprocess.call([command,argument,jsonfilename])

        return totcount

    except:
        return -1


twiqs = {<CENSORED>}
db = {<CENSORED>}
partypatterns = {}
partypatterns["vvd"] = ["v\\.?v\\.?d\\.?"]
partypatterns["pvda"] = ["p\\.?v\\.?d\\.?a\\.?","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+arbeid"]
partypatterns["sp"] = ["s\\.?p\\.?"]
partypatterns["pvv"] = ["p\\.?v\\.?v\\.?","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+vrijheid"]
partypatterns["cda"] = ["c\\.?d\\.?a\\.?"]
partypatterns["d66"] = ["d\'?66"]
partypatterns["gl"] = ["g\\.?l\\.?","groen.?links"]
partypatterns["cu"] = ["c\\.?u\\.?","christen.?unie"]
partypatterns["pvdd"] = ["p\\.?v\\.?d\\.?d\\.?","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+dieren"]
partypatterns["sgp"] = ["s\\.?g\\.?p\\.?"]
partypatterns["50plus"] = ["50[^\\d]?\s*(\\+|plus)"]
####
partypatterns["denk"] = ["denk"]
partypatterns["vnl"] = ["v\\.?n\\.?l\\.?","voornederland"]
partypatterns["ppnl"] = ["p\\.?p\\.?n\\.?l\\.?","piraten\\s*partij"]
####
partypatterns["fvd"] = ["f\\.?v\\.?d\\.?","forum\\s*v(oor)?\\s*democratie"]
partypatterns["geenpeil"] = ["geenpeil","geen\\s+peil"]
partypatterns["artikel1"] = ["art1kel","artikel\\s*1"]

#2017011222
#2017011304
#2017011319
#...
#2017011401
#2017011406
#...


#2017011704
#...
#2017011707
#2017011800
#2017011820
#2017011821

#2017020322
#2017020323
#2017020415
#2017020421
#2017020612

#2017020704
#2017020710
#2017020712
#2017020922
#2017021010
#2017021113

#2017022404
#2017022722
#2017022815
#2017030105
#2017030106

#2017030204
#2017030304
#2017030611
#2017030818
#2017030820
#2017030915
#2017031004
#2017031312
#2017031313
#2017031319
#2017031320
#2017031321
#2017031322
#2017031408
#2017031614
#2017031807




#datehour = datetime.datetime.strptime("2016121416","%Y%m%d%H") # starting time
#datehour = datetime.datetime.strptime("2017012219","%Y%m%d%H") # starting time
datehour = datetime.datetime.strptime("2017032414","%Y%m%d%H") # starting time
i = 1
while i == 1: # eternity
#while i < 50:
    partymatchesfilename = twiqsoutputfilename + '/partymatches'+datehour.strftime("%Y%m%d%H")+'.txt'
    if not os.path.exists(partymatchesfilename) and not datehour > (datetime.datetime.now() - datetime.timedelta(hours=2)):
        print 'harvesting tweets of ' + str(datehour) + ' at ' + str(datetime.datetime.now())
        totcount = gettweets2dbase(datehour,partypatterns,twiqs,db,storeindb=True,singleparty=singlepartybool)
        print 'harvested ' + str(totcount) + ' tweets'
        datehour = datehour + datetime.timedelta(hours=1)
    time.sleep(1800)
    #i += 1
