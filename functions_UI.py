#Adding dependency Modules/Packages
import tkinter as tk
from functions_BE_with_UI import *
import time

#Global variables
run_counter = 1

#Adding dependency Modules/Packages
def initiate_ui_window():
    global main_screen
    main_screen=tk.Tk()
    main_screen.title("iStockSoftware")
    main_screen.tk.call('wm', 'iconphoto', main_screen._w, tk.PhotoImage(file='stocks.gif'))
    user_entry_frame()

    main_screen.mainloop()



def user_entry_frame():
    ui_frame = tk.LabelFrame(main_screen, text='Enter 5 tickers separated by " ":', bg="#eff7a2")
    ui_frame.grid(row=0, column=0, sticky="nsew")

    global tickers_entry
    tickers_entry=tk.Entry(ui_frame, relief="solid", borderwidth=2)
    tickers_entry.grid(row=0, column=0)

    run_button=tk.Button(ui_frame,text='Run', relief="raised", command= execute_run_button)
    run_button.grid(row=0, column=1)

    create_stocks_frame()



def execute_run_button():
    user_input=tickers_entry.get()
    user_tickers_list=get_user_tickers_list(user_input)
    #Get final validated user ticker's list
    global final_tickers_list
    final_tickers_list=get_final_tickers_list(user_tickers_list)
    create_table_rows_columns()
    global fetched_tickers_instances_dict
    fetched_tickers_instances_dict=create_instances_dict(final_tickers_list)
    push_ticker_values()


def create_stocks_frame():

    #Creating Ticker tittles in window
    global stocks_frame
    stocks_frame=tk.LabelFrame(main_screen, text="  Your Stocks being displayed:  ", fg="#007cc7", bg="#eff7a2")
    stocks_frame.grid(row=1, column=0)
    
    stocks_label=tk.Label(stocks_frame, text= " Stocks: ", bg="#eff7a2")
    stocks_label.grid(row=1, column=0)

def create_table_rows_columns():
    #Add variables
    important_details_list=["Sh.Name:", "Exchang:", "L Price:", "L. Chge:", "L.Chge%:", "DayRnge:", "52wRnge:"]
    #Creating a row for each important ticker detail
    begin_row = 2
    for detail in important_details_list:
        detail_name=tk.Label(stocks_frame, text=detail, bg="#eff7a2")
        detail_name.grid(row=begin_row, column=0)
        begin_row+=1

    begin_column = 1
    for ticker in final_tickers_list:
        detail_name=tk.Label(stocks_frame,text=" ", bg="#eff7a2")
        detail_name.grid(row=1, column=begin_column)
        begin_column+=1
        detail_name=tk.Label(stocks_frame,text=ticker, bg="#b8e7f9", relief="sunken")
        detail_name.grid(row=1, column=begin_column, sticky = "nsew")
        begin_column+=1

def push_ticker_values():
    begin_column = 1
    for ticker in final_tickers_list:
        begin_row = 2
        value_field=tk.Label(stocks_frame, text=" ", bg="#eff7a2")
        value_field.grid(row=begin_row, column=begin_column)
        begin_column+=1
        try:
            for detail,value in fetched_tickers_instances_dict[ticker].retrive_ticker_detail_dict().items():
                if detail == "regularMarketChange": value = str(value)[0:5]
                if detail == "regularMarketChangePercent": value = str(value)[0:5]+"%"
                if detail == "shortName": value=str(value)[0:12]                
                value_field=tk.Label(stocks_frame, text = value)
                value_field.grid(row=begin_row, column=begin_column, sticky="nsew")
                begin_row +=1
        except:
            global default_tickers_list
            extra_ticker = default_tickers_list.pop()
            if len(default_tickers_list) < 1:
                default_tickers_list = ["PXT.TO", "HUBS", "PING", "BNS.TO", "AAPL", "CRM", "WORK", "BB.TO", "SU.TO", "SAIL"]
            for detail,value in fetched_tickers_instances_dict[extra_ticker].retrive_ticker_detail_dict().items():
                if detail in ["regularMarketChange", "regularMarketChangePercent"]: value=str(value)[0:5]
                if detail == "shortName": value=str(value)[0:12]                
                value_field=tk.Label(stocks_frame, text = value)
                value_field.grid(row=begin_row, column=begin_column, sticky="nsew")
                begin_row +=1
                detail_name = tk.Label(stocks_frame, text = "", bg="#b8e7f9", relief="sunken")
                detail_name.grid(row=1, column=begin_column, sticky = "nsew")
                detail_name.destroy()
                detail_name = tk.Label(stocks_frame, text = extra_ticker, bg="#b8e7f9", relief="sunken")
                detail_name.grid(row=1, column=begin_column, sticky = "nsew")
        begin_column+=1
    main_screen.after(10000, push_ticker_values)
