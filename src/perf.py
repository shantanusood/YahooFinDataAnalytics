from bs4 import BeautifulSoup
import pandas as p
#from obj import yahoo_obj as y
import traceback
import requests as r

def getPerformanceData(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = [i.text for i in soup.select(performance_trailing_data())][1:]
    labels = [i.text for i in soup.select(performance_trailing_label())][1:]
    dict = {}
    count = 0
    for i in labels:
        try:
            dict[i] = float(data[count][:-1])
        except:
            pass
        finally:
            count = count + 1
    return dict

def performance(tickers, metadata):
    code = 0
    for i in tickers:
        try:
            resp = getHtml("perf", i)
            code = resp[0]
            return getPerformanceData(resp[1])
        except:
            print("Exception occured, this is the status code {0}, and this is the ticker - {1}".format(code, i))
            traceback.print_exc()
            return None

if __name__ == "__main__":
    print(performance(['AWSHX'], ""))