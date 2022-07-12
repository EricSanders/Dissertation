import VoxPopuli
from voxpopulivariables import *
import colibricore

partypatterns = {}
partypatterns["denk"] = ["denk"]
prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)'
postpattern='(\s|\.|,|;|:|!|\?|$)'

denkcorpus = VoxPopuli.TweetCorpusNonAnnotated()
#denkcorpus.readgzfiles(firstdatehour='2014100100',lastdatehour='2014103123',pathname=tweetjsonfilesdir)
denkcorpus.readgzfiles(firstdatehour='2014110100',lastdatehour='2014113023',pathname=tweetjsonfilesdir)
#denkcorpus.readgzfiles(firstdatehour='2014120100',lastdatehour='2014123123',pathname=tweetjsonfilesdir)
#denkcorpus.readgzfiles(firstdatehour='2015010100',lastdatehour='2015013123',pathname=tweetjsonfilesdir)
#denkcorpus.readgzfiles(firstdatehour='2014030120',lastdatehour='2014030120',pathname=tweetjsonfilesdir)

denkcorpus.filteronpatterns(partypatterns,{},prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)

tweettexts = []

for tweetid in denkcorpus.tweets:
    tweettext = denkcorpus.tweets[tweetid].get('text')
    print(tweettext)
    
