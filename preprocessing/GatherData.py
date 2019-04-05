# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:31:53 2019

@author: mazzi
"""

# This algo will receive several tweets and store in a dataframe

import tweepy
import pandas as pd

# Read the file with the most common 500 words
common_words = pd.read_excel('500_most_frequent_words_pt.xls',encoding='utf-32')

consumer_key = 'YOUR_KEY_HERE'
consumer_key_secret = 'YOUR_KEY_HERE'
access_token = 'YOUR_TOKEN_HERE'
access_token_secret = 'YOUR_TOKEN_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


list_tweets = []

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        list_tweets.append([status.id,status.text])
        if len(list_tweets)%100==0:
            print(len(list_tweets))
        


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=common_words[0].astype(str)[:200].tolist(),languages=['pt'])

df_tweets = pd.DataFrame(list_tweets,columns=['id', 'tweet'])
# CSV or XLS did not work
df_tweets.to_json('dataset_tweets_3.json')