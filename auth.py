#!/usr/bin/python

import sys 
import pprint
import tweepy

DEBUG = 0

#start getAPIHandle
class getAPIHandle:
    def __init__(self):
        #Use different credentials if rate limit was hit and change IP
        #credFileName = "keys/credentials.key"
        credFileName = "keys/credentials2.key"
        #credFileName = "keys/credentials3.key"
        #credFileName = "keys/credentials4.key"
        #credFileName = "keys/credentials5.key"
        #credFileName = "keys/credentials6.key"
        #credFileName = "keys/credentials7.key"
        credFile = open(credFileName, "r")
        self.api = None

        cred = {}
        for line in credFile:
            splitArr = line.rstrip().split('=')
            if(len(splitArr) > 1): 
                key = splitArr[0].strip()
                value = splitArr[1].strip()
                cred[key] = value
                
        if(len(cred) < 4): 
            print "Error!! Could not find authentication details!!!"
            sys.exit(-1)
            
        if DEBUG:
            pprint.pprint(cred)
            
        consumer_key=cred['CONSUMER_KEY']
        consumer_secret=cred['CONSUMER_SECRET']

        access_token=cred['OAUTH_TOKEN']
        access_token_secret=cred['OAUTH_SECRET']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)
        
    def getAPI(self):
        return self.api
#end class
