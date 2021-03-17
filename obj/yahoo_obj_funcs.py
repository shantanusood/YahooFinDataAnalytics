from obj import yahoo_obj as y
import datetime as dt

def getTableData(soup, type):
    dict = {}
    n = 0
    header_val = [i.text.upper() for i in soup.select(y.table_breakdown_header())[1:-1]]
    l = soup.select(y.table_data())
    labels = soup.select(y.table_labels())
    data = [i.text for i in l]
    n = int(len(data)/(len(labels)+1)) + 1
    counter = 0
    try:
        dict["Duration"] = header_val
        for i in range(0, len(data), n):
            dict[str(labels[counter].text)] = data[i:i+n-1]
            counter = counter + 1
    except:
        n = 4
        for i in range(0, len(data), n):
            dict[str(labels[counter].text)] = data[i:i+n-1]
            counter = counter + 1
    return dict
