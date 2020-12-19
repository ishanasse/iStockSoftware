#Adding dependency Modules/Packages
import tkinter as tk
from functions_BE_with_UI import *
import time

#Adding dependency Modules/Packages
def initiate_ui_window():
    global main_screen
    main_screen=tk.Tk()
    main_screen_properties()
    create_main_canvas()
    user_entry_frame()

    main_screen.mainloop()

def main_screen_properties():
    main_screen.title("iStockSoftware")
    main_screen.tk.call('wm', 'iconphoto', main_screen._w, tk.PhotoImage(file='stocks_software/working_directory/stocks.gif'))

def create_main_canvas():
    main_canvas=tk.Canvas(main_screen, width=500, height=100, relief = 'solid', bg="#eff7a2")
    main_canvas.grid(row=0, column=0)

def user_entry_frame():
    ui_frame = tk.LabelFrame(main_screen, text='Enter 5 tickers separated by " ":', bg="#eff7a2")
    ui_frame.grid(row=0, column=0)

    global tickers_entry
    tickers_entry=tk.Entry(ui_frame, relief="solid", borderwidth=2)
    tickers_entry.grid(row=0, column=0)

    run_button=tk.Button(ui_frame,text='Run', relief="raised", command= execute_run_button)
    run_button.grid(row=0, column=1)

    create_tickers_canvas()



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


def create_tickers_canvas():
    tickers_canvas=tk.Canvas(main_screen, width=500, height=100, bg="#eff7a2")
    tickers_canvas.grid(row=1, column=0)

    #Creating Ticker tittles in window
    global stocks_frame
    stocks_frame=tk.LabelFrame(tickers_canvas, text="  Your Stocks being displayed:  ", fg="#007cc7", bg="#eff7a2")
    stocks_frame.grid(row=0, column=0)
    
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
        detail_name=tk.Label(stocks_frame,text=" ")
        detail_name.grid(row=1, column=begin_column, padx=30)
        begin_column+=1
        detail_name=tk.Label(stocks_frame,text=ticker, bg="#b8e7f9", relief="sunken")
        detail_name.grid(row=1, column=begin_column, padx=30)
        begin_column+=1

def push_ticker_values():
    begin_column = 1
    for ticker in final_tickers_list:
        begin_row = 2
        value_field=tk.Label(stocks_frame, text=" ")
        value_field.grid(row=begin_row, column=begin_column)
        begin_column+=1
        for detail,value in fetched_tickers_instances_dict[ticker].retrive_ticker_detail_dict().items():
            if detail in ["regularMarketChange", "regularMarketChangePercent"]: value=str(value)[0:5]
            if detail == "shortName": value=str(value)[0:12]                
            value_field=tk.Label(stocks_frame, text=value)
            value_field.grid(row=begin_row, column=begin_column)
            begin_row +=1
        begin_column+=1