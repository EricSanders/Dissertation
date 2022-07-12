import VoxPopuli
from voxpopulivariables import *
import copy
import datetime
from collections import OrderedDict

benpatterns = {}
benpatterns["ben"] = ["ben"]

benbigrampatternsbasic = {}
benbigrampatternsbasic["ben"] = [
    'ik\\s+ben', #+ #candidate in bigram error = 26% #percentage bigrams = 9%
    'ben\\s+ik', #+ #candidate in bigram error = 18% #percentage bigrams = 4%
    'ben\\s+er', #+ #candidate in bigram error = 23% #percentage bigrams = 1%
    'ben\\s+benieuwd', #+ #candidate in bigram error = 11% #percentage bigrams = 1%
    'wat\\s+ben', #+ #candidate in bigram error = 18% #percentage bigrams = 0%
    'ben\\s+blij', #+ #candidate in bigram error = 5% #percentage bigrams = 0%
]
benbigrampatternsoptionaldummy = {}
benbigrampatternsoptionaldummy["ben"] = [
    'abcxyz'
    ]
benbigrampatternsoptional = {}
benbigrampatternsoptional["ben"] = [
    'ben\\s+je', #+ #candidate in bigram error = 37% #percentage bigrams = 2%
    'ben\\s+jij', #+ #candidate in bigram error = 31% #percentage bigrams = 1%
    'ben\\s+een', #+ #candidate in bigram error = 64% #percentage bigrams = 0%
    'ben\\s+zo', #+ #candidate in bigram error = 48% #percentage bigrams = 0%
    'ben\\s+echt', #+ #candidate in bigram error = 50% #percentage bigrams = 0%
    'ben\\s+niet', #+ #candidate in bigram error = 78% #percentage bigrams = 1%
    'dan\\s+ben', #+ #candidate in bigram error = 75% #percentage bigrams = 0%
    'ben\\s+op', #+ #candidate in bigram error = 84% #percentage bigrams = 0%
    'ben\\s+al', #+ #candidate in bigram error = 74% #percentage bigrams = 0%
    'ben\\s+ook', #+ #candidate in bigram error = 68% #percentage bigrams = 0%
    'en\\s+ben', #+ #candidate in bigram error = 80% #percentage bigrams = 0%
    'ben\\s+nu', #+ #candidate in bigram error = 54% #percentage bigrams = 0%
    'ben\\s+nog', #+ #candidate in bigram error = 73% #percentage bigrams = 0%
    'ben\\s+het', #+ #candidate in bigram error = 64% #percentage bigrams = 0%
    'maar\\s+ben', #+ #candidate in bigram error = 83% #percentage bigrams = 0%
    'ben\\s+geen', #+ #candidate in bigram error = 41% #percentage bigrams = 0%
]

    
prepattern='(\s|\.|,|;|:|!|\?|\@|\#|^)'
postpattern='(\s|\.|,|;|:|!|\?|$)'


# read original tweets
corpus_ben = VoxPopuli.TweetCorpusAnnotated()
corpus_ben.readmysql(db_ben_original,'tweetid', aliases = {'datetime': 'tweetdatetime'})
corpus_ben_noretweets = corpus_ben.select_matchallfilters([('retweettotweetid','NULL')])
nr_ben_original = len(corpus_ben_noretweets.tweets)

corpus_original = corpus_ben_noretweets

# read annotated tweets
corpus_ben.readmysql(db_ben_annotated,'tweetid','userid')
corpus_ben.removenunannotated(decidingannotatorid='eric')
corpus_ben.shuffle(seed=1)
nr_ben_annotated = len(corpus_ben.tweets)

print('\tben set\t(without retweets)')
print('all\t\t',nr_ben_original)
print('annotated\t',nr_ben_annotated)
print('+ + + + + + + +')
print('fixed patterns:')
for patternbasic in benbigrampatternsbasic["ben"]:
    print(patternbasic)


corpus_ben_annotated = corpus_ben
corpus_annotated = corpus_ben_annotated

for patternoptional in benbigrampatternsoptionaldummy["ben"]:
#for patternoptional in benbigrampatternsoptional["ben"]:
    benbigrampatterns = {}
    benbigrampatterns["ben"] = []
    
    for patternbasic in benbigrampatternsbasic["ben"]:
        benbigrampatterns["ben"].append(patternbasic)

    benbigrampatterns["ben"].append(patternoptional)

    print('+ + + + + + + +')
    print("pattern:",patternoptional)
    print('+ + + + + + + +')

    bencorpusoriginal = copy.deepcopy(corpus_original)
    bennietcorpusoriginal = copy.deepcopy(corpus_original)
    bennietcorpusoriginal.filteronpatterns(benbigrampatterns,{},prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)
    bencorpusoriginal.filteronpatterns(benpatterns,benbigrampatterns,prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)


    print('# w/o bigram(s) in total w/o retweets:',len(bencorpusoriginal.tweets))
    print('# with bigram(s) in total w/o retweets:',len(bennietcorpusoriginal.tweets))
    print('- - - - - - - - - - - - ')


    bencorpus = copy.deepcopy(corpus_annotated)
    bennietcorpus = copy.deepcopy(corpus_annotated)
    bencorpus.filteronpatterns(benpatterns,benbigrampatterns,prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)
    bennietcorpus.filteronpatterns(benbigrampatterns,{},prepattern,postpattern,ignorecase=True,applyprepostpattern=True,errorapplyprepostpattern=True,removemismatch=True)

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
    tweethours = bencorpus.gettweethours()
    for tweethour in sorted(tweethours):
    #for tweethour in sorted([hourtime.hour(2017,3,14)]):
        daycorpusannotatedfull = {}
        daycorpusoriginalfull = {}
        daycorpusannotated = {}
        daycorpusoriginal = {}
        nrannotated[tweethour] = {}
        nroriginal[tweethour] = {}
        try:
            print('hour:',tweethour.strftime("%H"))
        except:
            print('hour is ',tweethour)
        print('-----------')

        daycorpusannotatedfull['w/o bigrams'] = bencorpus.select_matchallfilters([('tweethour',tweethour)])
        nrnobigramannotationsfull = len(daycorpusannotatedfull['w/o bigrams'].tweets)
        daycorpusannotatedfull['with bigrams'] = bennietcorpus.select_matchallfilters([('tweethour',tweethour)])
        nronlybigramannotationsfull = len(daycorpusannotatedfull['with bigrams'].tweets)

        daycorpusoriginal['w/o bigrams'] = bencorpusoriginal.select_matchallfilters([('tweethour',tweethour)])
        daycorpusoriginal['with bigrams'] = bennietcorpusoriginal.select_matchallfilters([('tweethour',tweethour)])
        nroriginal[tweethour]['w/o bigrams'] = len(daycorpusoriginal['w/o bigrams'].tweets)
        nroriginal[tweethour]['with bigrams'] = len(daycorpusoriginal['with bigrams'].tweets)
        nroriginal['sum']['w/o bigrams'] += nroriginal[tweethour]['w/o bigrams']
        nroriginal['sum']['with bigrams'] += nroriginal[tweethour]['with bigrams']

        (nronlybigramsannotations,nrnobigramsannotations) = VoxPopuli.computeproportionalamounts(nroriginal[tweethour]['with bigrams'],nroriginal[tweethour]['w/o bigrams'],nronlybigramannotationsfull,nrnobigramannotationsfull)

        print('\twith bigrams\tw/o bigrams')
        print('all\t\t',nroriginal[tweethour]['with bigrams'],'\t',nroriginal[tweethour]['w/o bigrams'])
        print('annotated\t',nronlybigramannotationsfull,'\t',nrnobigramannotationsfull)
        #print('adapted\t\t',nronlybigramsannotations,'\t',nrnobigramsannotations)
        
        #print(nronlybigramsannotations, nrnobigramsannotations)
        daycorpusannotated['w/o bigrams'] = bencorpus.select_matchallfilters([('tweethour',tweethour)])  #.part(nrnobigramsannotations)
        daycorpusannotated['with bigrams'] = bennietcorpus.select_matchallfilters([('tweethour',tweethour)])  #.part(nronlybigramsannotations)


        nrannotated[tweethour]['w/o bigrams'] = len(daycorpusannotated['w/o bigrams'].tweets)
        nrannotated['sum']['w/o bigrams'] += nrannotated[tweethour]['w/o bigrams']

        nrannotated[tweethour]['with bigrams'] = len(daycorpusannotated['with bigrams'].tweets)
        nrannotated['sum']['with bigrams'] += nrannotated[tweethour]['with bigrams']

        print('* * * * * * * * * * * * * * *')
        for bigramyesno,daycorpus in sorted(daycorpusannotated.items()):
            percsannotated = float('nan')
            percsoriginal = float('nan')
            if nrannotated[tweethour]['w/o bigrams'] + nrannotated[tweethour]['with bigrams'] > 0:
                percsannotated = int(100 * nrannotated[tweethour][bigramyesno] / (nrannotated[tweethour]['w/o bigrams'] + nrannotated[tweethour]['with bigrams']))
            if nroriginal[tweethour]['w/o bigrams'] + nroriginal[tweethour]['with bigrams'] > 0:
                percsoriginal = int(100 * nroriginal[tweethour][bigramyesno] / (nroriginal[tweethour]['w/o bigrams'] + nroriginal[tweethour]['with bigrams']))

            (annotatorids,annotatorcombinations,nrannotations,values) = daycorpus.annotationsummary(['candidate'],decidingannotatorid='eric')
            polnr[bigramyesno] = 0
            notpolnr[bigramyesno] = 0
            if values:
                if '' in values['candidate']:
                    polnr[bigramyesno] = values['candidate']['']
                if 'neen' in values['candidate']:
                    notpolnr[bigramyesno] = values['candidate']['neen']

            sumpolnr[bigramyesno] += polnr[bigramyesno]
            sumnotpolnr[bigramyesno] += notpolnr[bigramyesno]

            print('\t\tannotated\tall')
            print(bigramyesno,'\t',polnr[bigramyesno]+notpolnr[bigramyesno],'\t',percsannotated,'%\t',nroriginal[tweethour][bigramyesno],'\t', percsoriginal,'%')
            print('- - -')
            if polnr[bigramyesno] + notpolnr[bigramyesno] > 0:
                polperc = int(100 * polnr[bigramyesno] / (polnr[bigramyesno]+notpolnr[bigramyesno]))
                notpolperc = int(100 * notpolnr[bigramyesno] / (polnr[bigramyesno]+notpolnr[bigramyesno]))
                print('candidate','\t\t',polnr[bigramyesno],'\t',polperc,'%')
                print('verb ','\t\t',notpolnr[bigramyesno],'\t',notpolperc,'%')
            else:
                print('bleh')
            print('- - - - - - - - - - - - ')
            
        upparty = 0
        upverb = 0
        downparty = 0
        downverb = 0

        tokensets = daycorpusannotated['w/o bigrams'].gettokensets(word='ben',decidingannotationfield='candidate',decidingannotatorid='eric')
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
        percsannotated = float('nan')
        percsoriginal = float('nan')
        if nrannotated['sum']['w/o bigrams'] + nrannotated['sum']['with bigrams'] > 0:
            percsannotated = int(100 * nrannotated['sum'][bigramyesno] / (nrannotated['sum']['w/o bigrams'] + nrannotated['sum']['with bigrams']))
        if nroriginal['sum']['w/o bigrams'] + nroriginal['sum']['with bigrams'] > 0:
            percsoriginal = int(100 * nroriginal['sum'][bigramyesno] / (nroriginal['sum']['w/o bigrams'] + nroriginal['sum']['with bigrams']))

        print(bigramyesno,'\t',sumpolnr[bigramyesno]+sumnotpolnr[bigramyesno],'\t',percsannotated,'%\t',nroriginal['sum'][bigramyesno],'\t', percsoriginal,'%')
        if sumpolnr[bigramyesno] + sumnotpolnr[bigramyesno] > 0:
            polperc = int(100 * sumpolnr[bigramyesno] / (sumpolnr[bigramyesno]+sumnotpolnr[bigramyesno]))
            notpolperc = int(100 * sumnotpolnr[bigramyesno] / (sumpolnr[bigramyesno]+sumnotpolnr[bigramyesno]))
            print('candidate','\t\t',sumpolnr[bigramyesno],'\t',polperc,'%')
            print('verb ','\t\t',sumnotpolnr[bigramyesno],'\t',notpolperc,'%')
        else:
            print('bleh')
        print('- - - - - - - - - - - - ')

    upparty = 0
    upverb = 0
    downparty = 0
    downverb = 0

    tokensets = bencorpus.gettokensets(word='ben',decidingannotationfield='candidate',decidingannotatorid='eric')
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
    

