#!/usr/bin/python
import yql
import re

#start getUsers
def getUsers(urlOffset):
    response = None
    y = yql.Public()
    env = "http://datatables.org/alltables.env"
    query = 'select * from html where url="http://twittercounter.com/pages/100/'+urlOffset+'" and xpath="/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]"'
    response = y.execute(query, env=env)
    if(response):
        return response.rows
    return response
#end getUsers

offset = 0
actualCount = 0
topUsersFileName = 'userList/topUsersNew.txt'
fh = open(topUsersFileName, 'w')
incr = 20
while(offset <= 990):
    response = None
    if(offset == 0):
        response = getUsers('')
    else:
        response = getUsers(str(offset))
    
    if(response):
        if(len(response) < 5):
            incr = 0 
            print "Failed to get results, retrying, fetched results = %d" % (len(response))
        else:
            incr = 20
            actualCount += len(response)
        for user in response:
            if(user['p']):
                uName = user['p']
                if(uName):
                    userName = re.sub('[\(\)\{\}<>]', '', uName)
                    fh.write(userName+"\n")
        #end for loop
    else:
        incr = 0
        print "Failed to get results, retrying, fetched results = 0"
        
    offset += incr
    print 'User Count = %d, Actual Count = %d' % (offset, actualCount)
#end while loop
print 'Done'