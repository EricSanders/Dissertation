#!/usr/bin/pyton
import csv
from collections import defaultdict

allannotations = {}
nrallannotations = {}
allannotators = []
tweetgenie = {}

with open("annotator_tweeterannotation_20160530.csv","r") as csvfile:
    tweeterannotations = csv.reader(csvfile)
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

    csvoutputfile = open("AllAnnotations+TweetGenie.csv","w")
    csvoutput = csv.writer(csvoutputfile,delimiter=";",quotechar="'")
    csvoutput.writerow(["tweeterid","tweeternick","annotator","gender","genderconfidence","age","ageconfidence","politicalpreference","human","gender tweetgenie","age tweetgenie"])
    for (tweeterid,tweeternick) in allannotations:
        if nrallannotations[(tweeterid,tweeternick)] > 0:
            for annotator in allannotations[(tweeterid,tweeternick)]:
                #print (tweeterid,tweeternick,annotator,allannotations[(tweeterid,tweeternick)][annotator])
                printline = tweeterid + "," + tweeternick
                csvrow = (tweeterid,tweeternick,annotator)
                printline += "," + "," + annotator + ",".join(allannotations[(tweeterid,tweeternick)][annotator])
                csvrow += allannotations[(tweeterid,tweeternick)][annotator]
                if (tweeternick,tweeterid) in tweetgenie:
                    #print(tweetgenie[(tweeternick,tweeterid)])
                    printline += "," + ",".join(tweetgenie[(tweeternick,tweeterid)])
                    csvrow += tweetgenie[(tweeternick,tweeterid)]
                    #print(printline)
                csvoutput.writerow(csvrow)
