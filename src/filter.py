import requests as r 
from src import quote as q, financials as f, bs as b, cf as c 
import pandas as pd 
import sys 
import traceback 
import re
from src.helpers import commons as cm
from src import perf as p
from src import hist as h
from src import holdings as hl
from src import risk as ri

def filter(tickers, filter, metadata, val_filter_1, val_filter_2):
    if filter == "growth":
        return growth(tickers, metadata, val_filter_1)
    elif filter == "div":
        return dividend(tickers, metadata, val_filter_1)
    elif filter == "pe":
        return pe_ratio(tickers, metadata, val_filter_1, val_filter_2)
    elif filter == "profit":
        return profit(tickers, metadata)
    elif filter == "ratio":
        return ratio(tickers, metadata)
    elif filter == "cash":
        return cash(tickers, metadata, val_filter_1)
    elif filter == "perf":
        return p.performance(tickers, metadata, val_filter_1)
    elif filter == "hist":
        return h.history(tickers, metadata)
    elif filter == "hld":
        return hl.holdings(tickers, metadata)
    elif filter == "risk":
        return ri.risk(tickers, metadata)
    else:
        print("Invalid filter, usage:", end='')
        print("'./predict.py [spy|dow|ndx|rus|cst|*filter|filename_start:end] [growth|div|pe|cash|profit|ratio] (only for pe)[lt|gt] [0-9|floater]'")


def growth(tickers, metadata, val_filter_1):
    code = 0
    test = lambda x: (x>=int(val_filter_1))
    l = []
    data_return = {}
    for i in tickers:
        try:
            ret_tickers = []
            resp = cm.getHtml("financial", i) 
            code = resp[0]
            fin = f.getFinancialNumbers(resp[1])
            revenue = [int(i.replace(",","")) for i in list(fin['Total Revenue'])]
            change = list(pd.Series(revenue[::-1]).pct_change())[1:]
            rate = [round(i*100) for i in change][::-1][1:]
            for x in rate:
                if test(x):
                    ret_tickers.append(x)
            if len(ret_tickers) == 3:
                data_return[i] = ret_tickers
                print(ret_tickers, end=' ')
                l = [val for val in metadata if val['Ticker']==str(i)]
                if len(l)>0:
                    print(" -----------------INFO------------> ", end='')
                    print(l[0])
                else:
                    print(" ---Ticker (No Info available)--> ", end='')
                    print(i)
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i)) 
            #traceback.print_exc()

    return data_return

def dividend(tickers, metadata, val_filter_1):
    code = 0
    test = lambda x: (x>=float(val_filter_1))
    l = []
    data_return = {}
    for i in tickers:
        try:
            resp = cm.getHtml("quote", i)
            code = resp[0]
            quote = q.parse(resp[1])
            val = re.search("[0-9]*[.][0-9]*", str(str(quote['Forward Dividend & Yield']).split(' ')[5]))
            if val:
                if test(float(val.group())):
                    print(val.group(), end='')
                    l = [val for val in metadata if val['Ticker']==str(i)]
                    if len(l)>0:
                        print(" -----------------INFO------------> ", end='')
                        print(l[0])
                    else:
                        print(" ---Ticker (No Info available)--> ", end='')
                        print(i)
                    data_return[i] = float(val.group())
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            #traceback.print_exc()
    return data_return

def pe_ratio(tickers, metadata, val_filter_1, val_filter_2):
    code = 0
    test = False
    l = []
    data_return = {}
    if str(val_filter_1) == 'lt':
        test = lambda x: (x<=float(val_filter_2))
    elif str(val_filter_1) == 'gt':
        test = lambda x: (x>=float(val_filter_2))
    for i in tickers:
        try:
            resp = cm.getHtml("quote", i)
            code = resp[0]
            quote = q.parse(resp[1])
            pe = float(quote['PE Ratio (TTM)'])
            if test(pe):
                print(pe, end='')
                l = [val for val in metadata if val['Ticker']==str(i)]
                if len(l)>0:
                    print(" -----------------INFO------------> ", end='')
                    print(l[0])
                else:
                    print(" ---Ticker (No Info available)--> ", end='')
                    print(i)
                data_return[i] = pe
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            #traceback.print_exc()
    return data_return

def ratio(tickers, metadata):
    l = []
    data_return = {}
    for i in tickers:
        try:
            resp = cm.getHtml("financial", i)
            code = resp[0]
            fin = f.getFinancialNumbers(resp[1])
            revenue = [int(i.replace(",","")) for i in list(fin['Total Revenue'])]
            net = [int(i.replace(",","")) for i in list(fin['Net Income'])]
            rd = [int(i.replace(",","")) for i in list(fin['Research Development'])]
            prof = []
            for x in range(0, len(revenue)):
                t = revenue[x] / (net[x] + rd[x])
                prof.append(t)
            #change = list(pd.Series(prof[::-1]).pct_change())[1:]
            rate = [round(i, 3) for i in prof][1:]
            print(rate, end='')
            l = [val for val in metadata if val['Ticker']==str(i)]
            if len(l)>0:
                print(" -----------------INFO------------> ", end='')
                print(l[0])
            else:
                print(" ---Ticker (No Info available)--> ", end='')
                print(i)
            data_return[i] = rate
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            #traceback.print_exc()
    return data_return

def profit(tickers, metadata):
    l = []
    data_return = {}
    #locale.setlocale(locale.LC_ALL, '')
    for i in tickers:
        try:
            resp = cm.getHtml("financial", i)
            code = resp[0]
            fin = f.getFinancialNumbers(resp[1])
            revenue = [int(i.replace(",","")) for i in list(fin['Total Revenue'])]
            cost = [int(i.replace(",","")) for i in list(fin['Cost of Revenue'])]
            sga = [int(i.replace(",","")) for i in list(fin['Selling General and Administrative'])]
            prof = []
            for x in range(0, len(revenue)):
                t = revenue[x] - (cost[x] + sga[x])
                prof.append(t)
            print("Net Profit: ", end='')
            print(['{:,}'.format(i)+',000' for i in prof[1:]], end='')
            change = list(pd.Series(prof[::-1]).pct_change())[1:]
            rate = [round(i*100,3) for i in change][::-1][1:]
            print("; % Profit change (y/y): ", end='')
            print(rate, end='')
            l = [val for val in metadata if val['Ticker']==str(i)]
            if len(l)>0:
                print(" -----------------INFO------------> ", end='')
                print(l[0])
            else:
                print(" ---Ticker (No Info available)--> ", end='')
                print(i)
            data_return[i] = (prof[1:], rate)
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            #traceback.print_exc()
    return data_return

def cash(tickers, metadata, val_filter_1):
    code = 0
    l = []
    data_return = {}
    test = lambda x: (x>=int(val_filter_1))
    for i in tickers:
        try:
            ret_tickers = []
            resp = cm.getHtml("cf", i)
            code = resp[0]
            cf = c.getCashFlow(resp[1])
            revenue = [int(i.replace(",","")) for i in list(cf['Free Cash Flow'])]
            change = list(pd.Series(revenue[::-1]).pct_change())[1:]
            rate = [round(i*100) for i in change][::-1][1:]
            for x in rate:
                if test(x):
                    ret_tickers.append(x)
            if len(ret_tickers) == 3:
                print(ret_tickers, end=' ')
                l = [val for val in metadata if val['Ticker']==str(i)]
                if len(l)>0:
                    print(" -----------------INFO------------> ", end='')
                    print(l[0])
                else:
                    print(" ---Ticker (No Info available)--> ", end='')
                    print(i)
                data_return[i] = ret_tickers

        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i)) 
            #traceback.print_exc()
    return data_return


