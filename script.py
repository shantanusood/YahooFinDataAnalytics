#!/usr/bin/env python3
import numpy as np
import requests as r
import sys
from src import quote as q, financials as f, bs as b, cf as c 
import pandas as pd
from data import tickers_list as tl
import os.path
from src.helpers import commons as cm

def main(filter, tickers):
    """
    Usage: ./script.py [quote|fin|bs|cf] [ticker]

        quote: returns the basic data for the ticker as a dataframe
        fin: returns the income statement for the ticker as a dataframe
        bs: returns the balance sheet for the ticker as a dataframe
        cf: returns the cash flow for the ticker as a dataframe

        -> You can also get quote for various other securities, and a group of securities.
           There is a universe of securty tickers that can be found in /data/ folder.
           There are csv files where the ticker information is saved. Below are examples on how to query:
           ./script.py quote filename_startindex:endindex
           Examples:
           ------------------------------------------------------------------------------------------------------------------------------
           |./script.py quote Stocks_1001:1003	|  This returns the quote for stocks index 1001 (inclusive) to 1003 (not inclusive) 	|
           ------------------------------------------------------------------------------------------------------------------------------
           |./script.py quote Currency_2011:2016|  This returns the quote for currency index 2011 (inclusive) to 2016 (not inclusive)	|
           ------------------------------------------------------------------------------------------------------------------------------
           To get the index of required tickers in a file use the grep command, for example:
           ------------------------------------------------------------------------------------------------------------------------------
           |grep -in apple Stocks.csv	        |  This returns all lines & line number containing "Apple" startindex = line number - 2 |
           ------------------------------------------------------------------------------------------------------------------------------
    """

    if filter == 'quote':
        input = str(tickers)
        return q.getQuote(input)
    elif filter == 'fin':
        resp = cm.getHtml("financial", tickers)
        if resp[0] == 200:
            df = f.getFinancialNumbers(resp[1])
            pd.set_option('display.max_rows', 10, 'display.max_columns', 100)
            return df
    elif filter == 'bs':
        resp = cm.getHtml("bs", tickers)
        if resp[0] == 200:
            df = b.getBalanceSheet(resp[1])
            pd.set_option('display.max_rows', 10, 'display.max_columns', 100)
            return df
    elif filter == 'cf':
        resp = cm.getHtml("cf", tickers)
        if resp[0]:
            df = c.getCashFlow(resp[1])
            pd.set_option('display.max_rows', 10, 'display.max_columns', 100)
            return df
    else:
        print("Invalid data request type, usage: ", end='')
        print("'./script.py [quote|fin|bs|cf] [ticker]'")

if __name__ == '__main__':
    d = {}
    if "_" in sys.argv[2]:
        d = main(sys.argv[1], sys.argv[2])
        for i in d:
            print(i)
            print(d[i])
    else:
        print(main(sys.argv[1], sys.argv[2]))
