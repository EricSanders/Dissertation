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

    with open("annotator_tweeterannotation_20160530.csv","r") as csvfile:
        tweeterannotations = csv.reader(csvfile)
        tweeter = []
        for row in tweeterannotations:
            annotator = row[1]
            tweeterid = row[2]
            tweeternick = row[3]
            gender = row[4]
            genderconfidence = row[5]
            age = row[6]
            ageconfidence = row[8]
            politicalpreference = row[9]
            human = row[10]

            if (tweeterid,tweeternick) not in nrallannotations:
                nrallannotations[(tweeterid,tweeternick)] = 0
            nrallannotations[(tweeterid,tweeternick)] += 1
            if (tweeterid,tweeternick) not in allannotations:
                allannotations[(tweeterid,tweeternick)] = {}
            if annotator not in allannotations[(tweeterid,tweeternick)]:
                allannotations[(tweeterid,tweeternick)][annotator] = {}
            allannotations[(tweeterid,tweeternick)][annotator] = (gender,genderconfidence,age,ageconfidence,politicalpreference,human)
            if annotator not in allannotators:
                allannotators.append(annotator)

        tweetgeniefile = open("tweeters_100_200_ok_tweetgenieoutput.txt")
        for line in tweetgeniefile:
            (tweeternick,tweeterid,gender,age) = line.split()
            if (tweeternick,tweeterid) not in tweetgenie:
                tweetgenie[(tweeternick,tweeterid)] = {}
            tweetgenie[(tweeternick,tweeterid)] = (gender,age)

        for (tweeterid,tweeternick) in allannotations:
            if nrallannotations[(tweeterid,tweeternick)] > 0:
                for annotator in allannotations[(tweeterid,tweeternick)]:
                    tweeter = (tweeterid,tweeternick,annotator)
                    tweeter += allannotations[(tweeterid,tweeternick)][annotator]
                    if (tweeternick,tweeterid) in tweetgenie:
                        #print(tweetgenie[(tweeternick,tweeterid)])
                        tweeter += tweetgenie[(tweeternick,tweeterid)]
                    alltweeters[tweeternick] = tweeter



    csvoutputfile = open("AllAnnotations+TweetGenie+Parties.csv","w")
    csvoutput = csv.writer(csvoutputfile,delimiter=";",quotechar="'")
    csvoutput.writerow(["tweeterid","tweeternick","annotator","gender","genderconfidence","age","ageconfidence","politicalpreference","human","gender tweetgenie","age tweetgenie","party","year","tweetid"])

    dbname = 'potwan'
    dbuser = 'potwan_admin'
    dbpasswd = open('/www/lands/live/etc/.pw_potwan_admin').read().strip()
    dbhost = '<CENSORED>'

    db = pymysql.connect(dbhost,dbuser,dbpasswd,dbname,use_unicode=True,charset='utf8')
    cursor = db.cursor()

    for tweeternick in alltweeters:
        query = "SELECT * FROM annotator_tweetoriginal WHERE tweeter='%s'" % tweeternick
        try:
            # Execute the SQL command
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                tweetid = row[1]
                text = row[2]
                year = row[7]
                for party in getpartiesintweet(text):
                    csvrow = alltweeters[tweeternick] + (party,year,tweetid)
                    csvoutput.writerow(csvrow)
        except Exception as err:
            print(str(err))
            # Rollback in case there is any error
            db.rollback()

if __name__ == '__main__':
    sys.exit(main())
