import VoxPopuli

partypatterns = {}
partypatterns["vvd"] = ["v\\.?v\\.?d\\.?"]
partypatterns["pvda"] = ["p\\.?v\\.?d\\.?a\\.?","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+arbeid"]
partypatterns["sp"] = ["s\\.?p\\.?"]
partypatterns["pvv"] = ["p\\.?v\\.?v\\.?","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+vrijheid"]
partypatterns["cda"] = ["c\\.?d\\.?a\\.?"]
partypatterns["d66"] = ["d\'?66"]
partypatterns["gl"] = ["g\\.?l\\.?","groen.?links"]
partypatterns["cu"] = ["c\\.?u\\.?","christen.?unie"]
partypatterns["pvdd"] = ["p\\.?v\\.?d\\.?d\\.?","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+dieren","dierenpartij"]
partypatterns["sgp"] = ["s\\.?g\\.?p\\.?"]
partypatterns["50plus"] = ["50[^\\d]?\s*(\\+|plus)"]
####
partypatterns["denk"] = ["denk"]
partypatterns["fvd"] = ["f\\.?v\\.?d\\.?","forum\\s*v(oor)?\\s*democratie"]
####
#partypatterns["vnl"] = ["v\\.?n\\.?l\\.?","voornederland"]
#partypatterns["ppnl"] = ["p\\.?p\\.?n\\.?l\\.?","piraten\\s*partij"]
#partypatterns["geenpeil"] = ["geen.?peil"]
#partypatterns["artikel1"] = ["art1kel","artikel\\s*1"]
#partypatterns["nw"] = ["nieuwe.?wegen"]
#partypatterns["op"] = ["ondernemers.?partij"]
#partypatterns["jezus"] = ["jezus.?leeft"]

prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)'
postpattern='(\s|\.|,|;|:|!|\?|$)'

tgztweetsstartdir = "/vol/bigdata2/datasets2/twitter"
outdir = "/vol/tensusers2/esanders/VoxPopuli/5LXions/TweetsCSVs/2019"

corpus = VoxPopuli.TweetCorpusNonAnnotated()

#for dayrange in ((range(20110201,20110229),range(20110301,20110303))):
#for dayrange in ((range(20110201,20110206),range(0,0))):
#for dayrange in ((range(20110206,20110211),range(0,0))):
#for dayrange in ((range(20110211,20110216),range(0,0))):
#for dayrange in ((range(20110216,20110221),range(0,0))):
#for dayrange in ((range(20110221,20110226),range(0,0))):
#for dayrange in ((range(20110226,20110229),range(20110301,20110303),range(0,0))):

#for dayrange in ((range(20120813,20120831),range(20120901,20120913))):
#for dayrange in ((range(20120813,20120818),range(0,0))):
#for dayrange in ((range(20120818,20120823),range(0,0))):
#for dayrange in ((range(20120823,20120828),range(0,0))):
#for dayrange in ((range(20120828,20120831),range(20120901,20120903),range(0,0))):
#for dayrange in ((range(20120903,20120908),range(0,0))):

#for dayrange in ((range(20150217,20150229),range(20150301,20150318))):
#for dayrange in ((range(20150217,20150222),range(0,0))):
#for dayrange in ((range(20150222,20150227),range(0,0))):
#for dayrange in ((range(20150227,20150229),range(20150301,20150304),range(0,0))):
#for dayrange in ((range(20150304,20150309),range(0,0))):
#for dayrange in ((range(20150309,20150314),range(0,0))):
#for dayrange in ((range(20150314,20150319),range(0,0))):

#for dayrange in ((range(20170214,20170229),range(20150301,20150316))):
#for dayrange in ((range(20170214,20170219),range(0,0))):
#for dayrange in ((range(20170219,20170224),range(0,0))):
#for dayrange in ((range(20170224,20170229),range(0,0))):
#for dayrange in ((range(20170301,20170306),range(0,0))):
#for dayrange in ((range(20170306,20170311),range(0,0))):
#for dayrange in ((range(20170311,20170316),range(0,0))):
#for dayrange in ((range(20170216,20170219),range(0,0))):

#for dayrange in ((range(20190219,20190229),range(20190301,20190320))):
for dayrange in ((range(20190320,20190321),range(0,0))):
#for dayrange in ((range(20190222,20190227),range(0,0))):
#for dayrange in ((range(20190227,20190229),range(20190301,20190304),range(0,0))):
#for dayrange in ((range(20190304,20190309),range(0,0))):
#for dayrange in ((range(20190309,20190314),range(0,0))):
#for dayrange in ((range(20190314,20190319),range(0,0))):

    for day in dayrange:

        firstdatehour = str(day)+"00"
#        lastdatehour = str(day)+"00"
        lastdatehour = str(day)+"23"

        corpus.clear()
        print("reading day " + str(day))
        corpus.readgzfiles(firstdatehour,lastdatehour,tgztweetsstartdir)
        print("filtering")
        corpus.filteronpatterns(partypatterns,{},prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)
#        for tweet in corpus.gettweets():
#            urls = tweet.geturls()
#            if urls:
#                print('___'.join(urls))
#        outcsvfile = outdir + "/poltweets_" + str(day) + "_test.csv"
        outcsvfile = outdir + "/poltweets_" + str(day) + ".csv"
        print("writing")
        corpus.writecsvfile(outcsvfile)

