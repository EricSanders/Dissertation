#!/usr/bin/python

tweeters_100_200_list = []
tweeters_all_list = []

tweeters_100_200 = open("tweeters_100_200_ok.txt")
for line in tweeters_100_200:
    tweeters_100_200_list.append(line.rstrip())

tweeters_all = open("tweeters_ok.txt")
for line in tweeters_all:
    tweeters_all_list.append(line.rstrip())

for tweeter in (set(tweeters_all_list) - set(tweeters_100_200_list)):
    print(tweeter)
