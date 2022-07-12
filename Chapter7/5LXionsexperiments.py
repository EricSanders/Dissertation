import VoxPopuli
import glob
import LXionresults
from collections import OrderedDict

nrdaysamounts = [1,2,3,4,5,6,7,8,9,10,15,20,25]
multiparties = [True,False]
excludeurls = [True,False]
excluderetweets = [True,False]
nonelectedparties = {}
excludenonelecteds = [False]
#nrdaysamounts = [1]
#multiparties = [True]
#excludeurls = [False]
#excluderetweets = [True]

years = (['2011','2012','2015','2017','2019'])
for year in years:
    nonelectedparties[year] = ['fnpo','ppnl','vnl','artikel1','nw','op','geenpeil','jezus']
#years = (['2011'])
startdir = "/vol/tensusers2/esanders/VoxPopuli/5LXions/TweetsCSVs"
outdir = "/vol/tensusers2/esanders/VoxPopuli/5LXions/MAEs"

# # # Polls # # # 

                        
electionpercentages = LXionresults.getpercentages(LXionresults.electionresults,nonelectedparties)
electionseats = LXionresults.getseats(LXionresults.electionresults,nonelectedparties)
pollpercentages = LXionresults.getpercentages(LXionresults.pollmdhresults,nonelectedparties)
pollseats = LXionresults.getseats(LXionresults.pollmdhresults,nonelectedparties)
outfilename = outdir + '/mae_polls.txt'
outfile = open(outfilename,'w')
abserrpercentages = OrderedDict()
abserrseats = OrderedDict()
nrparties = OrderedDict()
for year in years:
    abserrpercentages[year] = 0
    abserrseats[year] = 0
    nrparties[year] = 0
    for party in electionpercentages[year]:
        abserrpercentages[year] += abs(electionpercentages[year][party]-pollpercentages[year][party])
        abserrseats[year] += abs(electionseats[year][party]-pollseats[year][party])
        nrparties[year] += 1
        maepercentages = abserrpercentages[year]/nrparties[year]
        maeseats = abserrseats[year]/nrparties[year]
        outfile.write(year+" "+party+" %d %.2f %.2f %.2f %d %d %d\n" % (LXionresults.pollmdhresults[year][party],electionpercentages[year][party],pollpercentages[year][party],electionpercentages[year][party]-pollpercentages[year][party],electionseats[year][party],pollseats[year][party],electionseats[year][party]-pollseats[year][party]))
    outfile.write(year+" %d ------------ %.2f %d %.2f %.2f\n" % (0.0,abserrpercentages[year],abserrseats[year],maepercentages,maeseats))

#exit(0)

# # # Tweets # # #

corpus = VoxPopuli.TweetCorpusNonAnnotated()

for nrdays in nrdaysamounts:
    nrdaysname = str(nrdays)+'days'
    for multiparty in multiparties:
        mpname = 'monoparty'
        if multiparty:
            mpname = 'multiparty'
        for excludeurl in excludeurls:
            euname = 'includeurls'
            if excludeurl:
                euname = 'excludeurls'
            for excluderetweet in excluderetweets:
                ername = 'includeretweets'
                if excluderetweet:
                    ername = 'excluderetweets'

                tweetpartycounts = OrderedDict()
                nrtweets = OrderedDict()
                for year in years:
                    tweetpartycounts[year] = OrderedDict()
                    nrtweets[year] = 0
                    for party in LXionresults.electionresults[year]:
                        tweetpartycounts[year][party] = 0
                    corpus.clear()
                    csvdirname = startdir + '/' + year
                    csvfilenames = glob.glob(csvdirname+'/*.csv')
                    csvfilenames.sort()
                    selectedcsvfilenames = csvfilenames[len(csvfilenames)-nrdays-1:-1]

                    for csvfilename in selectedcsvfilenames:
                        corpus.readcsvfile(csvfilename)
                        for tweet in corpus.gettweets():
                            parties = tweet.getparties()
                            urls = tweet.geturls()
                            retweettotweetid = tweet.get('retweettotweetid')
                            replytotweetid = tweet.get('replytotweetid')
                            if (len(parties) == 1 or multiparty == True) and (urls[0] == '' or excludeurl == False) and ((retweettotweetid == 'NULL' and replytotweetid == 'NULL') or excluderetweet == False):
                                nrtweets[year] += 1
                                for party in parties:
                                    #if not party in outparties:
                                    tweetpartycounts[year][party] += 1

                inparties,outparties = LXionresults.getpartieswithseats(LXionresults.electionresults,tweetpartycounts)
                #print(inparties)
                #print(outparties)
                #exit(0)


                for excludenonelected in excludenonelecteds:
                    enname = 'allparties'
                    leaveoutparties = outparties
                    if excludenonelected:
                        enname = 'electedparties'
                        leaveoutparties = nonelectedparties
                        
                    electionpercentages = LXionresults.getpercentages(LXionresults.electionresults,leaveoutparties)
                    electionseats = LXionresults.getseats(LXionresults.electionresults,leaveoutparties)

                    predictionpercentages = LXionresults.getpercentages(tweetpartycounts,leaveoutparties)
                    predictionseats = LXionresults.getseats(tweetpartycounts,leaveoutparties)

                    outfilename = outdir + '/mae_'+nrdaysname+'_'+mpname+'_'+euname+'_'+ername+'_'+enname+'.txt'
                    #print(outfilename)
                    outfile = open(outfilename,'w')

                    abserrpercentages = OrderedDict()
                    abserrseats = OrderedDict()
                    nrparties = OrderedDict()
                    for year in years:
                        abserrpercentages[year] = 0
                        abserrseats[year] = 0
                        nrparties[year] = 0
                        for party in predictionpercentages[year]:
                            abserrpercentages[year] += abs(electionpercentages[year][party]-predictionpercentages[year][party])
                            abserrseats[year] += abs(electionseats[year][party]-predictionseats[year][party])
                            nrparties[year] += 1
                            maepercentages = abserrpercentages[year]/nrparties[year]
                            maeseats = abserrseats[year]/nrparties[year]
                            outfile.write(year+" "+party+" %d %.2f %.2f %.2f %d %d %d\n" % (tweetpartycounts[year][party],electionpercentages[year][party],predictionpercentages[year][party],electionpercentages[year][party]-predictionpercentages[year][party],electionseats[year][party],predictionseats[year][party],electionseats[year][party]-predictionseats[year][party]))
                        outfile.write(year+" %d ------------ %.2f %d %.2f %.2f\n" % (nrtweets[year],abserrpercentages[year],abserrseats[year],maepercentages,maeseats))


