from obj import yahoo_obj as y 
import requests as r

def getFinancialLabels(soup):
    sel = y.table_labels()
    labels = soup.select(sel)
    labels_text = [i.text for i in labels]
    return labels_text

def getHtml(type, ticker):
    req = r.get(linkList(type, ticker))
    return (req.status_code, req.text)

def linkList(type, ticker):
    if type == 'financial':
        return "https://finance.yahoo.com/quote/{0}/financials?p={0}".format(ticker)
    elif type == 'quote':
        return "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)
    elif type == "cf":
        return "https://finance.yahoo.com/quote/{0}/cash-flow?p={0}".format(ticker)
    elif type == "bs":
        return "https://finance.yahoo.com/quote/{0}/balance-sheet?p={0}".format(ticker)
    elif type == "perf":
        return "https://finance.yahoo.com/quote/{0}/performance?p={0}".format(ticker)

