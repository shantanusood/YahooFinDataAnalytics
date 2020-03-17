#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as p
#from obj import yahoo_obj as y
import traceback
from obj import yahoo_obj as y
from src.helpers import commons as cm

def getPerformanceData(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    data = [i.text for i in soup.select(y.performance_annual_data())][1:]
    labels = [i.text for i in soup.select(y.performance_annual_label())][1:]
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


def getPerformanceTrail(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    data = [i.text for i in soup.select(y.performance_trailing_data())][1:]
    labels = [i.text for i in soup.select(y.performance_trailing_label())][1:]
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


def performance(tickers, metadata, type):
    code = 0
    for i in tickers:
        try:
            resp = cm.getHtml("perf", i)
            code = resp[0]
            if type == 'ann':
                d = getPerformanceData(resp[1], i)
                return d
            elif type == 'trail':
                d = getPerformanceTrail(resp[1], i)
                return d
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            traceback.print_exc()
            return None

if __name__ == "__main__":
    print(performance(['AWSHX'], "", 'ann'))
