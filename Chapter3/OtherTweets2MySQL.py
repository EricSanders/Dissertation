#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,re,string,gzip, warnings
#import MySQLdb
import pymysql

minimumnrtweets = 100
maximumnrtweets = 200

inputs = ((
'2012', # year
'/vol/tensusers/hvhalteren/newtweets/201209', # sourcerootdir
'2012090100', # first
#'2012091223', # first
'2012091223' # last
),(
'2015', # year
'/vol/tensusers/hvhalteren/newtweets/201503', # sourcerootdir
'2015030700', # first
#'2015031823', # first
'2015031823' # last
))
#results:
#1631513 inserted
#19877 errors


dbname = 'potwan'
dbuser = 'potwan_admin'
dbpasswd = open('/www/lands/live/etc/.pw_potwan_admin').read().strip()
dbhost = '<CENSORED>'

def main(argv=None):
    oks = 0
    errors = 0
    allpoliticaltweeters = {}
    db = pymysql.connect(dbhost,dbuser,dbpasswd,dbname,use_unicode=True,charset='utf8')
    cursor = db.cursor()

    warnings.filterwarnings("error")

    
    query = "SELECT * FROM annotator_tweeteroriginal"
    try:
        # Execute the SQL command
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            tweeterid = row[1]
            tweeternick = row[2]
            if (tweeterid,tweeternick) in allpoliticaltweeters:
                allpoliticaltweeters[(tweeterid,tweeternick)] += 1
            else:
                allpoliticaltweeters[(tweeterid,tweeternick)] = 1
            #print(tweeterid)
    except Exception as err:
        print(str(err))
        # Rollback in case there is any error
        db.rollback()

    for input in inputs:
        for root, dirs, files in os.walk(input[1]):
            print("going through ",input[1])
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
                    if int(ymdh) >= int(input[2]) and int(ymdh) <= int(input[3]):
                        #print ymdh
                        #if 1 == 2:
                        f = gzip.open(dirfilename,'rt',encoding='utf-8')
                        for line in f:
                            #print(repr(line))
    #                        fields = line.decode('utf8').split('\t')
    #                        fields = line.split(b'\t')
                            fields = line.split('\t')
                            try:
                                tweetid = fields[0]
                                datetime = fields[1]
                                replytotweetid = fields[2]
                                replytotweeterid = fields[3]
                                replytotweeternick = fields[4]
                                retweettotweetid = fields[5]
                                retweettotweeterid = fields[6]
                                retweettotweeternick = fields[7]
                                nrretweets = fields[8]
                                tweeterid = fields[9]
                                tweeternick = fields[10]
                                text = pymysql.escape_string(fields[21])
                                #text = pymysql.converters.escape_bytes(fields[21])
                                #text = fields[21]
                                if (tweeterid,tweeternick) in allpoliticaltweeters:
                                    allpoliticaltweeters[(tweeterid,tweeternick)] += 1

                            except:
                                pass
                
#    for (tweeterid,tweeternick),nr in allpoliticaltweeters.items():
#        print(tweeterid,tweeternick,nr)
#    for (tweeterid,tweeternick) in sorted(allpoliticaltweeters, key=allpoliticaltweeters.get,reverse=True):
#        print(tweeterid,tweeternick,allpoliticaltweeters[(tweeterid,tweeternick)])


#    db.close()
#    exit(0)

    for input in inputs:
        for root, dirs, files in os.walk(input[1]):
            print("going through ",input[1])
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
                    if int(ymdh) >= int(input[2]) and int(ymdh) <= int(input[3]):
                        #print ymdh
                        #if 1 == 2:
                        f = gzip.open(dirfilename,'rt',encoding='utf-8')
                        for line in f:
                            #print(repr(line))
    #                        fields = line.decode('utf8').split('\t')
    #                        fields = line.split(b'\t')
                            fields = line.split('\t')
                            try:
                                tweetid = fields[0]
                                datetime = fields[1]
                                replytotweetid = fields[2]
                                replytotweeterid = fields[3]
                                replytotweeternick = fields[4]
                                retweettotweetid = fields[5]
                                retweettotweeterid = fields[6]
                                retweettotweeternick = fields[7]
                                nrretweets = fields[8]
                                tweeterid = fields[9]
                                tweeternick = fields[10]
                                text = pymysql.escape_string(fields[21])
                                #text = pymysql.converters.escape_bytes(fields[21])
                                #text = fields[21]
                                if (tweeterid,tweeternick) in allpoliticaltweeters:
                                    if allpoliticaltweeters[(tweeterid,tweeternick)] >= minimumnrtweets and allpoliticaltweeters[(tweeterid,tweeternick)] <= maximumnrtweets:

                                        query = "INSERT INTO annotator_alltweetoriginal(tweetid,text,tweeterid,tweeternick,datetime,replytotweetid,retweettotweetid,year) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (tweetid,text,tweeterid,tweeternick,datetime,replytotweetid,retweettotweetid,input[0])

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
                                            #print(tweetid,text,tweeternick,datetime,replytotweetid,retweettotweetid)
                                            # Rollback in case there is any error
                                            db.rollback()
                            except:
                                pass
                
    db.close()
    print(str(oks) + " inserted")
    print(str(errors) + " errors")

if __name__ == '__main__':
    sys.exit(main())
