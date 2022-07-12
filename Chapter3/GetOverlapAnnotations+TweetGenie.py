#!/usr/bin/pyton
import csv
from collections import defaultdict

allannotations = {}
nrallannotations = {}
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

    tweetgeniefile = open("tweeters_100_200_ok_tweetgenieoutput.txt")
    for line in tweetgeniefile:
        (tweeternick,tweeterid,gender,age) = line.split()
        if (tweeternick,tweeterid) not in tweetgenie:
            tweetgenie[(tweeternick,tweeterid)] = {}
        tweetgenie[(tweeternick,tweeterid)] = (gender,age)

    #print("tweeterid"+","+"tweeternick"+","+"gender ericsanders"+","+"genderconfidence ericsanders"+","+"age ericsanders"+","+"ageconfidence ericsanders"+","+"politicalpreference ericsanders"+","+"human ericsanders"+","+"gender michelledegier"+","+"genderconfidence michelledegier"+","+"age michelledegier"+","+"ageconfidence michelledegier"+","+"politicalpreference michelledegier"+","+"human michelledegier"+","+"gender elinepilaet"+","+"genderconfidence elinepilaet"+","+"age elinepilaet"+","+"ageconfidence elinepilaet"+","+"politicalpreference elinepilaet"+","+"human elinepilaet"+","+"gender tweetgenie"+","+"age tweetgenie")
    csvoutputfile = open("OverlapAnnotations+TweetGenie.csv","w")
    csvoutput = csv.writer(csvoutputfile,delimiter=";",quotechar="'")
    csvoutput.writerow(["tweeterid","tweeternick","gender ericsanders","genderconfidence ericsanders","age ericsanders","ageconfidence ericsanders","politicalpreference ericsanders","human ericsanders","gender michelledegier","genderconfidence michelledegier","age michelledegier","ageconfidence michelledegier","politicalpreference michelledegier","human michelledegier","gender elinepilaet","genderconfidence elinepilaet","age elinepilaet","ageconfidence elinepilaet","politicalpreference elinepilaet","human elinepilaet","gender tweetgenie","age tweetgenie"])
    for (tweeterid,tweeternick) in allannotations:
        if nrallannotations[(tweeterid,tweeternick)] > 2:
            printline = tweeterid + "," + tweeternick
            csvrow = (tweeterid,tweeternick)
            #for annotator in allannotations[(tweeterid,tweeternick)]:
            for annotator in ("ericsanders","michelledegier","elinepilaet"):
                #print (tweeterid,tweeternick,annotator,allannotations[(tweeterid,tweeternick)][annotator])
                printline += "," + ",".join(allannotations[(tweeterid,tweeternick)][annotator])
                csvrow += allannotations[(tweeterid,tweeternick)][annotator]
            if (tweeternick,tweeterid) in tweetgenie:
                #print(tweetgenie[(tweeternick,tweeterid)])
                printline += "," + ",".join(tweetgenie[(tweeternick,tweeterid)])
                csvrow += tweetgenie[(tweeternick,tweeterid)]
            #print(printline)
            csvoutput.writerow(csvrow)
