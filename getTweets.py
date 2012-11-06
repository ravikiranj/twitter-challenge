#!/usr/bin/python

import sys 
import tweepy
from auth import getAPIHandle 
from helper import *


DEBUG = 0
apiHandle = getAPIHandle()
h = helper()

topUserList= h.getTopUserList()
twitter = apiHandle.getAPI()

twoWeeksAgo = h.getDateBeforeDays(14)
public_tweets = twitter.user_timeline(id=topUserList[0], since_id=twoWeeksAgo, count=100, page = 1)

count = 1
origUser = twitter.get_user(topUserList[0])
t1 = {'screenName' : '', 'userId' : '', 'followerCount' : 0,\
      'statusId' : '', 'createdAt' : 0, 'url': '', 'text' : '',\
      'toUserId' : '', 'toUserScreenName' : ''}
t1['screenName'] = origUser.screen_name
t1['userId'] = origUser.id
t1['followerCount'] = origUser.followers_count

for t in public_tweets:
    if(t.in_reply_to_status_id != None):
        t2 = {'screenName' : '', 'userId' : '', 'followerCount' : 0,\
              'statusId' : '', 'createdAt' : 0, 'url': '', 'text' : '',\
              'toUserId' : '', 'toUserScreenName' : ''}
              
        t1['statusId'] = t.id
        t1['text'] = t.text
        t1['createdAt'] = str(t.created_at)
        t1['toUserId'] = t.in_reply_to_user_id_str
        t1['toUserScreenName'] = t.in_reply_to_screen_name
        
        t2['userId'] = t.in_reply_to_user_id_str
        t2['statusId'] = t.in_reply_to_status_id
        t2['screenName'] = t.in_reply_to_screen_name
        
        if DEBUG:
            print "================================"
            print "Counter = %d" % (count)
            print "================================"
            print "Text = %s" % (t1['text'])
            print "In_Reply_To_Screen_Name = %s" % (t2['screenName'])
            print "In_Reply_To_Status_ID = %s" % (t1['statusId'])
            print "In_Reply_To_User_Id_Str = %s" % (t2['userId'])
            print "Created_At = %s" % (t1['createdAt'])
            
        origTweet = twitter.get_status(t2['statusId'])
        if(origTweet.in_reply_to_screen_name != None):
            t2['text'] = origTweet.text
            t2['followerCount'] = origTweet.author.followers_count
            t2['screenName'] = origTweet.author.screen_name
            t2['createdAt'] = str(origTweet.created_at)
            t2['toUserId'] = origUser.id 
            t2['toUserScreenName'] = origUser.screen_name
            
            t1['url'] = "https://twitter.com/" + t1['screenName'] + "/status/" + str(t1['statusId'])
            t2['url'] = "https://twitter.com/" + t2['screenName'] + "/status/" + str(t2['statusId'])
            
            if DEBUG:
                print "Orig Tweet = %s" % (t2['text'])
                print "Orig User = %s, Follower Count = %d" % (t2['screenName'], t2['followerCount'])
                
            if(t2['followerCount'] > 125000 and t1['followerCount'] > 1000000):
                print "================================"
                print "Counter = %d" % (count)
                print "================================"
                print "T1"
                print "==============="
                pprint.pprint(t1)
                
                print "T2"
                print "==============="
                pprint.pprint(t2)
                count += 1
    #end if
#end loop