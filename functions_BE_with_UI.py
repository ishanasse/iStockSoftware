# Import dependencies Files/Modules/Packages and static variables
from classes_BE import Ticker

########## Variables #########
default_tickers_list = ["PXT.TO", "HUBS", "PING", "BNS.TO", "AAPL", "CRM", "WORK", "BB.TO", "SU.TO", "SAIL"]
fetched_tickers_instances_dict={}

########## Define Functions for the BE logic ##########

def default_ticker_instances_dict():
    for ticker in default_tickers_list:
        fetched_tickers_instances_dict[ticker]=Ticker(ticker)

def get_user_tickers_list(user_input):
#Function used to grab tickers from user and return the list
    user_tickers_list=user_input.split(" ")
    return user_tickers_list


def validate_ticker(ticker: str):
# Function used to validate the FORMAT of each ticker provided by the user.

    if ticker == "": 
        return False
    if len(ticker) > 8: 
        return False
    for char in ticker:
        if not(char.isalpha() or char == "." or char== "-"): 
            return False
    if ticker.count(".")>2: 
        return False
    return True


def get_final_tickers_list(user_tickers_list: list):
    global default_tickers_list
    #Define variables for the function
    final_tickers_list=[]
    #final_tickers_dict={}
    for ticker in user_tickers_list:
        ticker=ticker.upper()
        if validate_ticker(ticker):
            final_tickers_list.append(ticker)
            if (ticker in default_tickers_list):
                default_tickers_list.remove(ticker)
    while len(final_tickers_list) < 5:
        final_tickers_list.append(default_tickers_list.pop())
        if len(default_tickers_list) < 1:
            default_tickers_list = ["PXT.TO", "HUBS", "PING", "BNS.TO", "AAPL", "CRM", "WORK", "BB.TO", "SU.TO", "SAIL"]
    return final_tickers_list

def create_instances_dict(final_tickers_list):
    for ticker in final_tickers_list:
        fetched_tickers_instances_dict[ticker]=Ticker(ticker)
    return fetched_tickers_instances_dict