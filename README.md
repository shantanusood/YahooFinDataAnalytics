# YahooFinDataAnalytics

* Complete universe of all Yahoo financial tickers available @ /data/ in the txt/csv files
* Usage can be found either in the html files: script.html or predict.html or within the script.py or predict.py

### Requirements to run the project:
* Runs Python bash script
* Python3

### Documentation:
*Usage: ./predict.py [spy|dow|ndx|rus|cst|filename_start:end] [growth|div|pe|cash|profit|ratio] (only for pe)[lt|gt] [0-9|floater]

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


*Usage: ./script.py [quote|fin|bs|cf] [ticker]

        quote: returns the basic data for the ticker as a dataframe
        fin: returns the income statement for the ticker as a dataframe
        bs: returns the balance sheet for the ticker as a dataframe
        cf: returns the cash flow for the ticker as a dataframe

        -> You can also get quote for various other securities, and a group of securities.
           There is a universe of securty tickers that can be found in /data/ folder.
           There are csv files where the ticker information is saved. Below are examples on how to query:
           ./script.py quote filename_startindex:endindex
           Examples:
           ------------------------------------------------------------------------------------------------------------------------------
           |./script.py quote Stocks_1001:1003  |  This returns the quote for stocks index 1001 (inclusive) to 1003 (not inclusive)     |
           ------------------------------------------------------------------------------------------------------------------------------
           |./script.py quote Currency_2011:2016|  This returns the quote for currency index 2011 (inclusive) to 2016 (not inclusive)   |
           ------------------------------------------------------------------------------------------------------------------------------
           To get the index of required tickers in a file use the grep command, for example:
           ------------------------------------------------------------------------------------------------------------------------------
           |grep -in apple Stocks.csv           |  This returns all lines & line number containing "Apple" startindex = line number - 2 |
           ------------------------------------------------------------------------------------------------------------------------------



## Examples:

S|Example|Explanation|
--- | --- | --- |
1.|./predict.py *AAPL growth 0|Revenue growth for the last 3 years if it is greater 0|
2.|./predict.py Stocks_10:15 growth -99|Revenue growth for the last 3 years for the stocks indexed 10 to 15 from the Stocks.txt for all growth|
3.|./script.py quote MSFT|Will give you basic info about the microsoft stock|
