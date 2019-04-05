# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:29:13 2019

@author: mazzi
"""
from wordcloud import WordCloud
from base64 import b64encode
from io import BytesIO

def generate_wordcloud():
    # Read the whole text.
    text = open('1000tweets.txt',encoding='utf8').read()
    # Generate a word cloud image
    wordcloud = WordCloud(width=1024,height=480)
    wordcloud.generate(text)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer,format="JPEG")
    output_image = buffer.getvalue()   
    # Return b64 encoded image, this is way faster than creating an image
    return "data:image/jpeg;base64,"+str(b64encode(output_image))[2:-1]

