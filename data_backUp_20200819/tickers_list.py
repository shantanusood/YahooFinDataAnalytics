#!/usr/bin/env python3
import sys
import pandas as pd

def range_vals(type, list):
    start = 0
    end = len(list)
    if "_" in type:
        start = int(type[int(type.index("_"))+1: int(type.index(":"))])
        end = int(type[int(type.index(":"))+1:])

    return [start, end]

def tickers(type):

    spy = []
    ndx = []
    rus = []
    filelist = []
    cst = ['MCHP', 'MSFT', 'MNST', 'MCO', 'MSI', 'MUR', 'NFLX', 'NKE', 'NOC', 'OXY', 'PCAR', 'PAYX', 'PBCT', 'PGR', 'PWR', 'RTN', 'O', 'REGN', 'ROST', 'R', 'CRM']

    if "spy" in type:
        with open('./data/sp500.txt', 'r') as f:
            spy = f.read().split('\n')
        ret = range_vals(type, spy)
        return [i for i in spy if len(i)>0][ret[0]:ret[1]]
    elif "ndx" in type:
        with open('./data/Nasdaq.txt', 'r') as f:
            ndx = f.read().split(",")
        ret = range_vals(type, ndx)
        return [i.replace('\t', '').replace("\'", "") for i in ndx][ret[0]:ret[1]]
    elif "rus" in type:
        with open('./data/Russel2000.txt', 'r') as f:
            rus = f.read().split(",")
        ret = range_vals(type, rus)
        return [i.replace('\t', '').replace("\'", '').replace('\n', '') for i in rus][ret[0]:ret[1]]
    elif "cst" in type:
        ret = range_vals(type, cst)
        return cst[ret[0]:ret[1]]
    elif "^" in type:
        tick = str(type[1:])
        return [tick]
    else:
        filename = ""
        if "_" in type:
            filename = './data/' + type[0:int(type.index('_'))] + '.txt'
        else:
            filename = './data/' + type+'.txt'
        with open(filename, 'r') as f:
            filelist = f.read().split('\n')
        ret = range_vals(type, filelist)
        return filelist[ret[0]:ret[1]]

def ticker_details(type):
    filename = ""
    start = 0
    end = 0
    data = None
    list = []
    if "_" in type:
        filename = './data/' + type[0:int(type.index('_'))] + '.csv'
        start = int(type[int(type.index("_"))+1: int(type.index(":"))])
        end = int(type[int(type.index(":"))+1:])
        data = pd.read_csv(filename)
        for i in range(start, end):
            list.append(dict(data.iloc[i]))
        return list
    else:
        filename = './data/' + type+'.csv'
        data = pd.read_csv(filename)
        return data

if __name__ == '__main__':
    print(ticker_details(sys.argv[1]))
