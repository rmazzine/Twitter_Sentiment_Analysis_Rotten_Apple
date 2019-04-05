# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 12:48:22 2019

@author: mazzi
"""

import pandas as pd
from AnalyseRTTwitter import tweet_analysis
from sklearn.metrics import accuracy_score

test_df = pd.read_excel('test_set_twitter_sentiment.xlsx')

result_list = []

for tweet in test_df.values:
    tweet_score = tweet_analysis(tweet[1],tweet[0])[4]
    if tweet_score >0:
        # Positive tweet
        result_list.append([1,tweet[2]])
    else:
        # Negative tweet
        result_list.append([0,tweet[2]])

result_df = pd.DataFrame(result_list,columns=['y_pred','y_real'])


acc_score = accuracy_score(result_df['y_real'],result_df['y_pred'])

print('The accuracy score of the system is {}%'.format(round(acc_score*100,2)))