import VoxPopuli
from voxpopulivariables import *
#import colibricore

partypatterns = {}
partypatterns["ben"] = ["ben"]
prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)'
postpattern='(\s|\.|,|;|:|!|\?|$)'

bencorpus = VoxPopuli.TweetCorpusNonAnnotated()
#bencorpus.readgzfiles(firstdatehour='2014100100',lastdatehour='2014101523',pathname=tweetjsonfilesdir)
#bencorpus.readgzfiles(firstdatehour='2014101600',lastdatehour='2014103123',pathname=tweetjsonfilesdir)
#bencorpus.readgzfiles(firstdatehour='2014110100',lastdatehour='2014111523',pathname=tweetjsonfilesdir)
#bencorpus.readgzfiles(firstdatehour='2014111600',lastdatehour='2014113023',pathname=tweetjsonfilesdir)
#bencorpus.readgzfiles(firstdatehour='2014120100',lastdatehour='2014121523',pathname=tweetjsonfilesdir)
#bencorpus.readgzfiles(firstdatehour='2014121600',lastdatehour='2014123123',pathname=tweetjsonfilesdir)
#bencorpus.readgzfiles(firstdatehour='2015010100',lastdatehour='2015011523',pathname=tweetjsonfilesdir)
bencorpus.readgzfiles(firstdatehour='2015011600',lastdatehour='2015013123',pathname=tweetjsonfilesdir)
#bencorpus.readgzfiles(firstdatehour='2014030120',lastdatehour='2014030120',pathname=tweetjsonfilesdir)

bencorpus.filteronpatterns(partypatterns,{},prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)

tweettexts = []

for tweetid in bencorpus.tweets:
    tweettext = bencorpus.tweets[tweetid].get('text')
    print(tweettext)
    
