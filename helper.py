#!/usr/bin/python

import sys 
import pprint
import datetime

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
        return newDate.strftime("%Y-%m-%d")
    
#end class
