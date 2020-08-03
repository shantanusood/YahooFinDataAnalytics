from flask import Flask
import script as s
import json
import pandas as pd
from data import tickers_list as t
from src import filter as f
import os
from flask_cors import CORS

from bs4 import BeautifulSoup
from obj import yahoo_obj as y
from src.helpers import commons as cm
from data import tickers_list as tl
import traceback

app = Flask(__name__)
CORS(app)

def getMetadata(input):
    metadata = []
    if "_" in input:
        if os.path.isfile('./data/'+input[0:int(input.index("_"))] + '.csv'):
            metadata = t.ticker_details(input)
    return metadata

@app.route('/')
def quide():
    return """
<!DOCTYPE html>
<html lang="en">
<body>
<p>
<h3>Try out below:</h3>
</p>
<ul>
<li>	http://localhost:5000/filters/^msft/cash/0</li>
<li>  	http://localhost:5000/filters/Stocks_21:25/cash/0</li>
<li>  	http://localhost:5000/filters/Stocks_21:25/profit</li>
<li>  	http://localhost:5000/filter/spy_21:25/pe/gt/0</li>
<li>  	http://localhost:5000/data/quote/msft</li>
</ul>
</body>
</html>
"""

@app.route('/data/<filter>/<tickers>')
def quote(filter, tickers):
    ret = s.main(filter, tickers)
    if isinstance(ret, pd.DataFrame):
        return ret.to_json()
    else:
        ret_j = {}
        for i in ret:
            ret_j[i] = ret[i].to_json()
            print(ret_j[i])
        return ret_j

@app.route('/data/monitoring')
def returnMonitoring():
    #with open('./data/monitoring.json', 'r') as data_file:
        #return str(json.loads(data_file.read())).replace("'", "\"")
    wrt = "["
    calls = []
    puts = []
    price = 0
    with open('./data/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            resp = cm.getHtml("quote", x['ticker'])
            if resp[0] == 200:
                df = parse(resp[1])
                x['price'] = df.iloc[0]['value']
                price = float(x['price'])
            counter = 0
            for vals in list(x['positions']['fidelity']['call']):
                if " " in vals:
                    x['positions']['fidelity']['call'][counter] = vals[:vals.index(" ")]
                counter = counter + 1
            counter = 0
            for vals in list(x['positions']['tastyworks']['call']):
                if " " in vals:
                    x['positions']['tastyworks']['call'][counter] = vals[:vals.index(" ")]
                counter = counter + 1
            counter = 0
            for vals in list(x['positions']['robinhood']['call']):
                if " " in vals:
                    x['positions']['robinhood']['call'][counter] = vals[:vals.index(" ")]
                counter = counter + 1
            counter = 0
            for vals in list(x['positions']['fidelity']['put']):
                if " " in vals:
                    x['positions']['fidelity']['put'][counter] = vals[:vals.index(" ")]
                counter = counter + 1
            counter = 0
            for vals in list(x['positions']['tastyworks']['put']):
                if " " in vals:
                    x['positions']['tastyworks']['put'][counter] = vals[:vals.index(" ")]
                counter = counter + 1
            counter = 0
            for vals in list(x['positions']['robinhood']['put']):
                if " " in vals:
                    x['positions']['robinhood']['put'][counter] = vals[:vals.index(" ")]
                counter = counter + 1
            counter = 0

            calls = list(x['positions']['fidelity']['call']) + list(x['positions']['tastyworks']['call']) + list(x['positions']['robinhood']['call'])
            calls = list(map(float, calls))
            try:
                counter = 0
                calls_min = min(calls)
                if int(str(calls_min)[str(calls_min).index(".")+1:]) == 0:
                    for vals in list(x['positions']['fidelity']['call']):
                        if vals == str(int(calls_min)):
                            divi = (float(vals) - price)*100/price
                            x['positions']['fidelity']['call'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['tastyworks']['call']):
                        if vals == str(int(calls_min)):
                            divi = (float(vals) - price)*100/price
                            x['positions']['tastyworks']['call'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['robinhood']['call']):
                        if vals == str(int(calls_min)):
                            divi = (float(vals) - price)*100/price
                            x['positions']['robinhood']['call'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                else:
                    for vals in list(x['positions']['fidelity']['call']):
                        if vals == str(calls_min):
                            divi = (float(vals) - price)*100/price
                            x['positions']['fidelity']['call'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['tastyworks']['call']):
                        if vals == str(calls_min):
                            divi = (float(vals) - price)*100/price
                            x['positions']['tastyworks']['call'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['robinhood']['call']):
                        if vals == str(calls_min):
                            divi = (float(vals) - price)*100/price
                            x['positions']['robinhood']['call'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
            except Exception:
                pass

            puts = list(x['positions']['fidelity']['put']) + list(x['positions']['tastyworks']['put']) + list(x['positions']['robinhood']['put'])
            puts = list(map(float, puts))
            try:
                counter = 0
                puts_max = max(puts)
                if int(str(calls_min)[str(calls_min).index(".")+1:]) == 0:
                    for vals in list(x['positions']['fidelity']['put']):
                        if vals == str(int(puts_max)):
                            divi = (price - float(vals)) * 100 / price
                            x['positions']['fidelity']['put'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['tastyworks']['put']):
                        if vals == str(int(puts_max)):
                            divi = (price - float(vals)) * 100 / price
                            x['positions']['tastyworks']['put'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['robinhood']['put']):
                        if vals == str(int(puts_max)):
                            divi = (price - float(vals)) * 100 / price
                            x['positions']['robinhood']['put'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                else:
                    for vals in list(x['positions']['fidelity']['put']):
                        if vals == str(puts_max):
                            divi = (price - float(vals)) * 100 / price
                            x['positions']['fidelity']['put'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['tastyworks']['put']):
                        if vals == str(puts_max):
                            divi = (price - float(vals)) * 100 / price
                            x['positions']['tastyworks']['put'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
                    for vals in list(x['positions']['robinhood']['put']):
                        if vals == str(puts_max):
                            divi = (price - float(vals)) * 100 / price
                            x['positions']['robinhood']['put'][counter] = vals + " (" + str(round(divi, 2)) + "%)"
                        counter = counter + 1
                    counter = 0
            except Exception:
                pass
            wrt = wrt + str(x) + ","

    with open('./data/monitoring.json', 'w') as file:
        file.write(wrt[:-1].replace("'", "\"") + "]")
        file.close()
    with open('./data/monitoring.json', 'r') as data_file:
        return data_file.read()

@app.route('/data/monitoring/delete/<ticker>')
def returnMonitoringDel(ticker):
    lst = []
    with open('./data/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        lst = list(data)
        counter = 0
        for x in data:
            if x['ticker'] == ticker:
                lst.pop(counter)
            counter = counter + 1
    with open('./data/monitoring.json', 'w') as file:
        file.write(str(lst).replace("'", "\""))
        file.close()
    return ""

@app.route('/data/monitoring/add/<account>/<ticker>/<width>/<call>/<put>')
def returnMonitoringAdd(account, ticker, width, call, put):
    wrt = "["
    with open('./data/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        counter = 0
        for x in data:
            if x['ticker'] == ticker:
                pylst = list(x['positions'][account]['call'])
                pylst.append(call)
                pylst2 = list(x['positions'][account]['put'])
                pylst2.append(put)
                x['positions'][account]['call'] = pylst
                x['positions'][account]['put'] = pylst2
                x['total'] = x['total'] + int(width)
                counter = 1
            wrt = wrt + str(x) + ","

        if counter < 1:
            val = '{"ticker":"' + ticker + '", "price": 100, "total": 0, "positions": {"fidelity": {"call": [], "put": []}, "robinhood": {"call": [], "put": []}, "tastyworks": {"call": [], "put": []}}}'
            jval = json.loads(val)
            pylst = list(jval['positions'][account]['call'])
            pylst.append(call)
            pylst2 = list(jval['positions'][account]['put'])
            pylst2.append(put)
            jval['positions'][account]['call'] = pylst
            jval['positions'][account]['put'] = pylst2
            jval['total'] = int(width)
            wrt = wrt + str(jval) + ","

    with open('./data/monitoring.json', 'w') as file:
        file.write(wrt[:-1].replace("'", "\"") + "]")
        file.close()
    return ""

@app.route('/data/monitoring/delete/<ticker>/<account>/<type>/<strike>')
def returnMonitoringDelStrike(account, ticker, type, strike):
    wrt = "["
    with open('./data/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            if x['ticker'] == ticker:
                pylst = list(x['positions'][account][type])
                pylst.remove(strike)
                x['positions'][account][type] = pylst
                x['total'] = x['total'] - 500
            wrt = wrt + str(x) + ","

    with open('./data/monitoring.json', 'w') as file:
        file.write(wrt[:-1].replace("'", "\"") + "]")
        file.close()
    return ""

@app.route('/filters/<tickerlist>/<filter>')
def withStdInput(tickerlist, filter):
    return json.dumps(f.filter(t.tickers(tickerlist), filter, getMetadata(tickerlist), "", ""))

@app.route('/filters/<tickers>/<filter>/<third>')
def withThirdInput(tickers, filter, third):
    return json.dumps(f.filter(t.tickers(tickers), filter, getMetadata(tickers), third, ""))

@app.route('/filters/<tickers>/<filter>/<third>/<fourth>')
def withFourthInput(tickers, filter, third, fourth):
    return json.dumps(f.filter(t.tickers(tickers), filter, getMetadata(tickers), third, fourth))

@app.route('/csv/<type>')
def csvData(type):
    filename = './data/' + type + '.csv'
    return pd.read_csv(filename).head(10000).to_csv()


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    dict = {'value':soup.select(y.current_value())[0].text}
    l = soup.select(y.quote_table())
    data = [j.text for j in l]
    for i in range(0, len(data), 2):
        dict[data[i]] = data[i+1:i+2]

    df = pd.DataFrame(dict)
    return df