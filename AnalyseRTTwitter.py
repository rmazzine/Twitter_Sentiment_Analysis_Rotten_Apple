# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:31:53 2019

@author: mazzi
"""

# This algo will receive several tweets and store in a dataframe

import tweepy
import pandas as pd
import re
import time
import os
from TwitterAnalyser import evaluate_tweet

df = pd.read_json('polarity_df.json')

consumer_key = 'YOUR_KEY_HERE'
consumer_key_secret = 'YOUR_KEY_HERE'
access_token = 'YOUR_TOKEN_HERE'
access_token_secret = 'YOUR_TOKEN_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def tweet_analysis(tweet_text,tweet_id):
    text = re.sub("[.;:!\'?,@\"()\[\]]","",tweet_text)
    score = evaluate_tweet(text,df)
    if os.path.getsize("1000tweets.txt")<1000000:
        open('1000tweets.txt','a',encoding='utf8').write(' '+text+' ')
    
    return [tweet_id,tweet_text,score[1],score[2],score[1]-score[2],score[3]]



list_buffer = []

class MyStreamListener(tweepy.StreamListener):
    
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.output_buffer = []
        super(MyStreamListener, self).__init__()
        


    def on_status(self, status):
        global list_buffer
        tweet_id, tweet_text = [status.id,status.text]
        if len(list_buffer)==10:
            list_buffer.append([tweet_id,tweet_text])
            self.output_buffer = list_buffer
            list_buffer = []
            myStream.disconnect()
            pass
        else:
            list_buffer.append([tweet_id,tweet_text])

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

def get_twitter_buffer(query=['twitter']):
    myStream.filter(track=query,languages=['pt'])
    return pd.DataFrame(myStreamListener.output_buffer,columns=['id','tweet'])



            
