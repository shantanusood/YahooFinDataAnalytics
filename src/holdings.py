#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as p
#from obj import yahoo_obj as y
import traceback
from obj import yahoo_obj as y
from src.helpers import commons as cm

def getTopHoldings(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    name = [i.text for i in soup.select(y.holdings_top_name())]
    assets = [float(i.text[:-1]) for i in soup.select(y.holdings_top_assets())]
    dict = {}
    print("Historical data for {0}:".format(ticker))
    try:
        dict['Name'] = name
        dict['Assets'] = assets
    except:
        traceback.print_exc()
    return dict

def holdings(tickers, metadata):
    code = 0
    for i in tickers:
        try:
            resp = cm.getHtml("hld", i)
            code = resp[0]
            d = getTopHoldings(resp[1], i)
            return d
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            traceback.print_exc()
            return None
