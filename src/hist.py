#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as p
#from obj import yahoo_obj as y
import traceback
from obj import yahoo_obj as y
from src.helpers import commons as cm

def getHistoryData(html, ticker):
    test = lambda x: str(x)!='Dividend'
    soup = BeautifulSoup(html, 'html.parser')
    date = [i.text for i in soup.select(y.history_date()) if test(i.text)]
    open = [float(i.text) for i in soup.select(y.history_open()) if test(i.text)]
    high = [float(i.text) for i in soup.select(y.history_high()) if test(i.text)]
    low = [float(i.text) for i in soup.select(y.history_low()) if test(i.text)]
    close = [float(i.text) for i in soup.select(y.history_close()) if test(i.text)]
    adj_close = [float(i.text) for i in soup.select(y.history_adj_close()) if test(i.text)]
    vol = [int(i.text.replace(',','')) for i in soup.select(y.history_vol()) if test(i.text)]
    labels = [i.text for i in soup.select(y.history_label()) if test(i.text)]
    print(labels)
    numColumns = len(labels)
    dict = {}
    count = 0
    print("Historical data for {0}:".format(ticker))
    try:
        dict[labels[0]] = date[::-1]
        dict[labels[1]] = open[::-1]
        dict[labels[2]] = high[::-1]
        dict[labels[3]] = low[::-1]
        dict[labels[4]] = close[::-1]
        dict[labels[5]] = adj_close[::-1]
        dict[labels[6]] = vol[::-1]
        print(dict)
    except:
        traceback.print_exc()
    finally:
        count = count + 1
    return dict

def history(tickers, metadata):
    code = 0
    for i in tickers:
        try:
            resp = cm.getHtml("hist", i)
            code = resp[0]
            d = getHistoryData(resp[1], i)
            return d
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            traceback.print_exc()
            return None
