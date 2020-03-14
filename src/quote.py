from bs4 import BeautifulSoup
import pandas as pd
from obj import yahoo_obj as y
from src.helpers import commons as cm
import os
from data import tickers_list as tl
import traceback

def getQuote(input):
    df_list = {}
    if "_" in input:
        count = 0
        details = []
        if os.path.isfile('./data/'+input[0:int(input.index("_"))] + '.csv'):
            details = tl.ticker_details(input)
        for i in tl.tickers(input):
            resp = cm.getHtml("quote", i)
            try:
                if resp[0] == 200:
                    df = parse(resp[1])
                    pd.set_option('display.max_rows', 5, 'display.max_columns', 100)
                    #print("Quote for: {} ".format(i), end='')
                    if len(details)>count:
                        #print(details[count])
                        df_list[str(details[count])] = df
                    else:
                        df_list[i] = df
                        #print("No Details available")
                    #print(df)
            except:
                print("Exception occured while getting quote for: {0}".format(i))
                traceback.print_exc()
            finally:
                count = count + 1
        return df_list
    else:
        resp = cm.getHtml("quote", input)
        if resp[0] == 200:
            df = parse(resp[1])
            pd.set_option('display.max_rows', 5, 'display.max_columns', 100)
            #print(df)
            return df
    return df_list

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    dict = {'value':soup.select(y.current_value())[0].text}
    l = soup.select(y.quote_table())
    data = [j.text for j in l]
    for i in range(0, len(data), 2):
        dict[data[i]] = data[i+1:i+2]

    df = pd.DataFrame(dict)
    return df
