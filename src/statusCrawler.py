# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:02:27 2017

@author: Thomas Hauptvogel
@Co-Author:Julian Striegl
"""

import tweepy
import json
import sys
from pymongo import MongoClient

consumer_key = '-Insert-Your-Consumer-Key-Here-'
consumer_secret = '-Insert-Your-Consumer-Secret-Here-'

access_token = '-Insert-Your-Access-Token-Here-'
access_token_secret = '-Insert-Your-Access-Token-Secret-Here-'

found_status = 0

#Authentication for the Tweepy Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,retry_count=3, timeout=1000, wait_on_rate_limit=True)

#Create a connection to your MongoDB database
dbClient = MongoClient('-Insert-MongoDB-Connection-String-Here-')
database = dbClient.mfdata

#Define your own Stream Listener
class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global found_status
        #Check if the found tweet has at least one hashtag
        if(len(status.entities.get('hashtags'))>0):
            #Count the found tweets in a global variable
            found_status = found_status + 1
            print(found_status)
            #Create a json string and put it in the database
            entry = json.dumps(status._json, ensure_ascii=False)
            database.tweetsUK.insert_one(json.loads(entry)).inserted_id
            #database.tweetsUSA.insert_one(json.loads(entry)).inserted_id

    def on_error(self, status_code):
        print(sys.stderr)
        print(status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr)
        return True # Don't kill the stream


#Create a listener for the streaming
sapi = tweepy.streaming.Stream(auth, CustomStreamListener())

#USA
#sapi.filter(locations=[-125.0011, 24.9493, -66.9326, 49.5904])

#United Kingdom
#Get tweets in the bounding box of the UK
sapi.filter(locations=[-14.02,49.67,2.09,61.06])