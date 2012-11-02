#!/usr/bin/python

import sys 
import tweepy
from auth import getAPIHandle 


DEBUG = 0
apiHandle = getAPIHandle()

twitter = apiHandle.getAPI()

public_tweets = twitter.user_timeline()

for tweet in public_tweets:
    print tweet.text