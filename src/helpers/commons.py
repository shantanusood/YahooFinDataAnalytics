from obj import yahoo_obj as y 
import requests as r

def getFinancialLabels(soup):
    sel = y.table_labels()
    labels = soup.select(sel)
    labels_text = [i.text for i in labels]
    return labels_text

def getHtml(type, ticker):
    req = r.get(linkList(type, ticker))
    if req.status_code == 200:
        return (req.status_code, req.text, "yahoo")
    else:
        req = r.get(linkList_alt(type, ticker))
        return (req.status_code, req.text, "alt")

def linkList_alt(type, ticker):
    if type == 'quote':
        if "^" in ticker:
            return "https://www.marketwatch.com/investing/index/{0}".format(str(ticker).replace("^", ""))
        else:
            return "https://www.marketwatch.com/investing/stock/{0}".format(str(ticker))

    else:
        return linkList(type, ticker)

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
    elif type == "hist":
        return "https://finance.yahoo.com/quote/{0}/history?p={0}".format(ticker)
    elif type == "hld":
        return "https://finance.yahoo.com/quote/{0}/holdings?p={0}".format(ticker)
    elif type == "risk":
        return "https://finance.yahoo.com/quote/{0}/risk?p={0}".format(ticker)
    elif type == "options":
        return "https://finance.yahoo.com/quote/{0}/options?p={0}".format(ticker)

def calendar(start_date, end_date, target_date, offset):
    return "https://finance.yahoo.com/calendar/earnings?from={0}&to={1}&day={2}&offset={3}&size=100".format(start_date, end_date, target_date, offset)

def isGoodCandidate(ticker, call, put, vol, open):
    call_vol = ["0" if j.text == "-" else j.text for j in call][8::11]
    call_oi = ["0" if j.text == "-" else j.text for j in call][9::11]
    call_vol = [int(i.replace(",", "")) for i in call_vol]
    call_oi = [int(i.replace(",", "")) for i in call_oi]
    put_vol = ["0" if j.text == "-" else j.text for j in put][8::11]
    put_oi = ["0" if j.text == "-" else j.text for j in put][9::11]
    put_vol = [int(i.replace(",", "")) for i in put_vol]
    put_oi = [int(i.replace(",", "")) for i in put_oi]
    if sum(call_vol) > vol and sum(call_oi) > open and sum(put_vol) > vol and sum(put_oi) > open:
        return (True, ticker, sum(call_vol), sum(call_oi), sum(put_vol), sum(put_oi))
    else:
        return (False, 0, 0)