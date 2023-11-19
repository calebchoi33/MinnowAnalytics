import numpy as np
from typing import List

def EMACalculate(stocks): #matrix
    k = 2/(len(stocks[0])+1)
    EMA = 0
    prev_EMA = 0
    
    prediction = stocks
    for i in range(len(stocks[1])+29):
        EMA = stocks[1][i-1] * k + prev_EMA * (1-k)
        prev_EMA = EMA
        prediction[i] = prev_EMA
        
        
    #try this one, starts predicting from 30 days ago    
    prediction = []
    for i in range(len(stocks)-29,len(stocks)):
        EMA = stocks["cost"][i] * k + prev_EMA * (1-k)
        prev_EMA = EMA
        prediction.append(prev_EMA)
  
    return prediction
        
        