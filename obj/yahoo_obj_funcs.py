from obj import yahoo_obj as y

def getTableData(soup, type):
    dict = {}
    n = 0
    l = soup.select(y.table_data())
    labels = soup.select(y.table_labels())[1:]
    data = [i.text for i in l]
    if type is "bs":
        n = 5
    else:
        n = 5
    counter = 0
    try:
        n = 5
        for i in range(0, len(data), n):
            dict[str(labels[counter].text)] = data[i:i+n-1]
            counter = counter + 1
    except:
        n = 4
        for i in range(0, len(data), n):
            dict[str(labels[counter].text)] = data[i:i+n-1]
            counter = counter + 1

    return dict
