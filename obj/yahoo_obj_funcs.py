from obj import yahoo_obj as y

def getTableData(soup, type):
    dict = {}
    n = 0
    l = soup.select(y.table_data())
    data = [i.text for i in l]
    if type is "bs":
        n = 5
    else:
        n = 6
    for i in range(0, len(data), n):
        dict[data[i]] = data[i+1:i+n]
    return dict
