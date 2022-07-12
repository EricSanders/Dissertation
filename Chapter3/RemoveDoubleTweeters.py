#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,re,string,warnings
import pymysql

dbname = 'potwan'
dbuser = 'potwan_admin'
dbpasswd = open('/www/lands/live/etc/.pw_potwan_admin').read().strip()
dbhost = '<CENSORED>'

def main(argv=None):
    alltweeters = {}
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
            if (tweeterid,tweeternick) in alltweeters:
                print("deleting",tweeterid,tweeternick,"with id",str(id),"already in db with id",str(alltweeters[(tweeterid,tweeternick)]))
#                delquery = "DELETE FROM annotator_tweeteroriginal_100_200 WHERE id='%s'" % id
                delquery = "DELETE FROM annotator_tweeteroriginal WHERE id='%s'" % id
                try:
                    # Execute the SQL command
                    cursor.execute(delquery)
                    db.commit()
                except Exception as err:
                    print(str(err))
            else:
                print("keeping",tweeterid,tweeternick,"with id",str(id))
                alltweeters[(tweeterid,tweeternick)] = id
            
    except Exception as err:
        print(str(err))
        # Rollback in case there is any error
        db.rollback()



if __name__ == '__main__':
    sys.exit(main())
