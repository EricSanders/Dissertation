import os
import subprocess
import re

# [IO]
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170301-20170313.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170301-20170313.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170312-20170313.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170312-20170313.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170313.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170313.labels'
traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170313-25.txt'
trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170313-25.labels'
testinputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170314.txt'
testlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_20170314.labels'

#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170301-20170313.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170301-20170313.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170308-20170313.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170308-20170313.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170311-20170313.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170311-20170313.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170313.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170313.labels'
#testinputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170314.txt'
#testlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/TweetSets/denktweets_best11_nobigrams_20170314.labels'
startoutputdir = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/DenkResults/Outputs/Report'

#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_best6_nobigrams_19-21.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_best6_nobigrams_19-21.labels'
#testinputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_best6_nobigrams_22.txt'
#testlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_best6_nobigrams_22.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_19-21.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_19-21.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_20-21.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_20-21.labels'
#traininputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_21.txt'
#trainlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_21.labels'
#testinputfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_22.txt'
#testlabelsfile = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/TweetSets/bentweets_22.labels'
#startoutputdir = '/vol/tensusers2/esanders/VoxPopuli/DenkBen/BenResults/Outputs/Report'

# [Features]
featuretypes = 'tokens'
ngramsize = '1_2'
#ngramsizes = ['1','2','3','5','1_2','1_2_3','2_3','1_2_3_4_5']
minimum_token_frequency = '1'
#minimumtokenfrequencies = [1,5,25]
module_featurize = 'quoll.classification_pipeline.modules.featurize'
frogconfig = '/vol/customopt/lamachine16.dev/share/frog/nld/frog.cfg'

# [Classification]
#classifiermethods = ['naive_bayes','knn','svm','logistic_regression','tree','perceptron']
classifiermethod = 'svm'
classifier_args = '/home/esanders/Twitter/Dissertatie/scripts/no_args.txt'
balance = '--balance'
#weightmethods = ['binary','frequency','tfidf']
weightmethod = 'binary'
#prunenumbers = [100,1000,10000,100000,999999999]
prunenumber = '100000'
module_report = 'quoll.classification_pipeline.modules.report'
#targets = ['politiek_','politiek_neen']

traininputfilebasename = os.path.basename(traininputfile)
traininputfilebasenamenoext = os.path.splitext(traininputfilebasename)[0]
testinputfilebasename = os.path.basename(testinputfile)
testinputfilebasenamenoext = os.path.splitext(testinputfilebasename)[0]

outputdir = startoutputdir + '/' + traininputfilebasenamenoext + '_' + testinputfilebasenamenoext

trainoutputfilename = outputdir + '/' + traininputfilebasenamenoext
#trainfeatures = trainoutputfilename + '.' + featuretypes + '.n_' + ngramsize + '.min' + minimum_token_frequency + '.lower_False.black_false.features.npz' 
trainfeatures = trainoutputfilename + '.features.npz' 
testoutputfilename = outputdir + '/' + testinputfilebasenamenoext
#testfeatures = testoutputfilename + '.' + featuretypes + '.n_' + ngramsize + '.min' + minimum_token_frequency + '.lower_False.black_false.features.npz' 
testfeatures = testoutputfilename + '.features.npz' 

if not os.path.exists(outputdir):
    os.makedirs(outputdir)

os.chdir(outputdir)

command = 'ln -s '+ traininputfile + ' .'
commandlist = command.split(" ")
print(commandlist)
subprocess.run(commandlist)

command = 'ln -s '+ testinputfile + ' .'
commandlist = command.split(" ")
print(commandlist)
subprocess.run(commandlist)

# train features
command = 'luiginlp Featurize --module ' + module_featurize + ' --inputfile ' + traininputfilebasename + ' --ngrams ' + ngramsize + ' --minimum-token-frequency ' + minimum_token_frequency + ' --featuretypes ' + featuretypes + ' --frogconfig ' + frogconfig
#commandlist = command.split(" ")
commandlist = []
commandlisttmp = command.split(" ")
for commandpart in commandlisttmp:
    commandpart = re.sub("(\d)_(?=\d)",r"\1 ",commandpart)
    commandlist.append(commandpart)
print(commandlist)
subprocess.run(commandlist)

# test features
command = 'luiginlp Featurize --module ' + module_featurize + ' --inputfile ' + testinputfilebasename + ' --ngrams ' + ngramsize + ' --minimum-token-frequency ' + minimum_token_frequency + ' --featuretypes ' + featuretypes + ' --frogconfig ' + frogconfig
#commandlist = command.split(" ")
commandlist = []
commandlisttmp = command.split(" ")
for commandpart in commandlisttmp:
    commandpart = re.sub("(\d)_(?=\d)",r"\1 ",commandpart)
    commandlist.append(commandpart)
print(commandlist)
subprocess.run(commandlist)

# testing
command = 'luiginlp Report --module ' + module_report + ' --train ' + trainfeatures + ' --test ' + testfeatures + ' --trainlabels ' + trainlabelsfile + ' --testlabels ' + testlabelsfile + ' --testdocs ' + testinputfilebasename + ' --classifier ' + classifiermethod + ' --weight ' + weightmethod + ' --prune ' + prunenumber
commandlist = command.split(" ")
print(commandlist)
subprocess.run(commandlist)
