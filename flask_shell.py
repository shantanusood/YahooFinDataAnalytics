from flask import Flask
import script as s
import json
import pandas as pd
from data import tickers_list as t
from src import filter as f
import os
from flask_cors import CORS

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
        return ret.to_json(orient='records', lines=True)
    else:
        ret_j = {}
        for i in ret:
            ret_j[i] = ret[i].to_json(orient='records', lines=True)
        return json.dumps(ret_j)

@app.route('/filters/<tickerlist>/<filter>')
def withStdInput(tickerlist, filter):
    return str(f.filter(t.tickers(tickerlist), filter, getMetadata(tickerlist), "", ""))

@app.route('/filters/<tickers>/<filter>/<third>')
def withThirdInput(tickers, filter, third):
    return str(f.filter(t.tickers(tickers), filter, getMetadata(tickers), third, ""))

@app.route('/filters/<tickers>/<filter>/<third>/<fourth>')
def withFourthInput(tickers, filter, third, fourth):
    return str(f.filter(t.tickers(tickers), filter, getMetadata(tickers), third, fourth))

