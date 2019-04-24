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
import re

import twitter_credentials
import twitter_API
import stockMarketData
import stockerAPI

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
#from iexfinance import Stock
#from iexfinance import get_historical_data

def getSymbols():
   company_table = pd.read_csv("file:///Users/charlienash/stockTalk/companylist.csv")
   stockSymbols = (company_table.loc[:, "Symbol"]).tolist()
   return stockSymbols


def run(name):
  #Clear csv files to start fresh
  # opening the file with w+ mode truncates the file
  f = open("tweets.csv", "w+")
  f.truncate()
  f.close()
  f = open("stockdata.csv", "w+")
  f.truncate()
  f.close()
  f = open("predictions.csv", "w+")
  f.truncate()
  f.close()


  company_table = pd.read_csv("file:///Users/charlienash/stockTalk/companylist.csv")
  today = datetime.datetime.today().strftime('%Y-%m-%d')
  week_ago = datetime.datetime.utcnow()-datetime.timedelta(days = 7)

  #------------------------------------------------Ask user to search for a company---------------------------------------
  print("Please enter the symbol of a NASDAQ company: ")
  symbol = str(name)
  symbol = re.sub("[,']",'',symbol)
  symbol = symbol.strip("[]")
  symbol = symbol.upper()
  print(symbol)
  try:
     companyRow = company_table.loc[:, "Symbol"] == symbol
     company = company_table.loc[companyRow, "Name"].item()
  except:
     print("Error: Symbol is not recognized. Please enter a valid NASDAQ trading symbol.")
     sys.exit()

  stock = stockerAPI.Stocker(symbol)
  #------------------------------------------------Populate Datasets-------------------------------------------------------
  twitter_API.main(company)

  #Read two input csv files
  tweets = pd.read_csv("tweets.csv")
  stockData = pd.read_csv("stockdata.csv")

  #Make dataframe of last week of stock data
  stockData.loc[:,'date'] = pd.to_datetime(stockData.loc[:,'date'])
  lastSeven = stockData.loc[:,'date'].map(lambda x: x>week_ago)
  stocksLastSeven = stockData.loc[lastSeven,:]

  #------------------------------------------------Create predictions-------------------------------------------------------
  stock.predict_future()

  #Collect data on tweet volume, percentage of positive tweets, and percentage of negative tweets
  totalVolume = tweets['id'].count()
  posTweets = tweets.loc[:,'positive'].sum()
  negTweets = tweets.loc[:, 'negative'].sum()
  percentPos = (posTweets/totalVolume)*100
  percentNeg = (negTweets/totalVolume)*100

  #Get data for predicting stock price
  lastIndex = stockData['date'].count()-1
  lastRow = stockData.iloc[lastIndex, :]
  currentPrice = lastRow.loc['4. close']

  #Adjust trend
  predictions = pd.read_csv("predictions.csv")
  diff = predictions.iloc[0, 3] - predictions.iloc[0, 1]
  predictions.loc[:, 'trend'] = predictions.loc[:, 'trend'].map(lambda x: x+diff)

  #Get data for predicting stock price
  estimate = predictions.loc[:, "estimate"]
  trend = predictions.loc[:, "trend"]
  change = predictions.loc[:, "change"]

  #------------------------------------------------Adjust estimates for Twitter data---------------------------------------
  overallPerception = (percentPos - percentNeg)/100
  if(overallPerception>0):
     predictions.loc[:, "twitter change"] = change.map(lambda x: x + abs(abs(x) * overallPerception*10))
  elif(overallPerception<0):
     predictions.loc[:, "twitter change"] = change.map(lambda x: x - abs(abs(x) * overallPerception))
  else:
     predictions.loc[:, "twitter change"] = 0

  #Find posTweetLikes & posTweetRT
  positiveTweets = tweets.loc[:, 'positive'].map(lambda x: x == 1)
  posTweetLikes = tweets.loc[positiveTweets,'fav_count'].sum()
  posTweetRT = tweets.loc[positiveTweets,'retweet_count'].sum()

  #Find negTweetLikes & negTweetRT
  negativeTweets = tweets.loc[:, 'negative'].map(lambda x: x == 1)
  negTweetLikes = tweets.loc[negativeTweets,'fav_count'].sum()
  negTweetRT = tweets.loc[negativeTweets,'retweet_count'].sum()

  #Find netLikes and netRT
  netLikes = posTweetLikes - negTweetLikes
  netRT = posTweetRT - negTweetRT

  predictions.loc[:, 'trend'] = predictions.loc[:, 'trend'] + (predictions.loc[:, 'twitter change'] - predictions.loc[:, 'change'])
  predictions.to_csv("predictions.csv", index=False)

  #------------------------------------------------Logic for advice-------------------------------------------------------
  predictions.loc[:,'percentChange'] = predictions.loc[:, 'trend'].map(lambda x: x/currentPrice)
  percentChange = predictions.loc[:,'percentChange'].tail(1).values[0]
  numPredictions = predictions.loc[:,'percentChange'].count()

  if(percentChange > 1.02):
     advice = 'buy more'
  elif(percentChange < .98):
     advice = 'sell your'
  else:
     advice = 'hold your'

  #------------------------------------------------Print Results-------------------------------------------------------
  percentPos = round(percentPos, 2)
  percentNeg = round(percentNeg, 2)
  predictedPrices = predictions.loc[:, "trend"]
  predictedPrices = predictedPrices.map(lambda x: round(x, 2))
  print("The current trading price of", company, "is", currentPrice, ".")
  print("There have been", totalVolume, "tweets about", company, "in the past week.")
  print("Of these tweets,", percentPos, "% speak about the company positively while", percentNeg, "% spoke negatively about the company.")
  print("Based on our predictions, the trading prices of", company, "over the next week will be: ")

  i = 0
  while(i<numPredictions):
     predictRow = predictions.iloc[i, :]
     d = predictRow['Date']
     p = predictRow['trend']
     print(d, ":", p)
     i = i+1

  if(numPredictions > 0):
     firstDayPredict = predictions.iloc[0, 0] + ": " + predictions.iloc[0,1].astype(str)
  else:
     firstDayPredict = ''
  if(numPredictions > 1):
     secondDayPredict = predictions.iloc[1, 0] + ": " + predictions.iloc[1,1].astype(str)
  else:
     secondDayPredict = ''
  if(numPredictions > 2):
     thirdDayPredict = predictions.iloc[2, 0] + ": " + predictions.iloc[2,1].astype(str)
  else:
     thirdDayPredict = ''
  if(numPredictions > 3):
     fourthDayPredict = predictions.iloc[3, 0] + ": " + predictions.iloc[3,1].astype(str)
  else:
     fourthDayPredict = ''
  if(numPredictions > 4):
     fifthDayPredict = predictions.iloc[4, 0] + ": " + predictions.iloc[4,1].astype(str)
  else:
     fifthDayPredict = ''
  if(numPredictions > 5):
     sixthDayPredict = predictions.iloc[5, 0] + ": " + predictions.iloc[5,1].astype(str)
  else:
     sixthDayPredict = ''
  if(numPredictions > 6):
     seventhDayPredict = predictions.iloc[6, 0] + ": " + predictions.iloc[6,1].astype(str)
  else:
     seventhDayPredict = ''

  if(advice == 'BUY MORE'):
     print("We suggest that you", advice, "more shares of this stock.")
  else:
     print("We suggest that you", advice, "your shares of this stock.")

  #------------------------------------------------Print graph-------------------------------------------------------
  graphDf1 = pd.DataFrame(columns = {'date', 'price'})
  graphDf1.loc[:, 'date'] = stocksLastSeven.loc[:, 'date']
  graphDf1.loc[:, 'price'] = stocksLastSeven.loc[:, '4. close']

  graphDf2 = predictions.loc[:, {'Date', 'trend'}]
  graphDf2.loc[:, 'price'] = predictions.loc[:, 'trend']
  graphDf2.loc[:, 'date'] = predictions.loc[:, 'Date']
  graphDf = graphDf1.append(graphDf2)

  plt.clf()
  plt.plot(graphDf.loc[:, 'date'], graphDf.loc[:, 'price']) 
  title = "Past Week's Date and Next Week's Predictions of " + company
  plt.title(title)
  plt.xlabel("Date")
  plt.ylabel("Trading Price")
#   plt.show()
  fileName = "static/graph.jpg"
  plt.savefig(fileName)

  displayTweets = tweets.iloc[0:10,9]
  displayTweets1 = displayTweets.iloc[0]
  displayTweets2 = displayTweets.iloc[1]
  displayTweets3 = displayTweets.iloc[2]
  displayTweets4 = displayTweets.iloc[3]
  displayTweets5 = displayTweets.iloc[4]
  displayTweets6 = displayTweets.iloc[5]
  displayTweets7 = displayTweets.iloc[6]
  displayTweets8 = displayTweets.iloc[7]
  displayTweets9 = displayTweets.iloc[8]
  displayTweets10 = displayTweets.iloc[9]

  return {'company' : company, 'currentPrice' : currentPrice, 'totalVolume' : totalVolume, 'percentPos': percentPos, 'percentNeg' : percentNeg, 'first' : firstDayPredict, 'second' : secondDayPredict, 'third' : thirdDayPredict, 'fourth' : fourthDayPredict, 'fifth' : fifthDayPredict, 'sixth' : sixthDayPredict, 'seventh' : seventhDayPredict, 'advice' : advice, 'displayTweets1' : displayTweets1, 'displayTweets2' : displayTweets2, 'displayTweets3' : displayTweets3, 'displayTweets4' : displayTweets4, 'displayTweets5' : displayTweets5, 'displayTweets6' : displayTweets6, 'displayTweets7' : displayTweets7, 'displayTweets8' : displayTweets8, 'displayTweets9' : displayTweets9, 'displayTweets10' : displayTweets10}