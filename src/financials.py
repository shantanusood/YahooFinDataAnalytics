from bs4 import BeautifulSoup
import pandas as p
from obj import yahoo_obj_funcs as y

def getFinancialNumbers(html):
    soup = BeautifulSoup(html, 'html.parser')
    df = p.DataFrame(y.getTableData(soup, "fin"))
    return df
