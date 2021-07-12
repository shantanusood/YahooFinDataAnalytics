def table_labels():
    return "span[class='Va(m)']"

def table_data():
    return "div[class='D(tbrg)'] > div[data-test='fin-row'] > div > div[data-test='fin-col']"
    #return "div[class='rw-expnded'][data-test='fin-row'] > div > div[class^='D']"

def table_breakdown_header():
    return "div[class='D(tbhg)'] > div > div"

def current_value():
    return "div[class$='Mend(20px)'] > span:nth-child(1)"

def current_value_alt():
    return "h3[class^='intraday__price'] > *"

def quote_table():
    return "div[data-test='right-summary-table'] > table > tbody > tr > td"

def quote_table_alt():
    return "li[class='kv__item'] > *"

def yahoo_dividend_table_first():
    return "table[data-test='historical-prices'] > tbody > tr:nth-child(1) > td"

def yahoo_dividend_table_fourth():
    return "table[data-test='historical-prices'] > tbody > tr:nth-child(4) > td"

def performance_trailing_label():
    return "section[data-yaft-module$='Performance'] >div:nth-child(2) > div > div >span:nth-child(1)"

def performance_trailing_data():
    return "section[data-yaft-module$='Performance'] >div:nth-child(2) > div > div >span:nth-child(2)"

def performance_annual_label():
    return "section[data-yaft-module$='Performance'] >div:nth-child(3) > div > div > span:nth-child(1)"

def performance_annual_data():
    return "section[data-yaft-module$='Performance'] >div:nth-child(3) > div > div > span:nth-child(3)"

def history_label():
    return "table[data-test='historical-prices'] > thead > tr > th > span"

def history_date():
    return "table[data-test='historical-prices'] > tbody > tr > td:nth-child(1) > span"

def history_open():
    return "table[data-test='historical-prices'] > tbody > tr > td:nth-child(2) > span"

def history_high():
    return "table[data-test='historical-prices'] > tbody > tr > td:nth-child(3) > span"

def history_low():
    return "table[data-test='historical-prices'] > tbody > tr > td:nth-child(4) > span"

def history_close():
    return "table[data-test='historical-prices'] > tbody > tr > td:nth-child(5) > span"

def history_adj_close():
    return "table[data-test='historical-prices'] > tbody > tr > td:nth-child(6) > span"

def history_vol():
    return "table[data-test='historical-prices'] > tbody > tr > td:nth-child(7) > span"

def holdings_top_name():
    return "div[data-test='top-holdings'] > table > tbody > tr > td:nth-child(1)"

def holdings_top_assets():
    return "div[data-test='top-holdings'] > table > tbody > tr > td:nth-child(3)"

def holdings_portfolio_comp():
    return "section[class*='smartphone'] > div:nth-child(1) > div:nth-child(1) > div > div > span:nth-child(2)"

def holdings_sector():
    return "section[class*='smartphone'] > div:nth-child(1) > div:nth-child(2) > div > div > span"

def holdings_bond():
    return "section[class*='smartphone'] > div:nth-child(2) > div:nth-child(2) > div > div > span"

def risk(row):
    return "section[data-yaft-module$='Performance'] > div > div > div:nth-child("+row+") > div > span"

def calendarTable():
    return "div[id='cal-res-table'] > div > table > tbody > tr > td"

def options_table(type):
    return "table[class^='{0}'][class$='list-options'] > tbody > tr> td".format(type)