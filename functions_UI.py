# Import dependencies Files/Modules/Packages and static variables
import tkinter as tk
from datetime import datetime
#from functions_BE_with_UI import *
from functions_BE_with_UI import default_ticker_instances_dict, get_user_tickers_list, get_final_tickers_list, create_instances_dict

# ---------- Define UI Related variables ----------#
 
run_counter = 0
yellow = "#eff7a2"
lblue = "#c8e3fe"
blue = "#9ECDFD"
red = "#e72b3c"
white = "#f2f8ff"
lgrey = "#f1f1f1"
re_interval = 5000 #5 secs
dynamic_details_list = ["regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "regularMarketDayRange", "fiftyTwoWeekRange"]

########## Define UI-TKinter related Functions ##########

# Function to fire the main TKinter Window
def initiate_ui_window():
    print(str(datetime.now())[11:22] + " Func: initiate_ui_window()") #Log    

    # Create a dict of default instances
    default_ticker_instances_dict()

    main_screen_properties()
    create_ue_frame() # user entry

    # Run main window
    main_screen.mainloop()


def main_screen_properties():
    print(str(datetime.now())[11:22] + " Func: main_screen_properties()") #Log
    global main_screen
    main_screen = tk.Tk()
    main_screen.title("iStockSoftware")
    
    try:
        main_screen.tk.call('wm', 'iconphoto', main_screen._w, tk.PhotoImage(file='stocks_software/working_directory/stocks.gif'))
    except:
        main_screen.tk.call('wm', 'iconphoto', main_screen._w, tk.PhotoImage(file='stocks.gif'))
    
    # Handle close
    main_screen.protocol("WM_DELETE_WINDOW", handle_close_window)


# User Entry Frame
def create_ue_frame():
    print(str(datetime.now())[11:22] + " Func: create_ue_frame()") #Log

    global ue_frame
    ue_frame = tk.LabelFrame(main_screen, text = 'Enter 5 tickers separated by " " as shown:', bg = lblue)
    ue_frame.grid(row = 0, column = 0, sticky = "nsew")

    global tickers_entry
    tickers_entry = tk.Entry(ue_frame, relief = "solid", borderwidth = 2)
    tickers_entry.grid(row = 0, column = 1, sticky = "nsew", columnspan = 2)

    create_ri_entry_window() # refresh interval

    show_sample_input()
    create_run_button()
    create_stocks_frame()


def create_run_button():
    run_button = tk.Button(ue_frame,text = 'Run', relief = "raised", command = execute_run_button)#, bg = blue)
    run_button.grid(row = 2, column = 3, sticky = "nsew")


def show_sample_input():
    sample_ip = tk.Label(ue_frame, text = 'Sample (case-insensitive) : "AAPL GOOG MSFT AC.TO TSLA"', bg = lblue)
    sample_ip.grid(row = 1, column = 0, sticky = "nse", columnspan = 3)


# Get preferred refresh interval
def create_ri_entry_window():
    ri_one = tk.Label(ue_frame, text = 'Refresh every :', bg = lblue)
    ri_one.grid(row = 2, column = 0, sticky = "nsew")
    global reint_entry
    reint_entry = tk.Entry(ue_frame, relief = "solid", borderwidth = 2)
    reint_entry.grid(row = 2, column = 1, sticky = "nsew")
    ri_two = tk.Label(ue_frame, text = ' secs (Choose 3-60)', bg = lblue)
    ri_two.grid(row = 2, column = 2, sticky = "nsw")


def create_stocks_frame():
    print(str(datetime.now())[11:22] + " Func: create_stocks_frame()") #Log

    global stocks_frame
    stocks_frame=tk.LabelFrame(main_screen, text="  Your Stocks being displayed:  ", bg=lblue)
    stocks_frame.grid(row = 1, column = 0, sticky = "nsew")
    
    # Row title STOCKs
    stocks_label=tk.Label(stocks_frame, text= "STOCKs ->", bg=lblue)
    stocks_label.grid(row = 1, column = 0)


def execute_run_button():
    print(str(datetime.now())[11:22] + " Func: execute_run_button()") #Log

    check_if_re_run()

    global final_tickers_list
    final_tickers_list = get_valid_tickers_list()

    # Create Fetched_tickers_instances_dict. Example: {"AAPL" : <instance>}
    global fetched_tickers_instances_dict
    fetched_tickers_instances_dict=create_instances_dict(final_tickers_list)

    get_refresh_interval()
    create_row_headers()
    create_static_cells()
    push_ticker_values()

# Get list of tickers and apply validation
def get_valid_tickers_list():
    user_input=tickers_entry.get()
    user_tickers_list = get_user_tickers_list(user_input)
    return get_final_tickers_list(user_tickers_list)

#Destroy previously created stocks_frame for re-run of the program
def check_if_re_run():
    global run_counter
    if run_counter > 0:
        stocks_frame.destroy()
        create_stocks_frame()
    run_counter = 1

# Get user preference or use default of 5 secs
def get_refresh_interval():    
    try:
        re_input = reint_entry.get()
        if (int(re_input) > 2) and (int(re_input) < 61):
            global re_interval
            # If valid interval provided, replace the default value
            re_interval = int(re_input) * 1000
    except:
        print("Using default refresh interval of 5 secs.")


# Create row headers with names of important details
def create_row_headers():
    print(str(datetime.now())[11:22] + " Func: create_row_headers()") #Log    
    
    important_details_list=["Shrt Name:", "Exchange.:", "Mrkt Price.:", "Lst Chnge.:", "Lst Chge%:", "DayRange:", "52W Rnge:"]

    current_row = 2
    for detail in important_details_list:
        detail_name=tk.Label(stocks_frame, text=detail, bg=lblue)
        detail_name.grid(row=current_row, column = 0, sticky = "nse")
        current_row+=1


# This function will fill static values to the stocks frame
def create_static_cells():
    print(str(datetime.now())[11:22] + " Func: create_static_cells()") #Log    
    
    current_column = 1

    # Validated EQUITY tickers for getting live market data
    global updated_tickers_list
    updated_tickers_list = []

    for ticker in final_tickers_list:

        add_column_space(current_column)
        current_column += 1

        # Create static cells
        try:
            # Fetch ticker market data
            ticker_data_dict = fetched_tickers_instances_dict[ticker].retrive_ticker_detail_dict()
    
            # If ticker result is not found <<<OR>>> ticker is not an EQUITY
            if ticker_data_dict["quoteType"] != "EQUITY":
                raise Exception("Invalid Equity ticker.")
            shname = ticker_data_dict["shortName"]
            updated_tickers_list.append(ticker)

        except:
            print(f"{datetime.now().strftime('%H:%M:%S')} {ticker} is not a valid EQUITY ticker. Using a default ticker.")
            global default_tickers_list

            #check if re-runs emptied the default_tickers_list, and re-fill it
            if len(default_tickers_list) < 1:
                default_tickers_list = ["PXT.TO", "HUBS", "PING", "BNS.TO", "AAPL", "CRM", "WORK", "BB.TO", "SU.TO", "SAIL"]

            ticker = default_tickers_list.pop()

            # Fetch ticker market data
            ticker_data_dict = fetched_tickers_instances_dict[ticker].retrive_ticker_detail_dict()
            
            shname = ticker_data_dict["shortName"]
            updated_tickers_list.append(ticker)

        shrt_name = tk.Label(stocks_frame, text = shname[0:12], relief="sunken")
        shrt_name.grid(row = 2, column=current_column, sticky = "nsew")

        ticker_title = tk.Label(stocks_frame, text = ticker, relief="sunken", bg = blue)
        ticker_title.grid(row = 1, column = current_column, sticky = "nsew")
        
        exname = ticker_data_dict["fullExchangeName"]
        exch_name = tk.Label(stocks_frame, text = exname, relief="sunken")
        exch_name.grid(row = 3, column=current_column, sticky = "nsew")
        
        current_column+=1


def add_column_space(col):
    add_space = tk.Label(stocks_frame,text=" ", bg=lblue)
    for row_var in range(8):
        add_space.grid(row = row_var, column = col)


def push_ticker_values():
    print(str(datetime.now())[11:22] + " Func: push_ticker_values()")
    
    current_column = 2

    for ticker in updated_tickers_list:   

        # Fetch ticker market data
        ticker_data_dict = fetched_tickers_instances_dict[ticker].retrive_ticker_detail_dict()

        current_row = 4
        #dynamic_details_list = ["regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "regularMarketDayRange", "fiftyTwoWeekRange"]

        for detail in dynamic_details_list:
            value = ticker_data_dict[detail]
            if detail == "regularMarketChange" or detail == "regularMarketChangePercent":
                value=str(value)[0:5]         
            value_field = tk.Label(stocks_frame, text = value)
            value_field.grid(row = current_row, column=current_column, sticky="nsew")

            current_row += 1

        current_column += 2
    
    print(str(datetime.now())[11:22] + " ***waiting to refresh***")
    stocks_frame.after(re_interval, push_ticker_values)


def handle_close_window():
    print(str(datetime.now())[11:22] + " Func: handle_close_window()")
    print("Closing iStockSoftware widget.")
    exit()