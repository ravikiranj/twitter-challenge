twitter-challenge Install Guide
===============================
1) Install python (python 2.7.*)
************************************
sudo apt-get install python

2) Install python-setuptools
************************************
sudo apt-get install python-setuptools

3) Install tweepy library
************************************
sudo easy_install tweepy

4) Install Python YQL
************************************
sudo easy_install yql

5) Fetch Top 1000 user list sorted by follower count (optional, already prefetched)
***********************************************************************************
python getTopUsersByFollowers.py

6) Fetch 10 conversations in last 2 weeks b/w A & B such that A(followerCount) > 1 million and B(followerCount) > 125k
***********************************************************************************************************************
python getTweets.py

Since, conversations like above are sparse, we may hit Twitter API hourly rate limit of 350 requests per hour. In that case,
to quickly bypass it, use a different access_token by changing the credential file in "auth.py" (Line 12-19) and use a different
IP address. After making the changes, run the above command again and the program will resume from the saved state until it
finds 10 such coversations.

The output of the program is written to "result.txt" which consists of details of tweets T1 and T2. 

A detailed explanation of how the problem was solved is listed in "Solution.pdf"

7) Sample Output and Console Output
*************************************
The sample output of the program can be found in "result.txt" and the logged console output can be found in "consoleOutput.txt".
When API rate limit is reached, the state is saved in "currUserIndex.txt".


