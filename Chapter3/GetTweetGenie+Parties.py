#!/usr/bin/pyton
import sys,csv,re,pymysql
from collections import defaultdict

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

def getpartiesintweet(tweet):
    parties = []
    for party in partypatterns:
        for partypattern in partypatterns[party]:
            pattern = '(\s|\.|,|;|:|!|\?|\@|\#|^)'+partypattern+'(\s|\.|,|;|:|!|\?|$)'
#            partymatch = re.search(pattern.encode('utf8'),tweet,re.IGNORECASE)
            partymatch = re.search(pattern,tweet,re.IGNORECASE)
            if partymatch:
                parties.append(party)
    return(parties)

def main(argv=None):
    allannotations = {}
    nrallannotations = {}
    allannotators = []
    tweetgenie = {}
    alltweeters = {}
    alltweets = {}

    tweetgeniefile = open("tweeters_ok_tweetgenieoutput.txt")
    for line in tweetgeniefile:
        (tweeternick,tweeterid,gender,age) = line.split()
        if (tweeternick,tweeterid) not in tweetgenie:
            tweetgenie[(tweeternick,tweeterid)] = {}
        tweetgenie[(tweeternick,tweeterid)] = (gender,age)

    csvoutputfile = open("TweetGenie+Parties.csv","w")
    csvoutput = csv.writer(csvoutputfile,delimiter=";",quotechar="'")
    csvoutput.writerow(["tweeterid","tweeternick","gender tweetgenie","age tweetgenie","party","year","tweetid"])

    dbname = 'potwan'
    dbuser = 'potwan_admin'
    dbpasswd = open('/www/lands/live/etc/.pw_potwan_admin').read().strip()
    dbhost = '<CENSORED>'

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
            tweeternick = row[3]
            year = row[7]
            if not tweeternick in alltweets:
                alltweets[tweeternick] = []
            alltweets[tweeternick].append((tweetid,text,year))
                
    except Exception as err:
        print(str(err))
        # Rollback in case there is any error
        db.rollback()

    for (tweeternick,tweeterid) in tweetgenie:
        if tweeternick in alltweets:
            for (tweetid,text,year) in alltweets[tweeternick]:
                for party in getpartiesintweet(text):
                    csvrow = (tweeterid,tweeternick) + tweetgenie[(tweeternick,tweeterid)] + (party,year,tweetid)
                    csvoutput.writerow(csvrow)

if __name__ == '__main__':
    sys.exit(main())
