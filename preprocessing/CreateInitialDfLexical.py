# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:10:59 2019

@author: mazzi
"""

import pandas as pd
import numpy as np

# Load tweets datasets
df_tweets_1 = pd.read_json('dataset_tweets_2.json')
df_tweets_2 = pd.read_json('dataset_tweets_3.json')

# Load list of positive and negative words
positive_words = pd.read_csv('positive_words_2.txt',delimiter='\n',header=None,encoding='latin')
negative_words = pd.read_csv('negative_words_2.txt',delimiter='\n',header=None,encoding='latin')

# Load sentiment emoji dataset and select only the positive emojis
df_emoji = pd.read_csv('Emoji_Sentiment_Data_v1.0.csv')
df_emoji = df_emoji[df_emoji['Positive']>20]
df_emoji = df_emoji[df_emoji['Negative']>20]
df_emoji['positive_negative_rate'] = df_emoji['Positive']/(df_emoji['Positive']+df_emoji['Negative'])
positive_emoji = df_emoji[df_emoji['positive_negative_rate']>=0.9]['Emoji']

# Merge all tweets datasets
df_tweets = df_tweets_1.append(df_tweets_2)
# Lowercase all text
df_tweets.loc[:,'tweet']=df_tweets['tweet'].str.lower()
# Remove duplicates
df_tweets_unq = df_tweets.drop_duplicates(keep='first',subset=['tweet'])
# Remove some characters
df_tweets_unq['tweet']=df_tweets_unq['tweet'].str.replace(r"[.;:!\'?,@\"()\[\]]","")

# For emoji recognition, split every word to find single emojis
# (as people usually use several emojis) and assign a positive score
# for the tweets that have those positive emojis
all_sliced_words = df_tweets_unq['tweet'].str.lower().apply(list)
positive_emoji_score = []
for tweet in all_sliced_words:
    positive_emoji_score.append(positive_emoji.isin(tweet).sum())

# Split every word to be identified as positive or negative based on the list
# then, every tweet will be assign a score for having positive or negative words
split_words = df_tweets_unq['tweet'].str.lower().str.split()
positive_score = []
negative_score = []
for tweet in split_words:
    positive_score.append(positive_words[0].isin(tweet).sum())
    negative_score.append(negative_words[0].isin(tweet).sum())

# Create columns with the positive/negative counts
df_tweets_unq['positive_score'] = positive_score
df_tweets_unq['negative_score'] = negative_score
df_tweets_unq['positive_emoji_score'] = positive_emoji_score
df_tweets_unq.loc[df_tweets_unq['positive_emoji_score']>1]=1
# Sum the positive emoji and positive score (from words)
df_tweets_unq['positive_score']+=df_tweets_unq['positive_emoji_score']
# Normalize
df_tweets_unq['positive_score'] = df_tweets_unq['positive_score']/(df_tweets_unq['positive_score'].sum()/df_tweets_unq['negative_score'].sum())

# Get all tweet words
full_words = []
for words in split_words:
    full_words+=words

# Get the unique words for all tweets
unique_words = np.unique(full_words)

# Remove all positive and negative predefined words
unique_words_clean = list(set(unique_words)-set(positive_words[0].tolist())-set(negative_words[0].tolist()))
# Set with all words positive and negative words
dimension_words= list(set(unique_words)-set(unique_words_clean))
# Separate the positive and negative words
dimension_positive = list(set(dimension_words)-set(negative_words[0].tolist()))
dimension_negative = list(set(dimension_words)-set(dimension_positive))
# For pre-classified positive and negative words, assagin a totally positive/negative
# score
df_positive_words = pd.DataFrame({'word':dimension_positive})
positive_word_quantity = []
for word in df_positive_words['word']:
    positive_word_quantity.append(full_words.count(word))
df_positive_words['positive_score'] = positive_word_quantity
df_positive_words['negative_score'] = 0
    
df_negative_words = pd.DataFrame({'word':dimension_negative})
negative_word_quantity = []
for word in df_negative_words['word']:
    negative_word_quantity.append(full_words.count(word))
df_negative_words['positive_score'] = 0
df_negative_words['negative_score'] = negative_word_quantity

# Create a dictionary to track every word contained in tweet rows
dict_words = {}
idx_tweet = 0
for tweet in split_words:
    for word in tweet:
        if word in dict_words:
            dict_words[word].append(idx_tweet)
        else:
            dict_words[word]=[idx_tweet]   
    idx_tweet+=1

# Create a list for every word found on tweets. Each word is contained in a
# tweet, and every tweet has an associated positive and negative score.
# This loop will give to every word the sum of positive and negative scores
# of all tweets where the word was found.
# For example, if we are evaluating the word 'doggo'. This word was found in tweets like:
# "I love my doggo", "my doggo is great", "look this lovely doggo"
# These tweets have several positive words like love,great and lovely
# Therefore, "doggo" will have a higher positive score as it was associated with positive words.
list_polarity_words = []
for word in unique_words_clean:
    idxs = dict_words[word]
    word_positive_pol = df_tweets_unq.iloc[idxs]['positive_score'].sum()
    word_negative_pol = df_tweets_unq.iloc[idxs]['negative_score'].sum()
    list_polarity_words.append([word,word_positive_pol,word_negative_pol])

# Create a DataFrame for every word
df_polarity_words = pd.DataFrame(list_polarity_words,columns=['word','positive_score','negative_score'])
df_polarity_words = df_polarity_words.append(df_positive_words)
df_polarity_words = df_polarity_words.append(df_negative_words)
# Make words as index for faster search
df_polarity_words.index = df_polarity_words['word']

# Save word_polarity_df
df_polarity_words.to_json('polarity_df.json')
        
        
