import re
from classes_BE import Ticker


########## Define Functions ##########

def get_user_tickers_list(user_input):
#Function used to grab tickers from user and return the list
    user_tickers_list=user_input.split(" ")
    return user_tickers_list

def validate_ticker(ticker: str):
# Function used to validate each ticker provided by the user. Conditions to check: 
# i.   Not greater than 8 characters II
# ii.  No use of numbers or symbols
# iii. No more than 2 DOTs
# iv. No more than 2 DOTs

    if ticker=="": 
        return False
    if len(ticker) > 8: 
        return False
    for char in ticker:
        if not(char.isalpha() or char=="."): 
            return False
    if ticker.count(".")>2: 
        return False
    return True

def get_final_tickers_list(user_tickers_list: list):
    #Define variables for the function
    #ticker_alias_list=["stock5", "stock4", "stock3", "stock2", "stock1"]
    default_tickers_list=["PXT.TO", "HUBS", "PING", "BNS.TO", "AAPL", "CRM", "WORK", "BB.TO", "SU.TO", "SAIL"]
    final_tickers_list=[]
    #final_tickers_dict={}
    for ticker in user_tickers_list:
        ticker=ticker.upper()
        if validate_ticker(ticker):
            final_tickers_list.append(ticker)
            if (ticker in default_tickers_list):
                default_tickers_list.remove(ticker)
            #if (ticker.upper() in default_tickers_list): default_tickers_list.remove(ticker.upper())
    while len(final_tickers_list) < 5:
        final_tickers_list.append(default_tickers_list.pop())
    return final_tickers_list
    # for alias in ticker_alias_list:
    #     final_tickers_dict[alias]=validated_user_tickers_list.pop()
    # return final_tickers_dict

# def create_ticker_instances(validated_user_tickers_list: list):
#     for ticker in validated_user_tickers_list:
#         Ticker.create_ticker_instances(ticker)

def create_instances_dict(final_tickers_list):
    fetched_tickers_instances_dict={}
    for ticker in final_tickers_list:
        fetched_tickers_instances_dict[ticker]=Ticker(ticker)
    return fetched_tickers_instances_dict