#!/usr/bin/env python3
import numpy as np
import requests as r
import sys
from src import quote as q, financials as f, bs as b, cf as c 
import pandas as pd
from data import tickers_list as tl
import os.path

def checkCode(req):
    if req.status_code is 200:
        return True
    else:
        print("Error occured: {}".format(req.status_code))
        return False

def main():
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
    if sys.argv[1] == 'quote':
        input = str(sys.argv[2])
        if "_" in input:
            count = 0
            details = []
            if os.path.isfile('./data/'+input[0:int(input.index("_"))] + '.csv'):
                details = tl.ticker_details(input)
            for i in tl.tickers(input):
                req = r.get("https://finance.yahoo.com/quote/{0}?p={0}".format(i))
                try:
                    if checkCode(req):
                        df = q.parse(req.text)
                        pd.set_option('display.max_rows', 5, 'display.max_columns', 100)
                        print("Quote for: {} ".format(i), end='')
                        if len(details)>count:
                            print(details[count])
                        else:
                            print("No Details available")
                        print(df)
                except:
                    print("Exception occured while getting quote for: {0}".format(i))
                finally:
                    count = count + 1
        else:
            req = r.get("https://finance.yahoo.com/quote/{0}?p={0}".format(input))
            if checkCode(req):
                df = q.parse(req.text)
                pd.set_option('display.max_rows', 5, 'display.max_columns', 100)
                print(df)
    elif sys.argv[1] == 'fin':
        req = r.get("https://finance.yahoo.com/quote/{0}/financials?p={0}".format(sys.argv[2]))
        if checkCode(req):
            df = f.getFinancialNumbers(req.text)
            pd.set_option('display.max_rows', 10, 'display.max_columns', 100)
            print(df)
    elif sys.argv[1] == 'bs':
        req = r.get("https://finance.yahoo.com/quote/{0}/balance-sheet?p={0}".format(sys.argv[2]))
        if checkCode(req):
            df = b.getBalanceSheet(req.text)
            pd.set_option('display.max_rows', 10, 'display.max_columns', 100)
            print(df)
    elif sys.argv[1] == 'cf':
        req = r.get("https://finance.yahoo.com/quote/{0}/cash-flow?p={0}".format(sys.argv[2]))
        if checkCode(req):
            df = c.getCashFlow(req.text)
            pd.set_option('display.max_rows', 10, 'display.max_columns', 100)
            print(df)

if __name__ == '__main__':
    main()

