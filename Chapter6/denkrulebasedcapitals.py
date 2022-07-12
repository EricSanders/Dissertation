import VoxPopuli
from voxpopulivariables import *
import datetime
    
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

#print('\tdenkniet set\tdenk set\t(without retweets)')
#print('all\t\t',nr_denkniet_original,'\t',nr_denk_original)
#print('annotated\t',nr_denkniet_annotated,'\t',nr_denk_annotated)
#print('adapted\t\t',nr_denkniet_annotated_adapted,'\t',nr_denk_annotated_adapted)



corpus_denk_annotated = corpus_denk.part(nr_denk_annotated_adapted)
corpus_denkniet_annotated = corpus_denkniet.part(nr_denkniet_annotated_adapted)
corpus_annotated = corpus_denk_annotated + corpus_denkniet_annotated

dates = [('tweetdate',datetime.date(2017,3,14))]
corpus_annotated_14 = corpus_annotated.select_matchanyfilter(dates)

upparty = 0
upverb = 0
downparty = 0
downverb = 0

tokensets = corpus_annotated_14.gettokensets(word='denk',decidingannotationfield='politiek',decidingannotatorid='eric')
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

tp = upparty
fp = upverb
fn = downparty
tn = downverb
precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
print('predicted = party')
print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))

tn = upparty
fn = upverb
fp = downparty
tp = downverb
precision,recall,f1 = VoxPopuli.computescores(tp=tp,fp=fp,fn=fn,tn=tn)
print('predicted = verb')
print('tp=',tp,'fp=',fp,'fn=',fn,'tn=',tn)
print('precision = %.2f, recall = %.2f, f1 = %.2f' % (precision,recall,f1))
