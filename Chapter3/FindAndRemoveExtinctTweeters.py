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
    db = pymysql.connect(dbhost,dbuser,dbpasswd,dbname,use_unicode=True,charset='utf8')
    cursor = db.cursor()

    query = "SELECT * FROM annotator_tweeterannotation"
    try:
        # Execute the SQL command
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            userid = row[1]
            tweeterid = row[2]
            tweeternick = row[3]
            tweeterstatus = checktweeterstatus(tweeternick)
            if tweeterstatus:
                print(str(id),str(userid),"https://twitter.com/" + tweeternick,str(tweeterstatus))
                delquery = "DELETE FROM annotator_tweeterannotation WHERE id='%s'" % id
                try:
                    # Execute the SQL command
                    cursor.execute(delquery)
                    db.commit()
                except Exception as err:
                    print(str(err))
                    # Rollback in case there is any error

    except Exception as err:
        print(str(err))
        # Rollback in case there is any error
        db.rollback()



if __name__ == '__main__':
    sys.exit(main())
