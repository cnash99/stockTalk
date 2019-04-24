#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 21:44:57 2019

@author: charlienash
"""

import nltk
import csv
import datetime
import numpy as np
import pandas as pd
import re
from textblob import TextBlob
from twython import Twython
from nltk.corpus import stopwords
from dateutil import parser
from urlextract import URLExtract
 
def main(name):
    s = str(name)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    week_ago = datetime.datetime.utcnow()-datetime.timedelta(days = 7)
    
    APP_KEY = "2a9hn9IPMnqG47NcQi2DXYnvV"
    APP_SECRET = "YJLjqNfllHpknn3v5tTK2VpsP8kvVBPtuvYdBCn8Bf8YadWPOg"           
    ACCESS_TOKEN = "AAAAAAAAAAAAAAAAAAAAANrD9QAAAAAAa9GI6S884DtSyV0mMQzdP7VJq%2BI%3DEdKiIATJXO4E5t0vX7QpHS5S68kQM1DTpuYi4rGOIsIDiisg2g"
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    
    #Clear tweets.csv
    filename = "tweets.csv"
    f = open(filename, "w+")
    f.close()


    s = s + " -filter:retweets AND -filter:replies"
    search = twitter.search(q= s, lang = 'en', created_at = week_ago, result_type = 'mixed', count = 100)
    #print(search)
    tweets = search["statuses"]
    ids = []
    ids = [tweet['id_str'] for tweet in tweets]
    time = [tweet['created_at'] for tweet in tweets]
    texts = [tweet['text'] for tweet in tweets]
    times = [tweet['retweet_count'] for tweet in tweets]
    favtimes = [tweet['favorite_count'] for tweet in tweets]
    userName = [tweet['user']['screen_name'] for tweet in tweets]
    follower_count = [tweet['user']['followers_count'] for tweet in tweets]
    location = [tweet['user']['location'] for tweet in tweets]
    lang = [tweet['lang'] for tweet in tweets]
    url = [tweet['entities']['urls']for tweet in tweets]

    p1 = pd.DataFrame(
    {'id': ids,
     'date': time,
     'text': texts,
     'fav_count':favtimes,
     'retweet_count': times,
     'userName': userName,
     'follower_count':follower_count,
     'location':location,
     'lang':lang,
     'url':url
    })
    
    #Preprocess texts
    p1.loc[:,'rawText'] = p1.loc[:,'text']
    p1.loc[:,'text'] = p1.loc[:,'text'].apply(lambda x: x.lower())
    p1.loc[:,'text'] = p1.loc[:,'text'].apply(lambda x: x.replace('[^\w\s]',''))
    
    #Remove "stop words" from texts
    stop = stopwords.words('english')
    p1.loc[:,'text'] = p1.loc[:,'text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    
    #Analyze tweets for positive words and negative words and return totals
    p1.loc[:,'reaction'] = p1.loc[:,'text'].apply(lambda x: TextBlob(x))
    p1.loc[:,'reaction'] = p1.loc[:,'reaction'].apply(lambda x: x.sentiment[0])
    
    #One hot encode for Positive, Negative, Neutral
    p1.loc[:,'positive'] = p1.loc[:,'reaction'].apply(lambda x: 1 if x>0 else 0)  
    p1.loc[:,'negative'] = p1.loc[:,'reaction'].apply(lambda x: 1 if x<0 else 0)  
    p1.loc[:,'neutral'] = p1.loc[:,'reaction'].apply(lambda x: 1 if x==0 else 0)  

    #Parse rawText into just the urls
    i = 0
    rawTextSeries = p1.loc[:,'url']
    while(i < 10):
     row = p1.iloc[i,:]
     author = row.loc['userName']
     author = str(author)
     id1 = row.loc['id']
     id1 = str(id1)
     inp = 'https://twitframe.com/show?url=https%3A%2F%2Ftwitter.com%2F' + author + '%2Fstatus%2F' + id1
     rawTextSeries.iloc[i] = inp
     i = i+1
    p1.loc[:,'rawText'] = rawTextSeries
    p1.to_csv("tweets.csv", index=False) 