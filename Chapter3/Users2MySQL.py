#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,re,string,gzip,warnings
#import MySQLdb
#import MySQLdb as pymysql
import pymysql
#import pymysql as MySQLdb # python3

#sourcerootdir = '/vol/tensusers/hvhalteren/newtweets/201209'
#first = '2012090100'
#first = '2012091223'
#last = '2012091223'
#80094 inserted
#15 errors

sourcerootdir = '/vol/tensusers/hvhalteren/newtweets/201503'
first = '2015030700'
#last = '2015030700'
last = '2015031823'
#42288 inserted
#10 errors


dbname = 'potwan'
dbuser = 'potwan_admin'
dbpasswd = open('/www/lands/live/etc/.pw_potwan_admin').read().strip()
dbhost = '<CENSORED>'

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

def partytweet(tweet):
    for party in partypatterns:
        for partypattern in partypatterns[party]:
            pattern = '(\s|\.|,|;|:|!|\?|\@|\#|^)'+partypattern+'(\s|\.|,|;|:|!|\?|$)'
#            partymatch = re.search(pattern.encode('utf8'),tweet,re.IGNORECASE)
            partymatch = re.search(pattern,tweet,re.IGNORECASE)
            if partymatch:
                return(True)
    return(False)
 
def main(argv=None):
    partytweeterids = {}
    partytweeteridsinserted = {}
    oks = 0
    errors = 0
    db = pymysql.connect(dbhost,dbuser,dbpasswd,dbname,use_unicode=True,charset='utf8')
    cursor = db.cursor()

    warnings.filterwarnings("error")

    for root, dirs, files in os.walk(sourcerootdir):
        #print 'root:' + root
        for dirname in dirs:
            pass
            #print 'dirname: ' + dirname
        for filename in files:
            #print 'filename: ' + filename
            #print 'root+filename: ' + os.path.join(root, filename)
            dirfilename = root + '/' + filename
            fnm = re.match('(\d{10}).twt.gz',filename)
            if fnm:
                ymdh = fnm.group(1)
                if int(ymdh) >= int(first) and int(ymdh) <= int(last):
                    #print ymdh
                    #if 1 == 2:
                    f = gzip.open(dirfilename,'rt',encoding='utf-8')
                    for line in f:
                        #print(repr(line))
#                        fields = line.decode('utf8').split('\t')
#                        fields = line.split(b'\t')
                        fields = line.split('\t')
                        try:
                            tweeterid = fields[9]
                            tweeternick = fields[10]
                            text = pymysql.escape_string(fields[21])
                            #text = pymysql.converters.escape_bytes(fields[21])
                            #text = fields[21]
                            if partytweet(text):
                                if (tweeterid,tweeternick) in partytweeterids:
                                    partytweeterids[(tweeterid,tweeternick)] += 1
                                else :
                                    partytweeterids[(tweeterid,tweeternick)] = 1

                        except:
                            pass

    for root, dirs, files in os.walk(sourcerootdir):
        #print 'root:' + root
        for dirname in dirs:
            pass
            #print 'dirname: ' + dirname
        for filename in files:
            #print 'filename: ' + filename
            #print 'root+filename: ' + os.path.join(root, filename)
            dirfilename = root + '/' + filename
            fnm = re.match('(\d{10}).usr.gz',filename)
            if fnm:
                ymdh = fnm.group(1)
                if int(ymdh) >= int(first) and int(ymdh) <= int(last):
                    #print ymdh
                    #if 1 == 2:
                    f = gzip.open(dirfilename,'rt',encoding='utf-8')
                    for line in f:
                        fields = line.split('\t')
                        try:
                            tweeterid = fields[0]
                            tweeternick = pymysql.escape_string(fields[1])
                            tweetername = pymysql.escape_string(fields[2])
                            tweeterinfo = pymysql.escape_string(fields[3])
                            tweeterlocation = pymysql.escape_string(fields[5])
                            tweetertimezone = fields[6]
                            tweeterlanguage = fields[7]
                            tweeterwebsite = fields[8]

                            if (tweeterid,tweeternick) in partytweeterids and not (tweeterid,tweeternick) in partytweeteridsinserted:
                                query = "INSERT INTO annotator_tweeteroriginal(tweeterid,tweeternick,tweetername,tweeterinfo,tweeterlocation,tweetertimezone,tweeterlanguage,tweeterwebsite) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (tweeterid,tweeternick,tweetername,tweeterinfo,tweeterlocation,tweetertimezone,tweeterlanguage,tweeterwebsite)
                                #cursor.execute(query)
                                try:
                                    oks += 1
                                    # Execute the SQL command
                                    cursor.execute(query)
                                    # Commit your changes in the database
                                    db.commit()
                                except Exception as err:
                                    errors += 1
                                    #sys.stderr.write('ERROR: %s\n' % str(err))
                                    #print(str(err))
                                    #print(tweeterid,tweeternick,tweetername,tweeterinfo,tweeterlocation,tweetertimezone,tweeterlanguage,tweeterwebsite)
                                    # Rollback in case there is any error
                                    db.rollback()

                                if (tweeterid,tweeternick) in partytweeteridsinserted:
                                    partytweeteridsinserted[(tweeterid,tweeternick)] += 1
                                else :
                                    partytweeteridsinserted[(tweeterid,tweeternick)] = 1


                        except:
                            pass
                          
#    for (tweeterid,tweeternick),nr in partytweeterids.items():
#        print(tweeterid,tweeternick,nr)
                
    db.close()
    print(str(oks) + " inserted")
    print(str(errors) + " errors")

if __name__ == '__main__':
    sys.exit(main())
