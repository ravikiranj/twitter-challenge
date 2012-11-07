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

#Generate date for 2 weeks ago
twoWeeksAgo = h.getDateBeforeDays(14)
#Conversation Counter
converseCount = 1
#Exit Flag
exitFlag = 0
#maxCount
maxCount = 10 

#Write results to file
#Get existing conversation count in result file
lastResultIndex = h.getLastResultIndex("result.txt")

#override conversation counter
converseCount = lastResultIndex + 1
resultFileName = "result.txt"
currUserIndexFileName = "currUserIndex.txt"

#Result file
result = open(resultFileName, "a")
#Store current user being processed so that we can resume
#from this user once twitter rate limit is hit (350 per hr)
h.checkCurrUserIndexFileExists(currUserIndexFileName)
currUserIndex = h.getCurrUserIndex(currUserIndexFileName)

writeCurrUser = open(currUserIndexFileName, "w")

#skip ladygaga [she replies loyally to all her unknown fans :)]
skipGaga = 1

#For each top user, get 100 status messages posted by user (will look for more if ten not found)
for topUser in topUserList:
    #Skip ladygaga
    if(skipGaga == 1 and topUser == "@ladygaga"):
        continue

    topUserIndex = topUserList.index(topUser)
    exceptionFlag = 0
    
    #Skip if user already been processed -> workaround for resuming after twitter rate limit has exceeded
    if(currUserIndex > topUserIndex):
        continue
        
    try:
        #twitter allows 'since' param, but tweepy does not, so do a manual check for twoWeeksAgo condition
        public_tweets = twitter.user_timeline(id=topUser, count=100, page = 1)
        origUser = twitter.get_user(topUser)
    except tweepy.TweepError, e:
        print "Exception = %s" % (e)
        if(hasattr(e, 'response') and hasattr(e.response, 'status') and \
           (e.response.status == 400 or e.response.status == 401)):
            #Exit -> Rate limit exceeded or bad request
            writeCurrUser.write(str(topUserIndex))
            writeCurrUser.close()
            result.close()
            print "HTTP Status Code = %d" % (e.response.status)
            print "Intermediate result written to %s, please resume after an hour if rate limit was exceeded or use different credentials (modify auth.py)" % (resultFileName)
            sys.exit(1)
        else:
            #Sometimes resources were not found or lacked permission to fetch protected account, skip these
            exceptionFlag = 1
            pass
        
    print "Current User = %s, Rank = %d, No. of followers = %d" % (origUser.screen_name, topUserIndex+1, origUser.followers_count)   
    #Update current user on console immediately
    sys.stdout.flush()
    
    if(exceptionFlag):
        continue
    
    #Fill top user details
    t1 = {}
    t1['screenName'] = origUser.screen_name
    t1['userId'] = origUser.id
    t1['followerCount'] = origUser.followers_count
    
    for t in public_tweets:
        exceptionFlag = 0
        #Proceed if status message was in reply to someone else's tweet
        if(t.in_reply_to_status_id != None):
            t1['statusId'] = t.id
            t1['text'] = t.text
            t1['createdAt'] = str(t.created_at)
            t1['toUserId'] = t.in_reply_to_user_id_str
            t1['toUserScreenName'] = t.in_reply_to_screen_name
            t1['creationTime'] = t.created_at
            
            #Check if the tweet was within last 2 weeks
            if(twoWeeksAgo > t1['creationTime']):
                continue
            
            #Get info of the second user
            t2 = {}
            t2['userId'] = t.in_reply_to_user_id_str
            t2['statusId'] = t.in_reply_to_status_id
            t2['screenName'] = t.in_reply_to_screen_name
            
            #Get original tweet
            try:
                origTweet = twitter.get_status(t2['statusId'])
            except tweepy.TweepError, e:
                print "Exception = %s" % (e)
                if(hasattr(e, 'response') and hasattr(e.response, 'status') \
                   and (e.response.status == 400 or e.response.status == 401)):
                    #Exit -> Rate limit exceeded or bad request
                    #Get next user
                    if(topUserIndex < len(topUserList)-1):
                        topUserIndex += 1
                    writeCurrUser.write(str(topUserIndex))
                    writeCurrUser.close()
                    result.close()
                    print "HTTP Status Code = %d" % (e.response.status)
                    print "Intermediate result written to %s, please resume after an hour if rate limit was exceeded or use different credentials (modify auth.py)" % (resultFileName)
                    sys.exit(1)
                else:
                    #Sometimes resources were not found or lacked permission to fetch protected account, skip these
                    exceptionFlag = 1
                    pass
            
            if(exceptionFlag):
                continue
            
            #Get info of original tweet for which t1 was a reply
            if(origTweet.in_reply_to_screen_name != None):
                #Fill tweet T2 details
                t2['text'] = origTweet.text
                t2['followerCount'] = origTweet.author.followers_count
                t2['screenName'] = origTweet.author.screen_name
                t2['createdAt'] = str(origTweet.created_at)
                t2['creationTime'] = origTweet.created_at
                t2['toUserId'] = origUser.id 
                t2['toUserScreenName'] = origUser.screen_name
                
                #Check if the tweet was within last 2 weeks
                if(twoWeeksAgo > t2['creationTime']):
                    continue
                
                t1['url'] = "https://twitter.com/" + t1['screenName'] + "/status/" + str(t1['statusId'])
                t2['url'] = "https://twitter.com/" + t2['screenName'] + "/status/" + str(t2['statusId'])
                
                #Check if T2 User's (B) follower count > 125k and T1 User's (A) follower count > 1 million
                if(t2['followerCount'] > 125000 and t1['followerCount'] > 1000000):
                    #Print the conversation if condition satisfied
                    result.write("================================\n")
                    result.write("Example No = %d\n" % (converseCount))
                    result.write("================================\n")
                    result.write("T1\n")
                    result.write("================================\n")
                    pprint.pprint(t1, result)
                    
                    result.write("================================\n")
                    result.write("T2\n")
                    result.write("================================\n")
                    pprint.pprint(t2, result)
                    #Newline
                    result.write("\n")
                    #Flush the file so that tail -f can pickup output
                    result.flush()
                    #Increment conversation counter
                    converseCount += 1
                    #Exit inner loop if maxCount conversations found and set exitFlag = 1
                    if(converseCount > maxCount):
                        exitFlag = 1
                        break
        #end if
    #end inner loop
    #Exit outer loop if 10 conversations found
    if(exitFlag):
        break
#end outer loop
print "Successfully found %d conversations" % (maxCount)
print "Output written to %s" % (resultFileName)
print "Done"
#Save current user
if(topUserIndex < len(topUserList)-1):
    topUserIndex += 1
writeCurrUser.write(str(topUserIndex))
writeCurrUser.close()
result.close()
