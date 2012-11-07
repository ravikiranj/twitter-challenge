#!/usr/bin/python

import sys 
import tweepy
from auth import getAPIHandle 
from helper import *

#DEBUG Flag
DEBUG = 0

#Get API Handle and Helper
apiHandle = getAPIHandle()
twitter = apiHandle.getAPI()
h = helper()

#Get Top User List from file
topUserList= h.getTopUserList()

#For each top user, get 100 status messages posted by user (will look for more if ten not found)
for topUser in topUserList:
    public_tweets = twitter.mentions(id=topUser)
    for t in public_tweets:
        print t.__dict__
    break