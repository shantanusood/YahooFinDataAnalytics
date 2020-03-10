from bs4 import BeautifulSoup
from obj import yahoo_obj_funcs as y
import pandas as p

def getBalanceSheet(html):
    soup = BeautifulSoup(html, 'html.parser')
    df = p.DataFrame(y.getTableData(soup, "bs"))
    return df

