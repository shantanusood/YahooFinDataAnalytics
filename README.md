# YahooFinDataAnalytics

* Complete universe of all Yahoo financial tickers available @ /data/ in the txt/csv files
* Usage can be found either in the html files: script.html or predict.html or within the script.py or predict.py

### This app is live at below url:
* http://shantanusood.pythonanywhere.com/

### Quick Start
* Steps:

        * pip3 install -r requirements.txt
        * export FLASK_APP=flask_shell.py (linux)
        * set FLASK_APP=flask_shell.py (windows)
        * flask run

* Go to http://localhost:5000/

### Requirements to run the project:
* Runs Python bash script
* Python3

### Documentation:
* Usage: ./predict.py [spy|dow|ndx|rus|cst|*ticker|filename_start:end] [growth|div|pe|cash|profit|ratio] (only for pe)[lt|gt] [0-9|floater]

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

* Usage: ./script.py [quote|fin|bs|cf] [ticker]

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

S|Bash|Flask Equivalent|Explanation|
--- | --- | --- | --- |
1.|./predict.py ^AAPL growth 0|/filters/^aapl/growth/0|Revenue growth for the last 3 years if it is greater 0|
2.|./predict.py Stocks_10:15 growth -99|/data/Stocks_10:15/growth/-99|Revenue growth for the last 3 years for the stocks indexed 10 to 15 from the Stocks.txt for all growth|
3.|./script.py quote MSFT| |Will give you basic info about the microsoft stock|
4.|./predict.py Stocks_120:140 profit| |Provides the growth of profit for the last 3 years, with 0th index being the latest year|
5.|./predict.py Stocks_120:140 ratio| |Provides the ratio of Total revenue to expenses for the last 3 years, with 0th index being the latest year|
6.|./predict.py ^aapl growth 0| |Total revenue growth for ticker 'aapl'|
7.|./predict.py spy_32:34 growth -99| |Total revenue growth for tickers in spy.txt (SP500 list) from index 32 to 39|
8.|./predict.py Stocks_32:34 growth -99| |Total revenue growth for tickers in filename Stocks.csv frm index 32 to 39|
9.|./predict.py ^aapl div 0| |Dividend (values greater than 0) for ticker 'aapl'|
10.|./predict.py spy_32:34 div 0| |Dividend (values greater than 0) for tickers in spy.txt (SP500 list) from index 32 to 39|
11.|./predict.py Stocks_32:34 div 0| |Dividend (values greater than 0) for tickers in filename Stocks.csv frm index 32 to 39|
12.|./predict.py Stocks_32:35 pe gt 0| |PE (values greater than 0 (use lt for less than)) for tickers in filename Stocks.csv frm index 32 to 39|
13.|./predict.py spy_32:34 pe gt 0| |PE (values greater than 0 (use lt for less than)) for tickers in spy.txt (SP500 list) from index 32 to 39|
14.|./predict.py ^aapl pe gt 0| |PE (values greater than 0 (use lt for less than)) for ticker 'aapl'|
15.|./predict.py ^aapl ratio| |Ratio (see documentation above for formula) for ticker 'aapl'|
16.|./predict.py spy_32:34 ratio| |Ratio (see documentation above for formula) for tickers in spy.txt (SP500 list) from index 32 to 39|
17.|./predict.py Stocks_30_35 ratio| |Ratio (see documentation above for formula) for tickers in filename Stocks.csv frm index 32 to 39|
18.|./predict.py ^aapl profit| |Profit as tuple (Net profit as a list on index 0 and profit growth % as a list on 1 index) for ticker 'aapl'|
19.|./predict.py spy_32:39 profit| |Profit as tuple (Net profit as a list on index 0 and profit growth % as a list on 1 index)  for tickers in spy.txt (SP500 list) from index 32 to 39|
20.|./predict.py Stocks_30:35 profit| |Profit as tuple (Net profit as a list on index 0 and profit growth % as a list on 1 index) for tickers in filename Stocks.csv frm index 32 to 39|
21.|./predict.py ^aapl cash -99| |Free Cash growth for ticker 'aapl'|
22.|./predict.py spy_32:39 cash -99| |Free Cash growth for tickers in spy.txt (SP500 list) from index 32 to 39|
23.|./predict.py Stocks_32:39 cash -9| |Free Cash growth for tickers in filename Stocks.csv frm index 32 to 39|
