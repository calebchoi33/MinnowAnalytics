import numpy as np
import pandas as pd
import streamlit as st

import csv
import math

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List
from LSTM import LSTMCalculate

def MAPE(real, fake):
    sum = 0
    for i in range(len(real)):
        sum += (real[i] - fake[i])/real[i]
    return float(sum) / float(len(real))

def RMSE(real, fake):
    sum = 0
    for i in range(len(real)):
        sum += pow((real[i] - fake[i]), 2)
    return math.sqrt(float(sum) / float(len(real)))

#stocks_csv: csv file string
#period: desired time period unit (day, week, month, year)
#trim: how many time periods starting from most recent to predict off of, -1 means use all data
#steps: how many predictions LSTM makes (3 steps means 3 time periods of predictions)
def predictor(stocks_csv, period, trim, steps):
    data = pd.read_csv('~/desktop/MinnowAnalytics/' + stocks_csv)
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df.Date)  
    if period == "Year":
        df = df.groupby([pd.Grouper(key='Date', freq='Y')])['Close'].median().reset_index(name = 'Price')
        delta = relativedelta(years = trim)
    elif period == "Month":
        df = df.groupby([pd.Grouper(key='Date', freq='M')])['Close'].median().reset_index(name = 'Price')
        delta = relativedelta(months = trim)
    elif period == "Week":
        df['Date'] -= pd.to_timedelta(7, unit='d')
        df = df.groupby([pd.Grouper(key='Date', freq='W')])['Close'].median().reset_index(name = 'Price')
        delta = timedelta(weeks = trim)
    else:
        df = df.sort_values(by = 'Date')
        delta = timedelta(days = trim)
    if trim != -1: 
        df = df.loc[df['Date'] > df['Date'].max() - delta]   
    dates = df['Date'].tolist()
    delta = delta/trim #get 1 period
    for i in range(steps):
        recentDate = dates[len(dates)-1]
        dates.append(recentDate + delta)
        
    price_guess = LSTMCalculate(df, steps)
    print(len(price_guess),steps)    
    df2 = pd.DataFrame(
    {'Date': dates,
     'Price': price_guess,
    })
    
    df2[len(df2)-1][1] = 150
    
    return df2
