#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as p
import traceback
from obj import yahoo_obj as y
from src.helpers import commons as cm

def getRisk(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    test = lambda x: x!="VGT"
    empty = lambda x: len(x)>0
    print("Risk data for {0}:".format(ticker))
    dict = {"Type": [i.text for i in soup.select(y.risk(str(2))) if test(i.text)]}
    data = []
    for x in range(3,20):
        try:
            data = [i.text for i in soup.select(y.risk(str(x))) if empty(i.text)]
            dict[data[0]] = [float(i) for i in data[1:]]
        except:
            pass
    print(dict)
    return dict

def risk(tickers, metadata):
    code = 0
    for i in tickers:
        try:
            resp = cm.getHtml("risk", i)
            code = resp[0]
            return getRisk(resp[1], i)
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker".format(i))
            traceback.print_exc()
            return None

if __name__ == "__main__":
    risk("aapl","")
