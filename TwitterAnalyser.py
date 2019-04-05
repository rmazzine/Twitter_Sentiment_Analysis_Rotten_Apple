# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:36:44 2019

@author: mazzi
"""
import numpy as np

# Tweet classification
def evaluate_tweet(tweet,df_polarity_words):
    tweet_list = str(tweet).lower().split()
    positive_total = 0
    negative_total = 0
    # Total polarity
    total_polarity = df_polarity_words['positive_score']+df_polarity_words['negative_score']
    mean_polarity_non_zero = int(total_polarity[total_polarity>1].mean())
    list_scores = []
    for word in tweet_list:
        try:
            word_scores = df_polarity_words.loc[word]
            # The total_words_scores will be used to penalize words that did
            # not receive much scores, as there is more uncertainty if they
            # are positive or negative
            total_word_scores = int(word_scores['positive_score']+word_scores['negative_score'])
            if total_word_scores>mean_polarity_non_zero:
                total_word_scores=mean_polarity_non_zero
            word_positive_score = total_word_scores/mean_polarity_non_zero*int(word_scores['positive_score'])/(int(word_scores['positive_score'])+int(word_scores['negative_score']))+(mean_polarity_non_zero-total_word_scores)/mean_polarity_non_zero*0.5
            positive_total += word_positive_score
            negative_total += 1-word_positive_score
            list_scores.append(word_positive_score)
            list_scores.append(word_positive_score-1)
            
        except:
            positive_word = None
            negative_word = None
            n_tries=0
            n_less= 0
            while (positive_word is None) and (n_tries!=140):
                n_tries+=1
                n_less+=1
                try:
                    word_scores = df_polarity_words.loc[word[:-n_less]]
                    # The total_words_scores will be used to penalize words that did
                    # not receive much scores, as there is more uncertainty if they
                    # are positive or negative
                    total_word_scores = int(word_scores['positive_score']+word_scores['negative_score'])
                    if total_word_scores>mean_polarity_non_zero:
                        total_word_scores=mean_polarity_non_zero
                    word_positive_score = total_word_scores/mean_polarity_non_zero*int(word_scores['positive_score'])/(int(word_scores['positive_score'])+int(word_scores['negative_score']))+(mean_polarity_non_zero-total_word_scores)/mean_polarity_non_zero*0.5
                    positive_word = word_positive_score
                    negative_word = 1-word_positive_score
                    positive_total += positive_word
                    negative_total += negative_word
                    list_scores.append(word_positive_score)
                    list_scores.append(1-word_positive_score)
                    
                except:
                    pass
    # Calculate variance
    var = np.var(list_scores)
    
    # Learning\updating dataframe
    for word in tweet_list:
        # Try to assign if word exist in polarity df
        add_positive = positive_total/(positive_total+negative_total)
        add_negative = negative_total/(positive_total+negative_total)
        try:
            df_polarity_words.loc[word,'positive_score'] += add_positive
            df_polarity_words.loc[word,'negative_score'] += add_negative
        except:
            # The word does not exist in df
            df_polarity_words.loc[word]=[word,add_positive,add_negative]
                
    if positive_total>negative_total:
        emotion_tweet = "Positivo"
    elif positive_total<negative_total:
        emotion_tweet = "Negativo"
    else:
        emotion_tweet = "Mixed/Neutral"
        
    return(emotion_tweet,positive_total,negative_total,var)