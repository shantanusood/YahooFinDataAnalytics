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


def getComposition(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    name = [i.text for i in soup.select(y.holdings_portfolio_comp())]
    dict = {}
    l1 = [name[0]]
    l2 = [name[1]]
    print("Composition data for {0}:".format(ticker))
    try:
        dict['Stocks'] = l1
        dict['Bonds'] = l2
    except:
        traceback.print_exc()
    print(dict)
    return dict


def getWeight(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    test = lambda x: len(x)>0
    sector = [i.text for i in soup.select(y.holdings_sector()) if test(i.text)]
    bond = [i.text for i in soup.select(y.holdings_bond()) if test(i.text)]
    dict = {}
    print("Historical data for {0}:".format(ticker))
    try:
        for i in range(0, len(sector), 2):
            try:
                dict[sector[i]] = float(sector[i+1][:-1])
            except:
                pass
        for i in range(0, len(bond), 2):
            try:
                dict[bond[i]] = float(bond[i+1][:-1])
            except:
                pass
    except:
        traceback.print_exc()
    print(dict)
    sector = []
    percent = []
    dict_api = {'Sector':sector, 'Percent':percent}
    for x in dict:
        dict_api['Sector'].append(x)
        dict_api['Percent'].append(dict[x])

    return dict_api

def holdings(tickers, metadata, type):
    code = 0
    for i in tickers:
        try:
            if len(type) == 0:
                resp = cm.getHtml("hld", i)
                code = resp[0]
                d = getTopHoldings(resp[1], i)
                return d
            elif type == 'comp':
                resp = cm.getHtml("hld", i)
                code = resp[0]
                d = getComposition(resp[1], i)
                return d
            elif type == 'weight':
                resp = cm.getHtml("hld", i)
                code = resp[0]
                d = getWeight(resp[1], i)
                return d
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            traceback.print_exc()
            return None
