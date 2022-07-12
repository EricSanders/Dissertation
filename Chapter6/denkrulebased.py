import VoxPopuli
from voxpopulivariables import *
import copy
import datetime
from collections import OrderedDict

denkpatterns = {}
denkpatterns["denk"] = ["denk"]

denkbigrampatternsbasic = {}
denkbigrampatternsbasic["denk"] = [
    'ik\\s+denk', #+ #party in bigram error = 0% #percentage bigrams = 26%
    'denk\\s+ik', #+ #party in bigram error = 0% #percentage bigrams = 24%
    'denk\\s+je', #+ #party in bigram error = 0% #percentage bigrams = 6%
    'denk\\s+jij', #+ #party in bigram error = 0% #percentage bigrams = 1%
    'denk\\s+dat', #+ #party in bigram error = 0% #percentage bigrams = 22%
    'denk\\s+alleen', #+ #party in bigram error = 0% #percentage bigrams = 0%
    'denk\\s+da', #+ #party in bigram error = 0% #percentage bigrams = 0%
    'denk\\s+daar', #+ #party in bigram error = 0% #percentage bigrams = 0%
    'denk\\s+eens', #+ #party in bigram error = 0% #percentage bigrams = 0%
    'denk\\s+eerder', #+ #party in bigram error = 0% #percentage bigrams = 0%
    'denk\\s+het', #+ #party in bigram error = 1% #percentage bigrams = 3%
]
denkbigrampatternsoptionaldummy = {}
denkbigrampatternsoptionaldummy["denk"] = [
    'abcxyz'
    ]
denkbigrampatternsoptional = {}
denkbigrampatternsoptional["denk"] = [
    'denk\\s+aan', #+ #party in bigram error = 4% #percentage bigrams = 2%
    'aan\\s+denk', #+ #party in bigram error = 23% #percentage bigrams = 0%
    'dan\\s+denk', #+ #party in bigram error = 7% #percentage bigrams = 1%
    'en\\s+denk', #+ #party in bigram error = 49% #percentage bigrams = 2%
    'ga\\s+denk', #+ #new #party in bigram error = 3% #percentage bigrams = 0%
    'je\\s+denk', #+ #new #party in bigram error = 12% #percentage bigrams = 0%
    'maar\\s+denk', #+ #party in bigram error = 4% #percentage bigrams = 1%
    'denk\\s+als', #+ #party in bigram error = 36% #percentage bigrams = 0%
    'denk\\s+bij', #+ #party in bigram error = 50% #percentage bigrams = 0%
    'denk\\s+dan', #+ #party in bigram error = 11% #percentage bigrams = 0%
    'denk\\s+dit', #+ (-) #party in bigram error = NaN% #percentage bigrams = 0%
    'denk\\s+een', #+ #party in bigram error = 32% #percentage bigrams = 0%
    'denk\\s+er', #+ #party in bigram error = 12% #percentage bigrams = 0%
    'denk\\s+even', #+ #party in bigram error = 33% #percentage bigrams = 0%
    'denk\\s+ff', #+ (-) #party in bigram error = NaN% #percentage bigrams = 0%
    'denk\\s+hier', #+ (-) #party in bigram error = 30% #percentage bigrams = 0%
    'denk\\s+maar', #+ #party in bigram error = 25% #percentage bigrams = 0%
    'denk\\s+mee', #+ #party in bigram error = 10% #percentage bigrams = 0%
    'denk\\s+na', #+ #party in bigram error = 9% #percentage bigrams = 0%
    'denk\\s+niet', #+ #party in bigram error = 7% #percentage bigrams = 2%
    'denk\\s+nog', #+ #party in bigram error = 16% #percentage bigrams = 0%
    'denk\\s+nu', #+ #party in bigram error = 20% #percentage bigrams = 0%
    'denk\\s+ook', #+ #party in bigram error = 10% #percentage bigrams = 1%
    'denk\\s+over', #+ (-) #party in bigram error = NaN% #percentage bigrams = 0%
    'denk\\s+t', #+ #new #party in bigram error = 2% #percentage bigrams = 0%
    'denk\\s+te', #+ #party in bigram error = 78% #percentage bigrams = 0%
    'denk\\s+toch', #+ #party in bigram error = 2% #percentage bigrams = 0%
    'denk\\s+weer', #+ (-) #party in bigram error = NaN% #percentage bigrams = 0%
    'denk\\s+wel' #+ #party in bigram error = 3% #percentage bigrams = 0%
]

    
prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)'
postpattern='(\s|\.|,|;|:|!|\?|$)'


# read original tweets
corpus_denk = VoxPopuli.TweetCorpusAnnotated()
corpus_denkniet = VoxPopuli.TweetCorpusAnnotated()
corpus_denk.readmysql(db_denk_original,'tweetid', aliases = {'datetime': 'tweetdatetime'})
corpus_denk_noretweets = corpus_denk.select_matchallfilters([('retweettotweetid','NULL')])
nr_denk_original = len(corpus_denk_noretweets.tweets)
corpus_denkniet.readmysql(db_denkniet_original,'tweetid', aliases = {'datetime': 'tweetdatetime'})
corpus_denkniet_noretweets = corpus_denkniet.select_matchallfilters([('retweettotweetid','NULL')])
nr_denkniet_original = len(corpus_denkniet_noretweets.tweets)

corpus_original = corpus_denk_noretweets + corpus_denkniet_noretweets

# read annotated tweets
corpus_denk.readmysql(db_denk_annotated,'tweetid','userid')
corpus_denk.removenunannotated(decidingannotatorid='eric')
corpus_denk.shuffle(seed=1)
nr_denk_annotated = len(corpus_denk.tweets)
corpus_denkniet.readmysql(db_denkniet_annotated,'tweetid','userid')
corpus_denkniet.removenunannotated(decidingannotatorid='eric')
corpus_denkniet.shuffle(seed=1)
nr_denkniet_annotated = len(corpus_denkniet.tweets)


(nr_denk_annotated_adapted,nr_denkniet_annotated_adapted) = VoxPopuli.computeproportionalamounts(nr_denk_original,nr_denkniet_original,nr_denk_annotated,nr_denkniet_annotated)

print('\tdenkniet set\tdenk set\t(without retweets)')
print('all\t\t',nr_denkniet_original,'\t',nr_denk_original)
print('annotated\t',nr_denkniet_annotated,'\t',nr_denk_annotated)
print('adapted\t\t',nr_denkniet_annotated_adapted,'\t',nr_denk_annotated_adapted)
print('+ + + + + + + +')
print('fixed patterns:')
for patternbasic in denkbigrampatternsbasic["denk"]:
    print(patternbasic)


corpus_denk_annotated = corpus_denk.part(nr_denk_annotated_adapted)
corpus_denkniet_annotated = corpus_denkniet.part(nr_denkniet_annotated_adapted)
corpus_annotated = corpus_denk_annotated + corpus_denkniet_annotated

for patternoptional in denkbigrampatternsoptionaldummy["denk"]:
#for patternoptional in denkbigrampatternsoptional["denk"]:
    denkbigrampatterns = {}
    denkbigrampatterns["denk"] = []
    
    for patternbasic in denkbigrampatternsbasic["denk"]:
        denkbigrampatterns["denk"].append(patternbasic)

    denkbigrampatterns["denk"].append(patternoptional)

    print('+ + + + + + + +')
    print("pattern:",patternoptional)
    print('+ + + + + + + +')

    denkcorpusoriginal = copy.deepcopy(corpus_original)
    denknietcorpusoriginal = copy.deepcopy(corpus_original)
    denknietcorpusoriginal.filteronpatterns(denkbigrampatterns,{},prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)
    denkcorpusoriginal.filteronpatterns(denkpatterns,denkbigrampatterns,prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)


    print('# w/o bigram(s) in total w/o retweets:',len(denkcorpusoriginal.tweets))
    print('# with bigram(s) in total w/o retweets:',len(denknietcorpusoriginal.tweets))
    print('- - - - - - - - - - - - ')

    denkcorpus = copy.deepcopy(corpus_annotated)
    denknietcorpus = copy.deepcopy(corpus_annotated)
    denkcorpus.filteronpatterns(denkpatterns,denkbigrampatterns,prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)
    denknietcorpus.filteronpatterns(denkbigrampatterns,{},prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)

    nrannotated = {}
    nroriginal = {}
    nrannotated['sum'] = {}
    nroriginal['sum'] = {}
    nrannotated['sum']['w/o bigrams'] = 0
    nroriginal['sum']['w/o bigrams'] = 0
    nrannotated['sum']['with bigrams'] = 0
    nroriginal['sum']['with bigrams'] = 0
    polnr = {}
    notpolnr = {}
    sumpolnr = {}
    sumnotpolnr = {}
    sumpolnr['w/o bigrams'] = 0
    sumnotpolnr['w/o bigrams'] = 0
    sumpolnr['with bigrams'] = 0
    sumnotpolnr['with bigrams'] = 0

    # per day
    tweetdates = denkcorpus.gettweetdates()
    for tweetdate in sorted(tweetdates):
    #for tweetdate in sorted([datetime.date(2017,3,14)]):
        daycorpusannotatedfull = {}
        daycorpusoriginalfull = {}
        daycorpusannotated = {}
        daycorpusoriginal = {}
        nrannotated[tweetdate] = {}
        nroriginal[tweetdate] = {}
        try:
            print('date:',tweetdate.strftime("%d-%m"))
        except:
            print('date is ',tweetdate)
        print('-----------')

        daycorpusannotatedfull['w/o bigrams'] = denkcorpus.select_matchallfilters([('tweetdate',tweetdate)])
        nrnobigramannotationsfull = len(daycorpusannotatedfull['w/o bigrams'].tweets)
        daycorpusannotatedfull['with bigrams'] = denknietcorpus.select_matchallfilters([('tweetdate',tweetdate)])
        nronlybigramannotationsfull = len(daycorpusannotatedfull['with bigrams'].tweets)

        daycorpusoriginal['w/o bigrams'] = denkcorpusoriginal.select_matchallfilters([('tweetdate',tweetdate)])
        daycorpusoriginal['with bigrams'] = denknietcorpusoriginal.select_matchallfilters([('tweetdate',tweetdate)])
        nroriginal[tweetdate]['w/o bigrams'] = len(daycorpusoriginal['w/o bigrams'].tweets)
        nroriginal[tweetdate]['with bigrams'] = len(daycorpusoriginal['with bigrams'].tweets)
        nroriginal['sum']['w/o bigrams'] += nroriginal[tweetdate]['w/o bigrams']
        nroriginal['sum']['with bigrams'] += nroriginal[tweetdate]['with bigrams']

        (nronlybigramsannotations,nrnobigramsannotations) = VoxPopuli.computeproportionalamounts(nroriginal[tweetdate]['with bigrams'],nroriginal[tweetdate]['w/o bigrams'],nronlybigramannotationsfull,nrnobigramannotationsfull)

        print('\twith bigrams\tw/o bigrams')
        print('all\t\t',nroriginal[tweetdate]['with bigrams'],'\t',nroriginal[tweetdate]['w/o bigrams'])
        print('annotated\t',nronlybigramannotationsfull,'\t',nrnobigramannotationsfull)
        print('adapted\t\t',nronlybigramsannotations,'\t',nrnobigramsannotations)
        
        #print(nronlybigramsannotations, nrnobigramsannotations)
        daycorpusannotated['w/o bigrams'] = denkcorpus.select_matchallfilters([('tweetdate',tweetdate)])  #.part(nrnobigramsannotations)
        daycorpusannotated['with bigrams'] = denknietcorpus.select_matchallfilters([('tweetdate',tweetdate)])  #.part(nronlybigramsannotations)


        nrannotated[tweetdate]['w/o bigrams'] = len(daycorpusannotated['w/o bigrams'].tweets)
        nrannotated['sum']['w/o bigrams'] += nrannotated[tweetdate]['w/o bigrams']

        nrannotated[tweetdate]['with bigrams'] = len(daycorpusannotated['with bigrams'].tweets)
        nrannotated['sum']['with bigrams'] += nrannotated[tweetdate]['with bigrams']

        print('* * * * * * * * * * * * * * *')
        for bigramyesno,daycorpus in sorted(daycorpusannotated.items()):
            percsannotated = 0
            if nrannotated[tweetdate]['w/o bigrams'] + nrannotated[tweetdate]['with bigrams'] > 0:
                percsannotated = int(100 * nrannotated[tweetdate][bigramyesno] / (nrannotated[tweetdate]['w/o bigrams'] + nrannotated[tweetdate]['with bigrams']))
            percsoriginal = int(100 * nroriginal[tweetdate][bigramyesno] / (nroriginal[tweetdate]['w/o bigrams'] + nroriginal[tweetdate]['with bigrams']))

            (annotatorids,annotatorcombinations,nrannotations,values) = daycorpus.annotationsummary(['politiek'],decidingannotatorid='eric')
            polnr[bigramyesno] = 0
            notpolnr[bigramyesno] = 0
            if values:
                if '' in values['politiek']:
                    polnr[bigramyesno] = values['politiek']['']
                if 'neen' in values['politiek']:
                    notpolnr[bigramyesno] = values['politiek']['neen']

            sumpolnr[bigramyesno] += polnr[bigramyesno]
            sumnotpolnr[bigramyesno] += notpolnr[bigramyesno]

            print('\t\tannotated\tall')
            print(bigramyesno,'\t',polnr[bigramyesno]+notpolnr[bigramyesno],'\t',percsannotated,'%\t',nroriginal[tweetdate][bigramyesno],'\t', percsoriginal,'%')
            print('- - -')
            if polnr[bigramyesno] + notpolnr[bigramyesno] > 0:
                polperc = int(100 * polnr[bigramyesno] / (polnr[bigramyesno]+notpolnr[bigramyesno]))
                notpolperc = int(100 * notpolnr[bigramyesno] / (polnr[bigramyesno]+notpolnr[bigramyesno]))
                print('party','\t\t',polnr[bigramyesno],'\t',polperc,'%')
                print('verb ','\t\t',notpolnr[bigramyesno],'\t',notpolperc,'%')
            else:
                print('bleh')
            print('- - - - - - - - - - - - ')
            
        upparty = 0
        upverb = 0
        downparty = 0
        downverb = 0

        tokensets = daycorpusannotatedfull['w/o bigrams'].gettokensets(word='denk',decidingannotationfield='politiek',decidingannotatorid='eric')
        for (token,value) in tokensets:
            if token[0].isupper():
                if value == '':
                    upparty += 1
                else:
                    upverb += 1
            else:
                if value == '':
                    downparty += 1
                else:
                    downverb += 1

        print('upparty=',upparty)
        print('upverb=',upverb)
        print('downparty=',downparty)
        print('downverb=',downverb)
        print('- - - - - - - - - - - - ')

        tp=upparty
        fp=upverb
        fn=polnr['with bigrams']+downparty
        tn=notpolnr['with bigrams']+downverb
        precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
        print('predicted = party')
        print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
        print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))
        tn=upparty
        fn=upverb
        fp=polnr['with bigrams']+downparty
        tp=notpolnr['with bigrams']+downverb
        precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
        print('-')
        print('predicted = verb')
        print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
        print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))
        print('=========')


    print('All days')
    print('--------')
    for bigramyesno in (['w/o bigrams','with bigrams']):
        percsannotated = int(100 * nrannotated['sum'][bigramyesno] / (nrannotated['sum']['w/o bigrams'] + nrannotated['sum']['with bigrams']))
        percsoriginal = int(100 * nroriginal['sum'][bigramyesno] / (nroriginal['sum']['w/o bigrams'] + nroriginal['sum']['with bigrams']))

        print(bigramyesno,'\t',sumpolnr[bigramyesno]+sumnotpolnr[bigramyesno],'\t',percsannotated,'%\t',nroriginal['sum'][bigramyesno],'\t', percsoriginal,'%')
        if sumpolnr[bigramyesno] + sumnotpolnr[bigramyesno] > 0:
            polperc = int(100 * sumpolnr[bigramyesno] / (sumpolnr[bigramyesno]+sumnotpolnr[bigramyesno]))
            notpolperc = int(100 * sumnotpolnr[bigramyesno] / (sumpolnr[bigramyesno]+sumnotpolnr[bigramyesno]))
            print('party','\t\t',sumpolnr[bigramyesno],'\t',polperc,'%')
            print('verb ','\t\t',sumnotpolnr[bigramyesno],'\t',notpolperc,'%')
        else:
            print('bleh')
        print('- - - - - - - - - - - - ')

    upparty = 0
    upverb = 0
    downparty = 0
    downverb = 0

    tokensets = denkcorpus.gettokensets(word='denk',decidingannotationfield='politiek',decidingannotatorid='eric')
    for (token,value) in tokensets:
        if token[0].isupper():
            if value == '':
                upparty += 1
            else:
                upverb += 1
        else:
            if value == '':
                downparty += 1
            else:
                downverb += 1

    #print('BEGIN NEW PART')
    #tp = upparty
    #fp = upverb
    #fn = downparty
    #tn = downverb
    #precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
    #print('predicted = party')
    print('upparty=',upparty)
    print('upverb=',upverb)
    print('downparty=',downparty)
    print('downverb=',downverb)
    print('- - - - - - - - - - - - ')
    #print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
    #print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))

    #tn = upparty
    #fn = upverb
    #fp = downparty
    #tp = downverb
    #precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
    #print('predicted = verb')
    #print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
    #print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))
    #print('END NEW PART')

    tp=upparty
    fp=upverb
    fn=sumpolnr['with bigrams']+downparty
    tn=sumnotpolnr['with bigrams']+downverb
    precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
    print('predicted = party')
    print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
    print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))
    tn=upparty
    fn=upverb
    fp=sumpolnr['with bigrams']+downparty
    tp=sumnotpolnr['with bigrams']+downverb
    precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
    print('-')
    print('predicted = verb')
    print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
    print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))
    

