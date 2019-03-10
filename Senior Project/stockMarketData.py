#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:01:40 2019

@author: charlienash
"""

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.sectorperformance import SectorPerformances
import matplotlib.pyplot as plt
import sys
import twitter_credentials
import numpy as np
import pandas as pd
import datetime

def stockchart(symbol):
    ts = TimeSeries(key=twitter_credentials.STOCK_API, output_format='pandas')
    data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
    df = data
    df.to_csv("stockdata.csv", index = True)
    return df

#symbol= input("Enter symbol name:" )
#stockchart(symbol)