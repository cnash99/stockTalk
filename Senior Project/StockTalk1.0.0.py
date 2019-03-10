#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 14:36:51 2019

@author: charlienash
"""
import datetime
from decimal import Decimal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

import twitter_credentials
import twitter_API
import stockMarketData

company_table = pd.read_csv("companylist.csv")
today = datetime.datetime.today().strftime('%Y-%m-%d')
week_ago = datetime.datetime.utcnow()-datetime.timedelta(days = 7)

#Ask user to search for a company
print("Please enter the symbol of a NASDAQ company: ")
symbol = str(input())
try:
    companyRow = company_table.loc[:, "Symbol"] == symbol
    company = company_table.loc[companyRow, "Name"].item()
except:
    print("Error: Symbol is not recognized. Please enter a valid NASDAQ trading symbol.")
    sys.exit()
    
#Populate tweets and stockData
twitter_API.main(company)
stockMarketData.stockchart(symbol)

#Read two input csv files
tweets = pd.read_csv("tweets.csv")
stocks = pd.read_csv("stockdata.csv")

#Make dataframe of last week of stock data
stocks.loc[:,'date'] = pd.to_datetime(stocks.loc[:,'date'])
lastSeven = stocks.loc[:,'date'].map(lambda x: x>week_ago)
stocksLastSeven = stocks.loc[lastSeven,:]

#Collect data on tweet volume, percentage of positive tweets, and percentage of negative tweets
totalVolume = tweets['id'].count()
posTweets = tweets.loc[:,'positive'].sum()
negTweets = tweets.loc[:, 'negative'].sum()
percentPos = (posTweets/totalVolume)*100
percentNeg = (negTweets/totalVolume)*100

#Get data for predicting stock price
lastIndex = stocks['date'].count()-1
lastRow = stocks.iloc[lastIndex, :]
currentPrice = lastRow.loc['4. close']
oneWeekLow = stocksLastSeven.loc[:, '4. close'].min()
oneWeekHigh = stocksLastSeven.loc[:, '4. close'].max()
distanceFromHigh = oneWeekHigh - currentPrice
distanceFromLow = currentPrice - oneWeekLow

#Predict predictedPrice
overallPerception= (percentPos - percentNeg)
if(overallPerception>0):
    change = distanceFromHigh*overallPerception
elif(overallPerception<0):
    change = distanceFromLow*overallPerception
else:
    change = 0
predictedPrice = currentPrice + change

#Logic for advice
percentChange = (predictedPrice-currentPrice)/currentPrice
if(percentChange > .05):
    advice = 'BUY'
elif(percentChange < -.05):
    advice = 'SELL'
else:
    advice = 'HOLD'

#Print Results
percentPos = round(percentPos, 2)
percentNeg = round(percentNeg, 2)
predictedPrice = round(predictedPrice, 2)
print("The current trading price of", company, "is", currentPrice, ".")
print("There have been", totalVolume, "tweets about", company, "in the past week.")
print("Of these tweets,", percentPos, "% speak about the company positively while", percentNeg, "% spoke negatively about the company.")
print("Based on our predictions, the trading price of", company, "will be", predictedPrice, "tomorrow.")
if(advice == 'BUY'):
    print("We suggest that you", advice, "more shares of this stock.")
else:
    print("We suggest that you", advice, "your shares of this stock.")
    