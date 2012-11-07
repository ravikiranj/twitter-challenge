#!/usr/bin/python

import sys 
import pprint
import datetime
import re
import os

from datetime import timedelta

DEBUG = 0

#start helper
class helper:
    def __init__(self):
        self.topUserFileName = "userList/topUsers.txt"
        self.topUserList = []
        for line in open(self.topUserFileName, 'r'):
            line = line.rstrip()
            self.topUserList.append(line)

    def getTopUserList(self):
        return self.topUserList
    
    def getDateBeforeDays(self, num):
        currDate = datetime.datetime.now()
        dateDiff = timedelta(days =- num)
        newDate = currDate + dateDiff
        return newDate
    
    def getLastResultIndex(self, fileName):
        currIndex = 0
        if(os.path.exists(fileName)):
            for line in open(fileName, "r"):
                line = line.rstrip()
                if(re.match('Example = ', line)):
                    splitArr = line.split(' ')
                    if(len(splitArr) > 2):
                        newIndex = int(splitArr[2])
                        currIndex = newIndex
        return currIndex
    
    def checkCurrUserFileExists(self, fileName):
        if(os.path.exists(fileName)):
            #do nothing
            dummy = 1
        else:
            #create empty file
            open(fileName, 'w').close()
            
    def getCurrUser(self, fileName):
        currUser = ""
        if(os.path.exists(fileName)):
            cUser = open(fileName, "r") 
            currUser = cUser.read()
            currUser = currUser.rstrip()
            cUser.close()
        return currUser
#end class
