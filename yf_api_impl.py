import pandas as pd # data manipulation
import yfinance as yf # get financials of the companies
import pymongo # connect to MongoDB
from pymongo import MongoClient # connect to MongoDB
from pymongo.server_api import ServerApi
import csv
from datetime import datetime, timedelta

def yf_makeCSV(ticker):
    uri = "mongodb+srv://jaimejac:HackaThon1@hackathon.nsbiltv.mongodb.net/?retryWrites=true&w=majority"
    DB_NAME = "Hackathon_Database"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
        
        
    db = client[DB_NAME]
    collection = db[ticker]

    collist = db.list_collection_names()
    name_of_db = ticker
    insert_data = False
    if name_of_db in collist:
       # The collection exists
        d = collection.find_one(sort=[("_id", pymongo.DESCENDING)])
        
        last_date = d['Date']
        start_date = last_date + timedelta(days=1)
        end_date = datetime.today()
        
        stock_df = yf.download(ticker, start=start_date, end = end_date)
        stock_df.reset_index(inplace=True)

        if stock_df['Date'][0] >= start_date:
            insert_data = True
        

    else:
    #    The collection does not exist
        insert_data = True
        stock_df = yf.download(ticker)
        stock_df.reset_index(inplace=True)

        
        

    stock_df['Date'] =  pd.to_datetime(stock_df['Date'], format='%Y-%m-%d')
    csv_name = ticker + '.csv'

    if insert_data :

        data_dict = stock_df.to_dict("records")

        collection.insert_many(data_dict)
        

        stock_data = collection.find({"Date":{"$exists":True},"Date":{"$ne":"null"}},{"Date":1, "Close":1})

        field_names = ["Date", "Close"]

        with open(csv_name, 'w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerow(field_names)

            for data in stock_data:
                csv_output.writerow(
                    [
                    data['Date'].strftime("%m/%d/%Y"),data['Close']
                    ])
    
    return csv_name
