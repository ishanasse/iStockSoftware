# Import dependencies Files/Modules/Packages and static variables
from datetime import datetime
import requests
#import urllib.request
#import json




# Class for Ticker and define Ticker related methods
class Ticker: 

    #Class variables
    yf_url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols='


    #Initialize the class
    def __init__(self, ticker):
        self.ticker = ticker
        self.ticker_json_url=Ticker.yf_url+self.ticker


    def __get_ticker_json(self):
    # Private Function used to fetch JSON data from YahooFinance URL and extract dict format data from JSON
    
        start_micros = int(datetime.now().microsecond) #Time_log
        #Output = JSON format Dict from YFinance
        ticker_data_json_dict = requests.get(self.ticker_json_url).json()
        finish_micros = int(datetime.now().microsecond) #Time_log
        time_ms = int(((finish_micros - start_micros) if finish_micros > start_micros else (1000000 + finish_micros - start_micros))/1000) #Time_log
        print(f'---Request.get for {self.ticker} took {time_ms}ms---') #Time_log
        return ticker_data_json_dict


    def __get_ticker_details_dict(self):
    #Making this function private as the instances would not need to call it.
    #Function used to extract dict format data from JSON

        #Define variables for the function
        #List of important KEYS that we care about
        important_details_list=["quoteType", "shortName", "fullExchangeName", "regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "regularMarketDayRange", "fiftyTwoWeekRange"]
        #This variable will be returned with important ticker details we care about
        important_ticker_details_dict={}

        #Getting the DICT variable with JSON result string
        ticker_data_json_dict = Ticker.__get_ticker_json(self)
    
        #Wrapping below call as dict.values() returns a view which cannot be accessed using index
        ticker_details_list=list(ticker_data_json_dict.values())

        #Iterating through the data to get to meaningful ticker details
        ticker_details_dict = ticker_details_list[0]['result'][0]

        #Place each valid important KEY = ticker with its VALUE = DictOfValues in the important_ticker_details_dict
        for ticker_param in important_details_list:
            if ticker_param in ticker_details_dict.keys():
                important_ticker_details_dict[ticker_param]=ticker_details_dict[ticker_param]
        return important_ticker_details_dict

    def retrive_ticker_detail_dict(self):
    #Function to retrieve ticker details Dict for each ticker
    # Input = Ticker, example: "FB"
    # Return the Dict with Values for FB Stock. Example {"Ticker": "FB", "lastPrice":"250.54", "DayPriceRange":"247.33-254.43"}
        ticker_details_dict=Ticker.__get_ticker_details_dict(self)
        return ticker_details_dict