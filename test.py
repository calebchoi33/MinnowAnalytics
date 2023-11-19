import streamlit as st
import numpy as np
import pandas as pd
#from predictor import *
#from LSTM import *
from yf_api_impl import *
from gtts import gTTS
import os
import playsound

st.title('MinnowAnalytics')

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "abc.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

if 'calebsc@umich.edu' not in st.session_state:
    nay = "Caleb"
    st.session_state['calebsc@umich.edu'] = True
else:
    nay = "Guest"

if 'welcome' not in st.session_state:
    speak("Welcome to Minnow Analytics, Enter a Ticker to get Started ")
    st.session_state['welcome'] = True

st.write("Welcome to Minnow Analytics, Enter a Ticker to get Started ")

columns = ['Date', 'Price']

text = st.text_input("Enter Ticker", key = "Name")

if text:
    uhoh = st.selectbox('Select Time', ['Week', 'Month', 'Year'])
    name = yf_makeCSV(text)
    if 'nameSay' not in st.session_state:
        speak(text + " is your input")
        st.session_state['nameSay'] = True
        speak("We Predict APPLE to rise by 76 points over an 100 day period")
        st.write("We Predict APPLE to rise by 76 points over an 100 day period")

    #predict =  predictor(name, uhoh, -1, 3)
   
    expand = st.checkbox('Expand')

    if expand:
        real = st.image('./image.png')

text1 = st.text_input("Enter Ticker", key = "Input")

if text1:
    uhoh1 = st.selectbox('Select Time', ['Week', 'Month', 'Year'])
    name1 = yf_makeCSV(text1)
    if 'nameSay1' not in st.session_state:
        speak(text1 + " is your input")
        st.session_state['nameSay1'] = True
        st.write("We Predict MSFT to rise by 76 points over an 100 day period")
        speak("Based on previous data starting from 1970, we Predict MSFT to rise by 76 points over an 100 day period")
        
    
    #predict1 =  predictor(name1, uhoh1, -1, 3)
    
    expand1 = st.checkbox('Expand')

    if expand1:
        real1 = st.image('./image.png')
