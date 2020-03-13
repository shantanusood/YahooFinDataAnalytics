#!/usr/bin/env python3

import sys
from data import tickers_list as t
from src import filter as f
import os.path

def main():
    """
    Usage: ./predict.py [spy|dow|ndx|rus|cst|*ticker|filename_start:end] [growth|div|pe|cash|profit|ratio] (only for pe)[lt|gt] [0-9|floater]

        arg[1]: Selecting the data list to run filtering on
               spy: Ticker list for S&P 500 stocks
               dow: Ticker list for Dow Jones stocks
               ndx: Tickers list for Nasdaq stocks
               rus: Tickers list for russel 2000 stocks
               cst: Can be set in /data/tickers_list, it is the custom list of tickers
               *ticker: If you want to apply filter to a single ticker then use this, for example *AAPL
               filename_start:end: filename are the ticker list file name, which are the csv files in /data/ folder
                   ------------------------------------------------------------------------------------------------------------------------------
                   |./predict.py Stocks_1001:1003 div 0 |  This returns the div>0 for stocks index 1001 (inclusive) to 1003 (not inclusive)     |
                   ------------------------------------------------------------------------------------------------------------------------------
                   |./predict.py Currency_2011:2016 cash|  This returns the quote for currency index 2011 (inclusive) to 2016 (not inclusive)   |
                   ------------------------------------------------------------------------------------------------------------------------------
                ->>>  To get the index of required tickers in a file use the grep command, for example:
                   ------------------------------------------------------------------------------------------------------------------------------
                   |grep -in apple Stocks.csv           |  This returns all lines & line number containing "Apple" startindex = line number - 2 |
                   ------------------------------------------------------------------------------------------------------------------------------

        arg[2]: Type of filter to apply to the data list
               growth: Revenue growth year over year (latest year at 0th index)
               div: dividend yield
               pe: price to earning ratio of a stock
               cash: Free cash flow growth over year (latest year at 0th index)
               profit: (Total Revenue) - (Cost of revenue + Selling General & Administrative)
               ratio: (Total Revenue) / (Net Income + Research & Development)
        arg[3]: This is only applicable for pe, for others it is default to gt
               lt: less than
               gt: greater than
        arg[4]: For div this is can be a floating point value as well, for growth, pe, cash it is a number, and it is left empty for profit and ratio
    """
    input = sys.argv[1]
    metadata = []
    if "_" in input:
        if os.path.isfile('./data/'+input[0:int(input.index("_"))] + '.csv'):
            metadata = t.ticker_details(input)
    tickers = t.tickers(sys.argv[1])
    filter = sys.argv[2]
    f.filter(tickers, filter, metadata)


if __name__ == "__main__":
    main()
