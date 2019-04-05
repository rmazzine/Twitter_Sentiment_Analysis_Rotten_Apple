# Twitter Sentiment Analysis PT BR - ROTTEN APPLE ALGORITHM

This repository has a python DASH dashboard application for a real time Twitter sentiment analysis using a simple real time learning classification algorithm that I called rotten apple. 


# Files

 - dashboardApp.py
	 - This is the main application file. It uses the python [DASH dashboard library](https://plot.ly/products/dash/) with [Flask](http://flask.pocoo.org/) to create a iterative dashboard that show tweets and statistics. 
 - AnalyseRTTwitter.py
	 - This file uses the [Tweepy](http://www.tweepy.org/) library to get tweets. There are two main functions: get_twitter_buffer - it gets 10 last tweets with a specific query and tweet_analysis that process the tweet using the classification algorithm on TwitterAnalyser file and return a list with tweet data and scores.
 - TwitterAnalyser.py
	 - It has the tweet classification algorithm that I called rotten apple. Bellow I explain more the logic behind this algorithm, but it has only one main function, evaluate_tweet, that evaluate a tweet based on a DataFrame with words and its polarity score.
 - TwitterWordcloudGen.py
	 - This file only has one function that generates a wordcloud image using the [WordCloud package](https://github.com/amueller/word_cloud). It transforms the image to a Base64 file that will be exhibited on the dashboard.

On the preprocessing folder, we have other files that were used to gather tweets and to create the polarity DataFrame.

 - preprocessing/GatherMostFrequentWords.py
	 - This is a simple file that gather several tweets and outputs the 500 most frequent words. This will be used on preprocessing/GatherData.py code to use as a search query (this way we expect to get the most general tweets as possible).
 - preprocessing/GatherData.py
	 - This file was used to gather tweet data. I took around 1 000 000 tweets (which 600 000 were unique).
 - preprocessing/CreateInitialDfLexical.py
	 - This code created the base DataFrame which basically has three columns:
		 -  **WORD** - which contains a unique word (or character/emoji/etc..)
		 - **POSITIVE_SCORE** - This is the positive polarity of the word, the score ranges from 0 to 1
		 - **NEGATIVE_SCORE** - It is simply the 1-positive_score. It could be omitted, but I left for a better code reading/interpretation. 

# The ROTTEN APPLE CLASSIFICATION ALGORITHM
## Motivation

One of the biggest challenges when building building an emotion classifier in an environment like Twitter is the fact tweets do not use regular/formal words, there is an intense use of emotes, ASCII art and expressions. These new ways of expression are highly dynamic and requires an algorithm that can actively work understanding them.

A additional problem when building these type of classifier for Portuguese is the lack of packages,training/testing data in Portuguese (~~ironic to say that in English ¯\_(ツ)_/¯~~). Most of classifiers found on Git-Hub were based on English classification libraries associated with translation packages, this obviously can lead to many errors (not only because misspelled words that will be hardly correctly translated, but there are many words and expressions (like emojis) [that can have a different meaning in different cultures/locales](https://www.daytranslations.com/blog/2018/02/how-emojis-are-perceived-differently-by-different-cultures-10690/).

Therefore, having all these problems in mind I build an algorithm called Rotten Apple. The name is related to a very famous proverb - ***A rotten apple spoils the barrel*** -. In my algorithm the rotten apples were [pre-defined negative or positive words](https://www.ppgia.pucpr.br/~paraiso/mineracaodeemocoes/recursos/barbara_martinazzo_versaofinal.pdf) (like lindo:positive / péssimo:negative) and [emojis](https://www.clarin.si/repository/xmlui/handle/11356/1048). These words (apples) were used to "spoil" other words that were not classified. Therefore, in my logic, when a word is constantly associated with a bad word, it may be a bad word too. If the word is neutral (like very/muito(a)) it may have a similar positive and negative score.

This makes this algorithm highly flexible to classify new words/expressions and the possibility to train in real time (as new classified tweets can assign updated scores to the words). This algorithm **do not** depends of training data, it is an unsupervised classification that only uses positive/negative words to create the initial word dataset.

Finally, I want to highlight this algorithm could be improved with mathematical modelling in the word classification process (assign or updating the polarity score) or in the tweet classification process*.

* For example: There are intensity modulation words like "very" that can increase (or decrease) the polarity of a word. This fact could be used for a better tweet classification process.

## Accuracy report
-   What metric are you using? Why ?
		- To check the algorithm performance, 100 random tweets were manually classified as more positive or more negative. As Twitter has a negative bias, I used F1 score as metric.
-   Which type of test did you choose ?
	- I did a "benchmark" test, where I ran my algorithm to classify the testing data.
-   Include the test dataset.
	- It is on preprocessing folder.

## Generating the classification score

To classify a tweet, each tweet word/emoji/expression separated by a space is analysed and assigned a score. The tweet score is the sum of all characters positive scores minus the negative score of all them. To classify a tweet as positive, I defined a threshold of tweet_total_score>=0.1, a negative tweet has the threshold of <=-0.2.  

## Neutral and Mixed classifications

Tweets that have a score higher than -0.2 and lower than 0.1 can be of two types. If all words used in the phrase are not highly polar (so, they are commonly used in positive or negative phrases) the tweet will have a low word variance, so I suppose these tweets could be classified as neutral, therefore we defined a threshold of variance<0.25. If the tweet use both polar negative and negative words, this can lead a low tweet polarity score but a high variance, for those tweets, with a variance threshold >= 0.25 we defined as mixed. 
