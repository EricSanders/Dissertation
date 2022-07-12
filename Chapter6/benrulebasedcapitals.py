import VoxPopuli
from voxpopulivariables import *
import datetime
    
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

#print('\tben set\t(without retweets)')
#print('all\t\t',nr_ben_original)
#print('annotated\t',nr_ben_annotated)
#print('+ + + + + + + +')
#print('fixed patterns:')

corpus_ben_annotated = corpus_ben
corpus_annotated = corpus_ben_annotated

hours = [('tweethour',22)]
corpus_annotated_22 = corpus_annotated.select_matchanyfilter(hours)

upparty = 0
upverb = 0
downparty = 0
downverb = 0

tokensets = corpus_annotated_22.gettokensets(word='ben',decidingannotationfield='candidate',decidingannotatorid='eric')
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
