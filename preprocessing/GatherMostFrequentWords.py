# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:31:53 2019

@author: mazzi
"""

# This algo will receive several tweets and store in a dataframe

import tweepy
import operator
import pandas as pd

consumer_key = 'YOUR_KEY_HERE'
consumer_key_secret = 'YOUR_KEY_HERE'
access_token = 'YOUR_TOKEN_HERE'
access_token_secret = 'YOUR_TOKEN_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

dict_word_count = {}

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status!="":
            words_list = status.text.split()
            for word in words_list:
                if word in dict_word_count:
                    dict_word_count[word]+=1
                else:
                    dict_word_count[word]=1
                

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track="a,o,e,vai,foi,sou,é,como,não,sim,você,vc,eu,como,eh,coisa,bom,ruim,viu,passou,caiu,andou,pq,porque,nós,nos,comprou,para,pra,fica",languages=['pt'])


sorted_x = sorted(dict_word_count.items(), key=operator.itemgetter(1))

list_500 = sorted_x[-501:]
# Delete first as it is RT
list_500 = list_500[:500]

df_500 = pd.DataFrame(list_500)
del df_500[1]

# This output contains the 500 most frequent words on twitter at the moment
# I let this code run for 30 minutes
df_500.to_excel('500_most_frequent_words_pt.xls',index=False,encoding='utf-32')


