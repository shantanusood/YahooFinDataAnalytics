#!/usr/bin/env python3

import sys
from data import tickers_list as t
from src import filter as f

def main():
    """
    Usage: ./predict.py [spy|dow|ndx|rus|cst|filename_start:end] [growth|div|pe|cash|profit|ratio] (only for pe)[lt|gt] [0-9|floater]

        arg[1]: Selecting the data list to run filtering on
               spy: Ticker list for S&P 500 stocks
               dow: Ticker list for Dow Jones stocks
               ndx: Tickers list for Nasdaq stocks
               rus: Tickers list for russel 2000 stocks
               cst: Can be set in /data/tickers_list, it is the custom list of tickers
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
               growth: Revenue growth year over year
               div: dividend yield
               pe: price to earning ratio of a stock
               cash:
               profit:
               ratio:
        arg[3]: This is only applicable for pe, for others it is default to gt
               lt: less than
               gt: greater than
        arg[4]: For div this is can be a floating point value as well, for growth, pe, cap, it is a number
    """

    tickers = t.tickers(sys.argv[1])
    filter = sys.argv[2]
    f.filter(tickers, filter)


if __name__ == "__main__":
    main()
