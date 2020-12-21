import urllib.request
import json
class Ticker: 

    #Define class variables
    yf_url='https://query1.finance.yahoo.com/v7/finance/quote?symbols='

    #Initialize the class
    def __init__(self, ticker):
        self.ticker = ticker
        self.ticker_json_url=Ticker.yf_url+self.ticker

    def __get_ticker_json(self):
    #Making this function private as the instances should do not need to call it.
    #Function used to fetch JSON data from YahooFinance URL and extract dict format data from JSON
    
    #Retrive the data on the webpage with URLLIB
        with urllib.request.urlopen(self.ticker_json_url) as ticker_json:
            ticker_data_json_dict=json.load(ticker_json)
            return ticker_data_json_dict

    def __get_ticker_details_dict(self):
    #Making this function private as the instances should do not need to call it.
    #Function used to extract dict format data from JSON

        #Define variables for the function
        #Getting the DICT variable with JSON result string
        ticker_data_json_dict=Ticker.__get_ticker_json(self)
        #List of important KEYS that we care about
        important_details_list=["shortName", "fullExchangeName", "regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "regularMarketDayRange", "fiftyTwoWeekRange"]
        #This variable will be returned with important ticker details we care about
        important_ticker_details_dict={}
    
        #Wrapping below call as dict.values() returns a view which cannot be accessed using index
        ticker_details_list=list(ticker_data_json_dict.values())

        #Iterating through the data to get to meaningful ticker details
        ticker_details_dict = ticker_details_list[0]['result'][0]

        #Place each valid important KEY with its VALUE in the important_ticker_details_dict
        for ticker_param in important_details_list:
            if ticker_param in ticker_details_dict.keys():
                important_ticker_details_dict[ticker_param]=ticker_details_dict[ticker_param]
        return important_ticker_details_dict

    def retrive_ticker_detail_dict(self):
        ticker_details_dict=Ticker.__get_ticker_details_dict(self)
        return ticker_details_dict