#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as p
#from obj import yahoo_obj as y
import traceback
from obj import yahoo_obj as y
from src.helpers import commons as cm

def getHistoryData(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    data = [i.text for i in soup.select(y.history_data())][1:]
    labels = [i.text for i in soup.select(y.history_label())][1:]
    dict = {}
    count = 0
    print("Performance data for {0}:".format(ticker))
    for i in labels:
        try:
            dict[i] = float(data[count][:-1])
            print(i, end=' : ')
            print(data[count])
        except:
            pass
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
