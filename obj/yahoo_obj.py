def table_labels():
    return "span[class='Va(m)']"

def table_data():
    return "div[class='rw-expnded'][data-test='fin-row'] > div > div[class^='D']"

def current_value():
    return "span[class^='Trsdu']"

def quote_table():
    return "div[data-test='right-summary-table'] > table > tbody > tr > td"

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

