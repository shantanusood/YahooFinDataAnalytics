from bs4 import BeautifulSoup
import pandas as p

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    dict = {'value':soup.select("span[class^='Trsdu']")[0].text}
    l = soup.select("div[data-test='right-summary-table'] > table > tbody > tr > td")
    data = [j.text for j in l]
    for i in range(0, len(data), 2):
        dict[data[i]] = data[i+1:i+2]

    df = p.DataFrame(dict)
    return df
