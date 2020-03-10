import requests as r 
from src import quote as q, financials as f, bs as b, cf as c 
import pandas as pd 
import sys 
import traceback 
import re

def filter(tickers, filter):
    if filter == "growth":
        growth(tickers)
    elif filter == "div":
        dividend(tickers)
    elif filter == "pe":
        pe_ratio(tickers)
    elif filter == "cap":
        market_cap(tickers)

def growth(tickers):
    code = 0
    test = lambda x: (x>=int(sys.argv[3]))

    for i in tickers:
        try:
            ret_tickers = []
            req1 = r.get("https://finance.yahoo.com/quote/{0}/financials?p={0}".format(i))
            code = req1.status_code
            fin = f.getFinancialNumbers(req1.text)
            revenue = [int(i.replace(",","")) for i in list(fin['Total Revenue'])]
            change = list(pd.Series(revenue[::-1]).pct_change())[1:]
            rate = [round(i*100) for i in change][::-1][1:]
            for x in rate:
                if test(x):
                    ret_tickers.append(x)
            if len(ret_tickers) == 3:
                print(ret_tickers, end=' ')
                print(i)
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i)) 
            #traceback.print_exc()

def dividend(tickers):
    code = 0
    test = lambda x: (x>=float(sys.argv[3]))
    for i in tickers:
        try:
            req0 = r.get("https://finance.yahoo.com/quote/{0}?p={0}".format(i))
            code = req0.status_code
            quote = q.parse(req0.text)
            val = re.search("[0-9]*[.][0-9]*", str(str(quote['Forward Dividend & Yield']).split(' ')[5]))
            if val:
                if test(float(val.group())):
                    print(i, end=' ')
                    print(val.group())
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            #traceback.print_exc()

def pe_ratio(tickers):
    code = 0
    test = False
    if str(sys.argv[3]) == 'lt':
        test = lambda x: (x<=float(sys.argv[4]))
    elif str(sys.argv[3]) == 'gt':
        test = lambda x: (x>=float(sys.argv[4]))
    for i in tickers:
        try:
            req0 = r.get("https://finance.yahoo.com/quote/{0}?p={0}".format(i))
            code = req0.status_code
            quote = q.parse(req0.text)
            pe = float(quote['PE Ratio (TTM)'])
            if test(pe):
                print(i, end=' ')
                print(pe)
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            #traceback.print_exc()

def market_cap(tickers):
    for i in tickers:
        req0 = r.get("https://finance.yahoo.com/quote/{0}?p={0}".format(i))
        req1 = r.get("https://finance.yahoo.com/quote/{0}/financials?p={0}".format(i))
        quote = q.parse(req0.text)
        fin = f.getFinancialNumbers(req1.text)
