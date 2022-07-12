#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,re,string,gzip, warnings
#import MySQLdb
import pymysql
import urllib2
from bs4 import BeautifulSoup

dbname = 'potwan'
dbuser = 'potwan_admin'
dbpasswd = open('/www/lands/live/etc/.pw_potwan_admin').read().strip()
dbhost = '<CENSORED>'

def checktweeterstatus(tweeternick):
    tweeturl = "https://twitter.com/" + tweeternick
    returnvalue = 0 # tweeter ok
    try:
        page = urllib2.urlopen(tweeturl).read()
        soup = BeautifulSoup(page)
        protected = soup.find_all("div", attrs={"data-protected": "true"})
        if protected:
            returnvalue = 2 # protected
        suspended = soup.find_all("div", attrs={"class": "route-account_suspended"})
        if suspended:
            returnvalue = 3 # suspended
    except urllib2.HTTPError as e:
        if e.code == 404:
            returnvalue = 1 # not existing

    return returnvalue

def main(argv=None):
    lastchecked = "mvdberg"
    lastcheckedseen = False


    db = pymysql.connect(dbhost,dbuser,dbpasswd,dbname,use_unicode=True,charset='utf8')
    cursor = db.cursor()

#    query = "SELECT * FROM annotator_tweeteroriginal_100_200"
    query = "SELECT * FROM annotator_tweeteroriginal"
    try:
        # Execute the SQL command
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            tweeterid = row[1]
            tweeternick = row[2]
            if lastcheckedseen:
                tweeterstatus = checktweeterstatus(tweeternick)
                print(tweeternick,str(tweeterstatus))
            else:
                if tweeternick == lastchecked:
                    lastcheckedseen = True

    except Exception as err:
        print(str(err))
        # Rollback in case there is any error
        db.rollback()



if __name__ == '__main__':
    sys.exit(main())
