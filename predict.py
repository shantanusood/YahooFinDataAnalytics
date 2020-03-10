#!/usr/bin/env python3

import sys
from data import tickers_list as t
from src import filter as f

def main():
    """
    Usage: ./predict.py [spy|dow|ndx|rus|cst] [growth|div|pe|cap] (only for pe)[lt|gt] [0-9|floater]

        arg[1]: Selecting the data list to run filtering on
               spy: Ticker list for S&P 500 stocks
               dow: Ticker list for Dow Jones stocks
               ndx: Tickers list for Nasdaq stocks
               rus: Tickers list for russel 2000 stocks
               cst: Can be set in /data/tickers_list, it is the custom list of tickers
        arg[2]: Type of filter to apply to the data list
               growth: Revenue growth year over year
               div: dividend yield
               pe: price to earning ratio of a stock
               cap: Real to predicted market cap comparison
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
