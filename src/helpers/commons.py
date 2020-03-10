from obj import yahoo_obj as y

def getFinancialLabels(soup):
    sel = y.table_labels()
    labels = soup.select(sel)
    labels_text = [i.text for i in labels]
    return labels_text

