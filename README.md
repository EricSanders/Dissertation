# Dissertation
Scripts created for experiments that resulted in the dissertation 'VoxPopuli'

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

Chapter 2 - Forecasting Dutch Parliamentary Elections of 2012 (adapted from paper in DIR 2013)

Elections: 2012

Scripts:

UnzipTweetFiles.perl

unzips the files with the tweets from TwiNL and writes them to different location

MakePartyTweetSet.perl

write tweets per day and remove double tweets

CountParties.perl

reads the tweet files, finds and counts political parties

reads the poll numbers

computes and outputs percentages

CountWords.perl

makes list of all words in tweets per day sorted on frequency

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

Chapter 3 - Using Demographics to Optimise Forecasting (adapted from paper in SocInfo 2016)

Elections: 2012, 2015

Users2MySQL.py

reads file with all tweets, finds those with political parties and writes information about tweeter to mysql db

OtherTweets2MySQL.py

write tweets from tweeters in mysql db to mysql db

RemoveDoubleTweeters.py

remove tweeters with more than one entry from mysql db

FindExtinctTweeters.py

find tweeters that do not have a visible profile on Twitter (banned, removed, etc.) in mysql db

FindAndRemoveExtinctTweeters.py

find tweeters that do not have a visible profile on Twitter (banned, removed, etc.) in mysql db and remove those entries

GetAllAnnotations+TweetGenie.py

get the annotated demographics of tweeters and the tweetgenie demographics of tweeters

GetAllAnnotations+TweetGenie+Parties.py

get the annotated demographics of tweeters, the tweetgenie demographics of tweeters and the parties tweeters tweeted about

GetTweetGenie+Parties.py

get the tweetgenie demographics of tweeters and the parties tweeters tweeted about

GetOverlapAnnotations+TweetGenie.py

find tweeters annotated by several annotators and add tweetgenie demographics

GetTweeters4Genie.py

selects tweeters for which demographics are to be decided by tweetgenie

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

Chapter 4 - Using Communicative Intent to Optimise Forecasting (adapted from paper in LREC 2020)

Elections: 2011, 2012, 2015

potwan.py

module with objects used in these experiments, also on the django website for the annotation application

ComputeMAEs_parallel.py

computes (M)AE of all possible combinations with/without the features that were annotated

FindBestMAE.py

finds the feature combination that gives the best (M)AE for various minimal amounts of tweets

PoliticalTweets2MySQL_fromfile.py

get tweets from TwiNL files, filters on political parties and stores in mysql database

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

Chapter 5 - Real-time Forecasting Web Application

Elections: 2017 (and 2019)

getpartytweetsdeamon.py

reads tweets from file, selects tweets with partynames and stores in mysql database

keeps running, checks every so often for a new file to handle

scripts for the frontend of the website can be found on https://github.com/Woseseltops/stemming2017

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

Chapter 6 - Disambiguating Denk

VoxPopuli.py

module for reading and storing tweets, computing scores, etc.

QuollGridSearch.py

wrapper around Quoll pipeline (https://github.com/LanguageMachines/quoll) that goes through pipeline with combinations of parameters

denkbigrams.py

benbigrams.py

denkrulebasedbigrams.py

benrulebasedbigrams.py

denkrulebasedcapitals.py

benrulebasedcapitals.py

denkrulebased.py

benrulebased.py

create tweet sets and compute scores for different methods

quollgridsearch.py

call the wrapper based on parameters set in initiation file

quolltraintest.py

goes through pipeline, trains and test different features

potwan.py

main script of django website

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

Chapter 7 - Longitudinal Study (adapted from paper in SocInfo 2019)

Elections: 2011, 2012, 2015, 2017, 2019

readtweets_5LXions.py

reads tweet files, filters tweets with party names and stores these in new files

LXionresults.py

module file with functions for computing and printing results

5LXionsexperiments.py

compute (M)AEs of all possible configurations

getmaepercategory.py

computes the (M)AE of each parameter normalised over all other parameters

