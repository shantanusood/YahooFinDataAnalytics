from flask import Flask, request, redirect, url_for, render_template
import time
import datetime as dt
import script as s
import json
import pandas as pd
from data import tickers_list as t
from src import filter as f
from os import listdir, makedirs
from os.path import isfile, join
from flask_cors import CORS
import os
from bs4 import BeautifulSoup
from obj import yahoo_obj as y
from src.helpers import commons as cm
from data import tickers_list as tl
import traceback
import collections
import requests as r

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
@app.route('/data/<username>/accounts')
def readRawData(username):
    with open('./data/' + username + '/accounts.json', 'r') as data_file:
        return data_file.read()

@app.route('/data/<username>/monitoring/raw')
def readAccounts(username):
    with open('./data/' + username + '/monitoring.json', 'r') as data_file:
        return data_file.read()

@app.route('/data/<username>/getit')
def getit(username):
    st = list(username)
    st_num = ""
    for x in st:
        st_num = st_num + str(int(str(ord(x)-96)[-1:])*2)[-1:]
    return str("{'this':'"+str(int(str(st_num)[0])*3)[-1:] + str(st_num)[1:5] + str(int(str(st_num)[5])*3)[-1:]+"'}").replace("'", "\"")

@app.route('/data/<username>/rental/addquotes')
def send_rent_quotes(username):
    data = {}
    history = []
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        history = data['history']
        val = "{'due_date': '" + str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date())[
                                 :-2] + "01" + "', 'paid_date': 'NA', 'rent': '" + str(
            data['recurring']) + "', 'utilities': '0', 'late': '0', 'additional': '0', 'total': '" + str(
            data['recurring']) + "', 'status': 'N'}"
        jval = json.loads(val.replace("'", "\""))
        history.insert(0, jval)
        data['history'] = history
    with open('./data/' + username + '/payhist.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
    return "['Successfully wrote to accounts!']".replace("'", "\"")

@app.route('/data/<username>/rental/editquotes/<delete_or_edit>/<due_date>/<paid_date>/<rent>/<utilities>/<late>/<additional>/<total>/<status>')
def edit_rent_quotes(username, delete_or_edit, due_date, paid_date, rent, utilities, late, additional, total, status):
    data = {}
    history = []
    index = 0
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        history = data['history']

        for hist in history:
            if(hist['due_date']==due_date and delete_or_edit=='edit'):
                history.pop(index)
                val = "{'due_date': '" + due_date + "', 'paid_date': '"+paid_date+"', 'rent': '" + rent + "', 'utilities': '"+utilities+"', 'late': '"+\
                      late+"', 'additional': '"+additional+"', 'total': '" + str(int(rent) + int(utilities) + int(late) + int(additional)) + "', 'status': '"+status+"'}"
                jval = json.loads(val.replace("'", "\""))
                history.append(jval)
                break
            elif(hist['due_date']==due_date and delete_or_edit=='delete'):
                history.pop(index)
                break
            index = index + 1
        data['history'] = history
    with open('./data/' + username + '/payhist.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return "['Successfully wrote to accounts!']".replace("'", "\"")

@app.route('/data/<username>/rental/history')
def payment_history(username):
    data = {}
    history = []
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        return data

@app.route('/data/<username>/rental/outstanding')
def outstanding(username):
    data = {}
    total_out = 0
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for hist in data['history']:
            if hist['status'] == 'N':
                total_out = total_out + int(hist['total'])
        return str(total_out)

@app.route('/data/<username>/rental/extend/<period>')
def extention(username, period):
    data = {}
    total_out = 0
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data['request'] = period
    with open('./data/' + username + '/payhist.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return data

@app.route('/data/<username>/rental/extend/approve/<period>')
def extentionApprove(username, period):
    data = {}
    total_out = 0
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data['request'] = "false"
        data['expiry'] = period
    with open('./data/' + username + '/payhist.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return data

@app.route("/properties/add", methods=["POST"])
def addNewProperty():
    with open('./properties/'+request.json['name']+'.json', 'w') as data_file:
        val = "{'name': '"+request.json['name']+"', 'address': '"+request.json['address']+"', 'workorders': []}"
        jval = json.loads(val.replace("'", "\""))
        data_file.write(str(jval).replace("'", "\""))
        return "['Successfully created new property']".replace("'", "\"")

@app.route("/properties/get")
def getAllProperties():
    onlyfiles = [f for f in listdir("./properties/") if isfile(join("./properties/", f))]
    return str([str(x)[:-5] for x in onlyfiles]).replace("'", "\"")

@app.route("/properties/<properties>/get")
def getProperty(properties):
    with open('./properties/' + properties + '.json', 'r') as data_file:
        return str(json.loads(data_file.read())).replace("'", "\"")

@app.route("/properties/<properties>/workorder", methods=['GET', 'POST'])
def createWorkOrder(properties):
    data = {}
    workorder = []
    with open('./properties/'+properties+'.json', 'r') as data_file:
        data = json.loads(data_file.read())
        workorder = data['workorders']
        workorder.insert(0, request.json)
        data['workorders'] = workorder
    with open('./properties/' + properties + '.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return str(data).replace("'", "\"")

@app.route("/properties/inprogress")
def getAllInprogress():
    data = {}
    final_data = []
    onlyfiles = [f for f in listdir("./properties/") if isfile(join("./properties/", f))]
    for file in onlyfiles:
        with open('./properties/' + file, 'r') as data_file:
            data = json.loads(data_file.read())
            for x in data['workorders']:
                if(x['status'] == 'In progress'):
                    final_data.append(x)
    return str(final_data).replace("'", "\"")

@app.route("/properties/workorder/delete", methods=['GET', 'POST'])
def getDelete():
    data = {}
    final_data = []
    onlyfiles = [f for f in listdir("./properties/") if isfile(join("./properties/", f))]
    for file in onlyfiles:
        with open('./properties/' + file, 'r') as data_file:
            data = json.loads(data_file.read())
            lst_data = data['workorders']
            index = 0
            for x in lst_data:
                if (x['address'] == request.json['address'] and x['submitdate'] == request.json['time']):
                    lst_data.pop(index)
                    data['workorders'] = lst_data
                    break
                index = index + 1
            with open('./properties/' + file, 'w') as data_file2:
                data_file2.write(str(data).replace("'", "\""))
    return str(['Successfully deleted']).replace("'", "\"")

@app.route("/properties/workorder/completed", methods=['GET', 'POST'])
def getMarkCompleted():
    data = {}
    final_data = []
    onlyfiles = [f for f in listdir("./properties/") if isfile(join("./properties/", f))]
    for file in onlyfiles:
        with open('./properties/' + file, 'r') as data_file:
            data = json.loads(data_file.read())
            lst_data = data['workorders']
            index = 0
            for x in lst_data:
                if (x['address'] == request.json['address'] and x['submitdate'] == request.json['time']):
                    jval = json.loads(str(lst_data[index]).replace("'", "\""))
                    jval['status'] = 'Completed'
                    lst_data.pop(index)
                    lst_data.insert(index, jval)
                    data['workorders'] = lst_data
                    break
                index = index + 1
            with open('./properties/' + file, 'w') as data_file2:
                data_file2.write(str(data).replace("'", "\""))
    return str(['Successfully changed to completed']).replace("'", "\"")

@app.route("/properties/workorder/inprogress", methods=['GET', 'POST'])
def getMarkProgress():
    data = {}
    final_data = []
    onlyfiles = [f for f in listdir("./properties/") if isfile(join("./properties/", f))]
    for file in onlyfiles:
        with open('./properties/' + file, 'r') as data_file:
            data = json.loads(data_file.read())
            lst_data = data['workorders']
            index = 0
            for x in lst_data:
                print(request.json)
                if (x['address'] == request.json['address'] and x['submitdate'] == request.json['time']):
                    jval = json.loads(str(lst_data[index]).replace("'", "\""))
                    jval['status'] = 'In progress'
                    lst_data.pop(index)
                    lst_data.insert(index, jval)
                    data['workorders'] = lst_data
                    break
                index = index + 1
            with open('./properties/' + file, 'w') as data_file2:
                data_file2.write(str(data).replace("'", "\""))
    return str(['Successfully changed to in progress']).replace("'", "\"")

@app.route("/data/bug/get")
def getBugFeature():
    with open('./data/bug_feature.json', 'r') as data_file:
        return str(json.loads(data_file.read())).replace("'", "\"")

@app.route("/data/roles/get")
def getRoles():
    with open('./data/roles.json', 'r') as data_file:
        return str(json.loads(data_file.read())).replace("'", "\"")

@app.route("/data/roles/change/<username>/<newrole>")
def changeRole(username, newrole):
    data = {}
    with open('./data/roles.json', 'r') as data_file:
        data = json.loads(data_file.read())
        index = 0
        for x in data:
            if x['userid'] == username:
                data[index]['role'] = newrole
                break
            index = index + 1
    with open('./data/roles.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
    return str(data).replace("'", "\"")

@app.route("/data/roles/updateqa/<username>", methods=['GET', 'POST'])
def updateQA(username):
    data = []
    index = 0
    with open('./data/roles.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for dt in data:
            if dt['userid'] == username:
                data[index]['question'] = request.json['question']
                data[index]['answer'] = request.json['answer']
            index = index + 1
    with open('./data/roles.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return str(data).replace("'", "\"")

@app.route("/data/roles/changestatus/<username>/<status>")
def changeUserStatus(username, status):
    data = []
    index = 0
    with open('./data/roles.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for dt in data:
            if dt['userid'] == username:
                data[index]['status'] = status
            index = index + 1
    with open('./data/roles.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return str(data).replace("'", "\"")

@app.route("/data/newuser", methods=['GET', 'POST'])
def createAccount():
    data = []
    with open('./data/roles.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data.append(request.json)
    newpath = r'./data/'+request.json['userid']
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    with open('./data/roles.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
    accstr = "{'fidelity': 'account1', 'robinhood': 'account2', 'tastyworks': 'account3'}"
    payhist = "{ 'propetyname': '', 'address': '', 'recurring': '', 'status': 'Active', 'expiry': '', 'durations': [], 'request': 'false', 'history': []}"
    daily = "[{'date': ['"+ str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date())+"', '"+str(dt.datetime.today() - dt.timedelta(days=1)).split(" ")[0]+"']},{'fidelity': [0, 0]},{'robinhood': [0, 0]},{'tastyworks': [0, 0]},{'retirement': [0, 0]},{'total': [0, 0]}]"
    gains = "[{'"+ str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date().strftime("%Y-%m"))+"': {'realized': 0,'unrealized': 0,'expected': 0}},{'"+ str((dt.date.today().replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m"))+"': {'realized': 0,'unrealized': 0,'expected': 0}}]"
    monitoring = "[{'ticker': 'spy','price': '59.42','total': 0,'positions': {'fidelity': {'call': ['63'],'put': ['0'],'exp': ['18-Sep'],'coll': ['0'],'prem': ['42']},'robinhood': {'call': [],'put': [],'exp': [],'coll': [],'prem': []},'tastyworks': {'call': [],'put': [],'exp': [],'coll': [],'prem': []}},'ordered': {'call': [{'63': ['fidelity','18-Sep','0','42','6.02']}],'put': [{'0': ['fidelity','18-Sep','0','42','100.0']}]}}]"
    progress = "{'2020': {'11-20': {'spy': {'20200918SLV32': ['fidelity','32','0','34','0','0','1']}}}}"
    stocks = "[]"
    with open('./data/' + request.json['userid']  + '/accounts.json', 'w') as data_file3:
        data_file3.write(str(accstr).replace("'", "\""))
    with open('./data/' + request.json['userid']  + '/daily.json', 'w') as data_file4:
        data_file4.write(str(daily).replace("'", "\""))
    with open('./data/' + request.json['userid']  + '/gains.json', 'w') as data_file5:
        data_file5.write(str(gains).replace("'", "\""))
    with open('./data/' + request.json['userid']  + '/monitoring.json', 'w') as data_file6:
        data_file6.write(str(monitoring).replace("'", "\""))
    with open('./data/' + request.json['userid']  + '/payhist.json', 'w') as data_file7:
        data_file7.write(str(payhist).replace("'", "\""))
    with open('./data/' + request.json['userid']  + '/progress.json', 'w') as data_file8:
        data_file8.write(str(progress).replace("'", "\""))
    with open('./data/' + request.json['userid']  + '/stocks.json', 'w') as data_file9:
        data_file9.write(str(stocks).replace("'", "\""))
    return str(['Successfully added to roles']).replace("'", "\"")

@app.route("/data/deleteuser/<username>")
def deleteUser(username):
    data = []
    index = 0
    with open('./data/roles.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for dt in data:
            if username == dt['userid']:
                data.pop(index)
            index = index + 1
    with open('./data/roles.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
    dir = r'./data/'+username
    for files in os.listdir(dir):
        os.remove(os.path.join(dir, files))
    os.rmdir(dir)
    return str(['Successfully delete user']).replace("'", "\"")

@app.route("/data/bug/add/<type>", methods=['GET', 'POST'])
def addBugFeature(type):
    data = {}
    addthis = []
    with open('./data/bug_feature.json', 'r') as data_file:
        data = json.loads(data_file.read())
        addthis = data[type]
        addthis.insert(0, request.json)
        data[type] = addthis
    with open('./data/bug_feature.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return data

@app.route("/data/bug/delete/<type>", methods=['GET', 'POST'])
def deleteBugFeature(type):
    data = {}
    addthis = []
    with open('./data/bug_feature.json', 'r') as data_file:
        data = json.loads(data_file.read())
        addthis = data[type]
        index = 0
        for x in addthis:
            if x==request.json:
                addthis.pop(index)
            index = index + 1
        data[type] = addthis
    with open('./data/bug_feature.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return data

@app.route("/data/notifications/add", methods=['GET', 'POST'])
def captureNotification():
    data = []
    with open('./data/notifications.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data.append(request.json['data'])
    with open('./data/notifications.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
    return str(data).replace("'", "\"")

@app.route("/data/notifications/get")
def getNotification():
    data = []
    with open('./data/notifications.json', 'r') as data_file:
        data = json.loads(data_file.read())
    return str(data).replace("'", "\"")

@app.route("/data/notifications/delete", methods=['GET', 'POST'])
def delNotification():
    data = []
    with open('./data/notifications.json', 'r') as data_file:
        data = json.loads(data_file.read())
        index = 0
        for x in data:
            if x == request.json['data']:
                data.pop(index)
    with open('./data/notifications.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
    return str(data).replace("'", "\"")

@app.route("/data/subscriber/add", methods=['GET', 'POST'])
def addToSubscriber():
    data = []
    data2 = []
    with open('./data/subscribers.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data.append(request.json)
    with open('./data/subscribers.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
    with open('./data/notifications.json', 'r') as data_file2:
        data2 = json.loads(data_file2.read())
        strx = "User "+ request.json['username'] + " with paypal " + request.json['paypal'] + " clicked on subscribe at " + request.json['datetime']
        data2.append(strx)
    with open('./data/notifications.json', 'w') as data_file2:
        data_file2.write(str(data2).replace("'", "\""))
    return ""

@app.route("/data/<username>/updatetenant", methods=['GET', 'POST'])
def updateTenant(username):
    data = {}
    prop = {}
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data['propetyname'] = request.json['propetyname']
        with open('./properties/' + data['propetyname'] + '.json', 'r') as data_file:
            prop = json.loads(data_file.read())
            data['address'] = prop['address']
        data['recurring'] = request.json['recurring']
        data['deposit'] = request.json['deposit']
        data['durations'] = request.json['durations'].split(",")
        data['status'] = request.json['status']
        data['email'] = request.json['email']
        data['phone'] = request.json['phone']
        data['expiry'] = request.json['expiry']
    with open('./data/' + username + '/payhist.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return str(data).replace("'", "\"")

@app.route("/properties/<properties>/update", methods=['GET', 'POST'])
def updateProperty(properties):
    data = {}
    with open('./properties/' + properties + '.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data['address'] = request.json['address']
        data['image'] = request.json['image']
        data['desc'] = request.json['desc']
        data['circuitbreaker'] = request.json['circuitbreaker']
        data['watermain'] = request.json['watermain']
        data['alarm'] = request.json['alarm']
        data['fire'] = request.json['fire']
        data['centralheat'] = request.json['centralheat']
        data['heatage'] = request.json['heatage']
        data['pet'] = request.json['pet']
        data['police'] = request.json['police']
        data['hospital'] = request.json['hospital']
        data['dmv'] = request.json['dmv']
    with open('./properties/' + properties + '.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return "['Successfully wrote to accounts!']".replace("'", "\"")

@app.route('/data/<username>/updatedmycontact/<email>/<phone>')
def updateContact(username, email, phone):
    data = {}
    with open('./data/' + username + '/payhist.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data['email'] = email
        data['phone'] = phone
    with open('./data/' + username + '/payhist.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return str(data).replace("'", "\"")

@app.route('/data/<username>/accounts/<account1>/<account2>/<account3>')
def updateAccounts(username, account1, account2, account3):
    data = {}
    with open('./data/' + username + '/accounts.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data['fidelity'] = account1
        data['robinhood'] = account2
        data['tastyworks'] = account3
        print(data)
    with open('./data/' + username + '/accounts.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        return "['Successfully wrote to accounts!']".replace("'", "\"")

@app.route('/data/<username>/daily')
def dailyProgress(username):
    with open('./data/'+username+'/daily.json', 'r') as data_file:
        return data_file.read()

@app.route('/data/<username>/daily/<fidelity>/<robinhood>/<tastyworks>/<retirement>/<fidelityc>/<robinhoodc>/<tastyworksc>/<retirementc>')
def dailyProgressModify(username, fidelity, robinhood, tastyworks, retirement, fidelityc, robinhoodc, tastyworksc, retirementc):
    wrt = "["
    data_lst = []
    with open('./data/'+username+'/daily.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data_lst = list(data)
        date = list(data_lst[0]['date'])
        t = dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date()
        if str(t.strftime('%m/%d/%Y')) != data_lst[0]['date'][-1]:
            date.append(str(t.strftime('%m/%d/%Y')))
            data_lst[0]['date'] = date
            fid = list(data_lst[1]['fidelity'])
            fid.append(int(fidelity))
            data_lst[1]['fidelity'] = fid
            rob = list(data_lst[2]['robinhood'])
            data_lst[2]['robinhood'] = rob
            rob.append(int(robinhood))
            tasty = list(data_lst[3]['tastyworks'])
            tasty.append(int(tastyworks))
            data_lst[3]['tastyworks'] = tasty
            ret = list(data_lst[4]['retirement'])
            ret.append(int(retirement))
            data_lst[4]['retirement'] = ret
            total = list(data_lst[5]['total'])
            total.append(int(fidelity)+int(robinhood)+int(tastyworks))
            data_lst[5]['total'] = total

            if int(fidelityc) != 0:
                data_lst[1]['fidelity'] = [x+int(fidelityc) for x in fid]
            if int(robinhoodc) != 0:
                data_lst[2]['robinhood'] = [x+int(robinhoodc) for x in rob]
            if int(tastyworksc) != 0:
                data_lst[3]['tastyworks'] = [x+int(tastyworksc) for x in tasty]
            if int(retirementc) != 0:
                data_lst[4]['retirement'] = [x+int(retirementc) for x in ret]
            if int(fidelityc) != 0 or int(robinhoodc) != 0 or int(tastyworksc) != 0:
                incr = int(fidelityc) + int(robinhoodc) + int(tastyworksc)
                total = [x + incr for x in total]
                data_lst[5]['total'] = total
            with open('./data/'+username+'/daily.json', 'w') as file:
                file.write(str(data_lst).replace("'", "\""))
                file.close()
            return "['SUCCESS']".replace("'", "\"")
        else:
            return "['Duplicate edit instead']".replace("'", "\"")

@app.route('/data/<username>/daily/get')
def getDailyProgressRecent(username):
    wrt = "["
    data_lst = []
    with open('./data/'+username+'/daily.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data_lst = list(data)
        date_list = data_lst[0]['date'][-2:]
        fidelity_list = data_lst[1]['fidelity'][-2:]
        robinhood_list = data_lst[2]['robinhood'][-2:]
        tastyworks_list = data_lst[3]['tastyworks'][-2:]
        retirement_list = data_lst[4]['retirement'][-2:]
        ret = "[['"+date_list[0]+"','"+str(fidelity_list[0])+"','"+str(robinhood_list[0])+"','"+str(tastyworks_list[0])+"','"+str(retirement_list[0])+"'],['"+date_list[1]+"','"+str(fidelity_list[1])+"','"+str(robinhood_list[1])+"','"+str(tastyworks_list[1])+"','"+str(retirement_list[1])+"']]"
    return ret.replace("'", "\"")

@app.route('/data/<username>/updatedaily/<date>/<fidelity>/<robinhood>/<tastyworks>/<retirement>/<datec>/<fidelityc>/<robinhoodc>/<tastyworksc>/<retirementc>')
def dailyProgressUpdateRecent(username, date, fidelity, robinhood, tastyworks, retirement, datec, fidelityc, robinhoodc, tastyworksc, retirementc):
    wrt = "["
    data_lst = []
    date = str(dt.datetime.strptime(str(date), '%Y-%m-%d').date().strftime("%m/%d/%Y"))
    datec = str(dt.datetime.strptime(str(datec), '%Y-%m-%d').date().strftime("%m/%d/%Y"))
    print(date)
    #"06/29/2020"
    print(datec)
    with open('./data/'+username+'/daily.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data_lst = list(data)
        data_lst[0]['date'][-1] = datec
        data_lst[1]['fidelity'][-1] = int(fidelityc)
        data_lst[2]['robinhood'][-1] = int(robinhoodc)
        data_lst[3]['tastyworks'][-1] = int(tastyworksc)
        data_lst[4]['retirement'][-1] = int(retirementc)
        data_lst[5]['total'][-1] = int(int(fidelityc) + int(robinhoodc) + int(tastyworksc))
        data_lst[0]['date'][-2] = date
        data_lst[1]['fidelity'][-2] = int(fidelity)
        data_lst[2]['robinhood'][-2] = int(robinhood)
        data_lst[3]['tastyworks'][-2] = int(tastyworks)
        data_lst[4]['retirement'][-2] = int(retirement)
        data_lst[5]['total'][-2] = int(int(fidelity) + int(robinhood) + int(tastyworks))
        data = data_lst
    with open('./data/'+username+'/daily.json', 'w') as file:
        file.write(str(data).replace("'", "\""))
        file.close()
    return "DONE"

@app.route('/data/<username>/deletedaily', methods=["GET", "POST"])
def dailyProgressDeleteRecent(username):
    wrt = "["
    data_lst = []
    with open('./data/'+username+'/daily.json', 'r') as data_file:
        data = json.loads(data_file.read())
        data_lst = list(data)
        i = data_lst[0]['date'].index(request.json['date'])
        data_lst[0]['date'].pop(i)
        data_lst[1]['fidelity'].pop(i)
        data_lst[2]['robinhood'].pop(i)
        data_lst[3]['tastyworks'].pop(i)
        data_lst[4]['retirement'].pop(i)
        data_lst[5]['total'].pop(i)
        data = data_lst
    with open('./data/'+username+'/daily.json', 'w') as file:
        file.write(str(data).replace("'", "\""))
        file.close()
    return "DONE"

@app.route('/data/<username>/daily/<index>/<type>/<filter>')
def filterHistData(username, index, type, filter):
    with open('./data/'+username+'/daily.json', 'r') as data_file:
        data = json.loads(data_file.read())
        date = dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date()
        if str(filter).__eq__('1Wk'):
            date = date - dt.timedelta(days = 7)
        elif str(filter).__eq__('1Mon'):
            date = date - dt.timedelta(days = 30)
        elif str(filter).__eq__('3Mon'):
            date = date - dt.timedelta(days = 93)
        elif str(filter).__eq__('6Mon'):
            date = date - dt.timedelta(days = 187)
        elif str(filter).__eq__('1Year'):
            date = date - dt.timedelta(days = 365)
        elif str(filter).__eq__('2Year'):
            date = date - dt.timedelta(days=730)
        elif str(filter).__eq__('All'):
            date = dt.datetime.strptime(str(list(data[0]['date'])[0]), '%m/%d/%Y').date()
        else:
            date = dt.datetime.strptime('01/01/'+str(date.year), '%m/%d/%Y').date()
        isFound = False
        i = 0
        newDateLst = []
        newTypeLst = []
        for x in data[0]['date']:
            in_date = dt.datetime.strptime(str(x), '%m/%d/%Y').date()
            if in_date == date or (in_date - dt.timedelta(days = 1)) == date or (in_date - dt.timedelta(days = 2)) == date:
                newDateLst = list(data[0]['date'])[i:]
                newTypeLst = list(data[int(index)][str(type)])[i:]
                isFound = True
                break
            i = i + 1
        if isFound==False:
            newDateLst = data[0]['date']
            newTypeLst = data[int(index)][str(type)]
        dct = {'date': newDateLst, type: newTypeLst, 'change': '$'+str(int(newTypeLst[-1])-int(newTypeLst[0])) + ' (' + str(round((int(newTypeLst[-1])-int(newTypeLst[0]))*100/int(newTypeLst[0]), 2))+'%)'}
        return json.loads(json.dumps(dct))

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

@app.route('/data/<username>/expiration')
def byExpirationDate(username):
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        dct = {}
        for x in data:
            f_lst = list(x['positions']['fidelity']['exp'])
            fc_lst = list(x['positions']['fidelity']['coll'])
            counter = 0
            for f in f_lst:
                try:
                    dct[f] = dct[f] + int(fc_lst[counter])
                except:
                    dct[f] = int(fc_lst[counter])
                counter = counter + 1
            r_lst = list(x['positions']['robinhood']['exp'])
            rc_lst = list(x['positions']['robinhood']['coll'])
            counter = 0
            for r in r_lst:
                try:
                    dct[r] = dct[r] + int(rc_lst[counter])
                except:
                    dct[r] = int(rc_lst[counter])
                counter = counter + 1
            t_lst = list(x['positions']['tastyworks']['exp'])
            tc_lst = list(x['positions']['tastyworks']['coll'])
            counter = 0
            for t in t_lst:
                try:
                    dct[t] = dct[t] + int(tc_lst[counter])
                except:
                    dct[t] = int(tc_lst[counter])
                counter = counter + 1
        return json.loads(json.dumps(dct))

@app.route('/data/<username>/monitoring')
def returnMonitoring(username):
    #with open('./data/monitoring.json', 'r') as data_file:
        #return str(json.loads(data_file.read())).replace("'", "\"")
    wrt = "["
    calls = []
    puts = []
    price = 0
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            resp = cm.getHtml("quote", x['ticker'])
            try:
                collateral = list(x['positions']['fidelity']['coll']) + list(x['positions']['tastyworks']['coll']) + list(x['positions']['robinhood']['coll'])
                collateral = list(map(int, collateral))
                x['total'] = sum(collateral)
            except:
                print(traceback.format_exc())
                pass
            if resp[0] == 200:
                try:
                    df = parse(resp[1])
                    x['price'] = df.iloc[0]['value']
                    price = float(x['price'].replace(',', ''))
                except Exception:
                    x['price'] = 0
                    price = float(x['price'])
                    print(traceback.format_exc())
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
            x['ordered'] = json.loads('{"call": [], "put": []}')
            try:
                counter = 0
                for val in list(x['positions']['robinhood']['call']):
                    dct = {val: []}
                    lst = dct[val]
                    lst.append('robinhood')
                    lst.append(x['positions']['robinhood']['exp'][counter])
                    lst.append(x['positions']['robinhood']['coll'][counter])
                    lst.append(x['positions']['robinhood']['prem'][counter])
                    perc = (float(val) - price) * 100 / price
                    lst.append(str(round(perc, 2)))
                    counter = counter + 1
                    app = list(x['ordered']['call'])
                    app.append(json.loads(json.dumps(dct)))
                    x['ordered']['call'] = app
                counter = 0
                for val in list(x['positions']['fidelity']['call']):
                    dct = {val: []}
                    lst = dct[val]
                    lst.append('fidelity')
                    lst.append(x['positions']['fidelity']['exp'][counter])
                    lst.append(x['positions']['fidelity']['coll'][counter])
                    lst.append(x['positions']['fidelity']['prem'][counter])
                    perc = (float(val) - price) * 100 / price
                    lst.append(str(round(perc, 2)))
                    counter = counter + 1
                    app = list(x['ordered']['call'])
                    app.append(json.loads(json.dumps(dct)))
                    x['ordered']['call'] = app
                counter = 0
                for val in list(x['positions']['tastyworks']['call']):
                    dct = {val: []}
                    lst = dct[val]
                    lst.append('tastyworks')
                    lst.append(x['positions']['tastyworks']['exp'][counter])
                    lst.append(x['positions']['tastyworks']['coll'][counter])
                    lst.append(x['positions']['tastyworks']['prem'][counter])
                    perc = (float(val) - price) * 100 / price
                    lst.append(str(round(perc, 2)))
                    counter = counter + 1
                    app = list(x['ordered']['call'])
                    app.append(json.loads(json.dumps(dct)))
                    x['ordered']['call'] = app
                x['ordered']['call'] = sortVals(x['ordered']['call'])
                counter = 0
                for val in list(x['positions']['robinhood']['put']):
                    dct = {val: []}
                    lst = dct[val]
                    lst.append('robinhood')
                    lst.append(x['positions']['robinhood']['exp'][counter])
                    lst.append(x['positions']['robinhood']['coll'][counter])
                    lst.append(x['positions']['robinhood']['prem'][counter])
                    perc = (price - float(val)) * 100 / price
                    lst.append(str(round(perc, 2)))
                    counter = counter + 1
                    app = list(x['ordered']['put'])
                    app.append(json.loads(json.dumps(dct)))
                    x['ordered']['put'] = app
                counter = 0
                for val in list(x['positions']['fidelity']['put']):
                    dct = {val: []}
                    lst = dct[val]
                    lst.append('fidelity')
                    lst.append(x['positions']['fidelity']['exp'][counter])
                    lst.append(x['positions']['fidelity']['coll'][counter])
                    lst.append(x['positions']['fidelity']['prem'][counter])
                    perc = (price - float(val)) * 100 / price
                    lst.append(str(round(perc, 2)))
                    counter = counter + 1
                    app = list(x['ordered']['put'])
                    app.append(json.loads(json.dumps(dct)))
                    x['ordered']['put'] = app
                counter = 0
                for val in list(x['positions']['tastyworks']['put']):
                    dct = {val: []}
                    lst = dct[val]
                    lst.append('tastyworks')
                    lst.append(x['positions']['tastyworks']['exp'][counter])
                    lst.append(x['positions']['tastyworks']['coll'][counter])
                    lst.append(x['positions']['tastyworks']['prem'][counter])
                    perc = (price - float(val)) * 100 / price
                    lst.append(str(round(perc, 2)))
                    counter = counter + 1
                    app = list(x['ordered']['put'])
                    app.append(json.loads(json.dumps(dct)))
                    x['ordered']['put'] = app
                x['ordered']['put'] = sortVals(x['ordered']['put'])
            except Exception:
                print(traceback.format_exc())
                pass

            wrt = wrt + str(x) + ","

    with open('./data/'+username+'/monitoring.json', 'w') as file:
        file.write(wrt[:-1].replace("'", "\"") + "]")
        file.close()
    with open('./data/'+username+'/monitoring_temp.json', 'w') as file:
        file.write(wrt[:-1].replace("'", "\"") + "]")
        file.close()
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        return data_file.read()

@app.route('/data/<username>/monitoring/temp')
def returnTempMonitoring(username):
    data = {}
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
    with open('./data/'+username+'/monitoring_temp.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        data_file2.close()
    with open('./data/'+username+'/monitoring_temp.json', 'r') as data_file3:
        return data_file3.read()

def sortVals(vals):
    try:
        lst = []
        dict_vals = {}
        for x in vals:
            dict_vals.update(dict(x))
        dict_vals = collections.OrderedDict(sorted(dict_vals.items()))
        for i in dict_vals:
            lst.append(json.loads(json.dumps({i: dict_vals[i]})))
        return lst
    except Exception:
        print(traceback.format_exc())
        return vals

@app.route('/data/<username>/monitoring/delete/<ticker>')
def returnMonitoringDel(username, ticker):
    lst = []
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        lst = list(data)
        counter = 0
        for x in data:
            if x['ticker'] == ticker:
                lst.pop(counter)
            counter = counter + 1
    with open('./data/'+username+'/monitoring.json', 'w') as file:
        file.write(str(lst).replace("'", "\""))
        file.close()
    return ""

@app.route('/data/<username>/monitoring/add/<account>/<ticker>/<width>/<exp>/<call>/<put>/<prem>')
def returnMonitoringAdd(username, account, ticker, width, exp, call, put, prem):
    prem = str(int(float(prem)))
    wrt = "["
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        counter = 0
        for x in data:
            if x['ticker'] == ticker:
                for f in x['positions']['fidelity']['prem']:
                    if str(f) == str(prem):
                        expiry = str(dt.datetime.strptime(str(exp), '%Y-%m-%d').strftime('%d-%b'))
                        if expiry in x['positions']['fidelity']['exp']:
                            prem = str(int(prem) + 1)
                for f in x['positions']['robinhood']['prem']:
                    if str(f) == str(prem):
                        expiry = str(dt.datetime.strptime(str(exp), '%Y-%m-%d').strftime('%d-%b'))
                        if expiry in x['positions']['robinhood']['exp']:
                            prem = str(int(prem) + 1)
                for f in x['positions']['tastyworks']['prem']:
                    if str(f) == str(prem):
                        expiry = str(dt.datetime.strptime(str(exp), '%Y-%m-%d').strftime('%d-%b'))
                        if expiry in x['positions']['tastyworks']['exp']:
                            prem = str(int(prem) + 1)
                pylst = list(x['positions'][account]['call'])
                pylst.append(call)
                pylst2 = list(x['positions'][account]['put'])
                pylst2.append(put)
                pylst3 = list(x['positions'][account]['exp'])
                t = dt.datetime.strptime(str(exp), '%Y-%m-%d')
                pylst3.append(str(t.strftime('%d-%b')))
                pylst4 = list(x['positions'][account]['coll'])
                pylst4.append(width)
                pylst5 = list(x['positions'][account]['prem'])
                pylst5.append(prem)
                x['positions'][account]['call'] = pylst
                x['positions'][account]['put'] = pylst2
                x['positions'][account]['exp'] = pylst3
                x['positions'][account]['coll'] = pylst4
                x['positions'][account]['prem'] = pylst5
                counter = 1
            wrt = wrt + str(x) + ","

        if counter < 1:
            val = '{"ticker":"' + ticker + '", "price": 100, "total": 0, "positions": {"fidelity": {"call": [], "put": [], "exp":[], "coll":[], "prem": []}, "robinhood": {"call": [], "put": [], "exp":[], "coll":[], "prem": []}, "tastyworks": {"call": [], "put": [], "exp":[], "coll":[], "prem": []}}}'
            jval = json.loads(val)
            pylst = list(jval['positions'][account]['call'])
            pylst.append(call)
            pylst2 = list(jval['positions'][account]['put'])
            pylst2.append(put)
            pylst3 = list(jval['positions'][account]['exp'])
            t = dt.datetime.strptime(str(exp), '%Y-%m-%d')
            pylst3.append(str(t.strftime('%d-%b')))
            pylst4 = list(jval['positions'][account]['coll'])
            pylst4.append(width)
            pylst5 = list(jval['positions'][account]['prem'])
            pylst5.append(prem)
            jval['positions'][account]['call'] = pylst
            jval['positions'][account]['put'] = pylst2
            jval['positions'][account]['exp'] = pylst3
            jval['positions'][account]['coll'] = pylst4
            jval['positions'][account]['prem'] = pylst5
            jval['total'] = int(width)
            wrt = wrt + str(jval) + ","

    with open('./data/'+username+'/monitoring.json', 'w') as file:
        file.write(wrt[:-1].replace("'", "\"") + "]")
        file.close()
    print(str("['Value:  "+account + ' - ' + ticker + ' - ' + width + ' - ' + exp + ' - ' + call + ' - ' + put + ' - ' + prem + " added successfully!']").replace("'", "\""))
    return str("['Value:  " + ticker + ' - ' + exp + ' - ' + " added!']").replace("'", "\"")

@app.route('/data/<username>/monitoring/delete/getcontracts/<ticker>/<account>/<type>/<strike>')
def getNumberOfContracts(username, ticker, account, type, strike):
    removerVals = []
    premium = ""
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            if x['ticker'] == ticker:
                pylst = list(x['positions'][account][type])
                i = pylst.index(strike)
                call = list(x['positions'][account]['call'])
                removerVals.append(call.pop(i))
                x['positions'][account]['call'] = call
                put = list(x['positions'][account]['put'])
                removerVals.append(put.pop(i))
                x['positions'][account]['put'] = put
                exp = list(x['positions'][account]['exp'])
                removerVals.append(exp.pop(i))
                x['positions'][account]['exp'] = exp
                coll = list(x['positions'][account]['coll'])
                removerVals.append(coll.pop(i))
                x['positions'][account]['coll'] = coll
                prem = list(x['positions'][account]['prem'])
                premium = prem.pop(i)
                removerVals.append(premium)
                x['positions'][account]['prem'] = prem
    contractsavailable = 0
    with open('./data/'+username+'/progress.json', 'r') as data_file:
        data = json.loads(data_file.read())
        t = dt.datetime.strptime(str(removerVals[2]), '%d-%b')
        for y in data:
            try:
                id = str(y) + str(t.strftime('%m%d')) + ticker.upper() + str(removerVals[4])
                contractsavailable = int(data[str(y)][str(t.strftime('%m-%d'))][str(ticker)][id][6])
            except:
                pass
    return str("{'contracts':'"+str(contractsavailable)+"', 'premium':'"+premium+"'}").replace("'", "\"")

@app.route('/data/<username>/monitoring/delete/<ticker>/<account>/<type>/<strike>/<cost>/<contracts>')
def returnMonitoringDelStrike(username, ticker, account, type, strike, cost, contracts):
    wrt = "["
    removerVals = []
    premium = 0
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            if x['ticker'] == ticker:
                pylst = list(x['positions'][account][type])
                i = pylst.index(strike)
                call = list(x['positions'][account]['call'])
                removerVals.append(call.pop(i))
                x['positions'][account]['call'] = call
                put = list(x['positions'][account]['put'])
                removerVals.append(put.pop(i))
                x['positions'][account]['put'] = put
                exp = list(x['positions'][account]['exp'])
                removerVals.append(exp.pop(i))
                x['positions'][account]['exp'] = exp
                coll = list(x['positions'][account]['coll'])
                removerVals.append(coll.pop(i))
                x['positions'][account]['coll'] = coll
                prem = list(x['positions'][account]['prem'])
                premium = prem.pop(i)
                removerVals.append(premium)
                x['positions'][account]['prem'] = prem
            wrt = wrt + str(x) + ","
    contractsavailable = 0
    year = ""
    id = ""
    with open('./data/'+username+'/progress.json', 'r') as data_file:
        data = json.loads(data_file.read())
        t = dt.datetime.strptime(str(removerVals[2]), '%d-%b')
        found = False
        for y in data:
            try:
                id = str(y) + str(t.strftime('%m%d')) + ticker.upper() + str(removerVals[4])
                contractsavailable = int(data[str(y)][str(t.strftime('%m-%d'))][str(ticker)][id][6])
                year = y
                found = True
            except:
                pass
            if found:
                break
        if int(contracts) == int(contractsavailable):
            with open('./data/'+username+'/monitoring.json', 'w') as file:
                file.write(wrt[:-1].replace("'", "\"") + "]")
                file.close()
            removeFromProgress(username, removerVals, ticker, account, cost, contracts, premium)
        else:
            updateContractsPartial(username, ticker, account, type, strike, cost, contractsavailable, contracts, year, id, str(t.strftime('%m%d')), premium)
    return ""

def updateContractsPartial(username, ticker, account, type, strike, cost, contractsavailable, contracts, year, id, datetime, premium):
    wrt = "["
    removerVals = []
    with open('./data/' + username + '/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            if x['ticker'] == ticker:
                pylst = list(x['positions'][account][type])
                i = pylst.index(strike)
                coll = list(x['positions'][account]['coll'])
                x['positions'][account]['coll'][i] = str(round(int(coll[i])/int(contractsavailable))*int(int(contractsavailable) - int(contracts)))
                #x['positions'][account]['coll'][i] = str(int(round(int(coll[i])/contractsavailable))*int(contracts))
            wrt = wrt + str(x) + ","
    with open('./data/'+username+'/monitoring.json', 'w') as file:
        file.write(wrt[:-1].replace("'", "\"") + "]")
        file.close()
    with open('./data/' + username + '/progress.json', 'r') as data_file:
        data = json.loads(data_file.read())
        dt = datetime[:2] + "-" + datetime[2:]
        data[year][dt][ticker][id][6] = str(int(contractsavailable) - int(contracts))
    with open('./data/' + username + '/progress.json', 'w') as file:
        file.write(str(data).replace("'", "\""))
        file.close()
    addSubGains(username, year + "-" + datetime[:2], str(int(int(premium) - int(cost)) * int(contracts)), "-" + str(int(premium) * int(contracts)))
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

@app.route('/data/<username>/progress/gains')
def getProgressGains(username):
    ordering = []
    j1 = {}
    j2 = {}
    with open('./data/'+username+'/gains.json', 'r') as data_file:
        ordering = list(json.loads(data_file.read()))
        ordering = sorted(ordering, key=lambda d: list(d.keys()))
    with open('./data/'+username+'/gains.json', 'w') as data_file2:
        data_file2.write(str(ordering).replace("'", "\""))
        data_file2.close()
    with open('./data/'+username+'/gains.json', 'r') as data_file:
        data = list(json.loads(data_file.read()))
        found_j1 = False
        found_j2 = False
        for x in data:
            if str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date().strftime('%Y-%m')) in x.keys():
                j1 = json.loads(str(x).replace("'", "\""))
                found_j1 = True
            elif str((dt.date.today().replace(day=1) - dt.timedelta(days=-32)).strftime("%Y-%m")) in x.keys():
                j2 = json.loads(str(x).replace("'", "\""))
                found_j2 = True
        if not found_j1:
            j1 = json.loads(json.dumps(data[-2:][0]))
        if not found_j2:
            j2 = json.loads(json.dumps(data[-2:][1]))
        ret = "[['realized', 'expected'],['"
        m1 = ""
        m2 = ""
        for x in j1:
            m1 = x
            ret = ret + str(j1[x]['realized']) + "','"
            #ret = ret + str(j1[x]['unrealized']) + "','"
            ret = ret + str(j1[x]['expected']) + "'],['"
        for x in j2:
            m2 = x
            ret = ret + str(j2[x]['realized']) + "','"
            #ret = ret + str(j2[x]['unrealized']) + "','"
            ret = ret + str(j2[x]['expected']) + "'],['"
        ret = ret + m1 + "','" + m2 + "']]"
        return ret.replace("'", "\"")

@app.route('/data/<username>/progress/add/<account>/<ticker>/<contracts>/<collateral>/<exp>/<call>/<put>/<prem>')
def updateProgressData(username, account, ticker, contracts, collateral, exp, call, put, prem):
    prem = str(int(float(prem)))
    with open('./data/'+username+'/monitoring.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            if x['ticker'] == ticker:
                sz = []
                sz = x['positions'][account]['exp']
                sz_count = len(sz)
                for i in range(sz_count):
                    if x['positions'][account]['call'][i] == str(call) and x['positions'][account]['put'][i] == str(put) and x['positions'][account]['exp'][i] == str(dt.datetime.strptime(str(exp), '%Y-%m-%d').strftime('%d-%b')) and x['positions'][account]['coll'][i] == str(collateral):
                        prem = str(x['positions'][account]['prem'][i])

    year = str(exp).split('-')[0]
    month = str(exp).split('-')[1]
    day = str(exp).split('-')[2]
    date = month + "-" + day
    longcall = str(0)
    longput = str(0)

    if int(put)==0 and int(collateral)==0:
        longcall = str(0)
    elif int(put)==0 and int(collateral)!=0:
        longcall = str(float(call) + float(collateral) / 100)
    elif int(call)==0 and int(collateral)!=0:
        longput = str(float(put) - float(collateral) / 100)
    else:
        longcall = str(float(call) + float(collateral) / 100)
        longput = str(float(put) - float(collateral) / 100)

    id = year + month + day + str(ticker).upper() + str(prem)
    data = {}
    with open('./data/'+username+'/progress.json', 'r') as data_file:
        data = json.loads(data_file.read())
        isNoYear = True
        for x in data:
            if x == year:
                isNoYear = False
                if data[x].get(date):
                    for y in data[x]:
                        if y == date:
                            if data[x][y].get(ticker):
                                val = "['"+str(account)+"','" + str(
                                    int(prem) * int(contracts)) + "','" + longcall + "','" + str(
                                    call) + "','" + str(put) + "','" + longput + "','"+str(contracts)+"']"
                                data[year][date][ticker][id] = json.loads(val.replace("'", "\""))
                            else:
                                val = "{'" + id + "':['"+str(account)+"','" + str(
                                    int(prem) * int(contracts)) + "','" + longcall + "','" + str(
                                    call) + "','" + str(put) + "','" + longput + "','"+str(contracts)+"']}"
                                data[year][date][ticker] = json.loads(val.replace("'", "\""))
                else:
                    val = "{'" + ticker + "':{'" + id + "':['"+str(account)+"','" + str(
                        int(prem) * int(contracts)) + "','" + longcall + "','" + str(
                        call) + "','" + str(put) + "','" + longput + "','"+str(contracts)+"']}}"
                    data[year][date] = json.loads(val.replace("'", "\""))
        if isNoYear:
            val = "{'"+month+"-"+day+"':{'"+ticker+"':{'"+id+"':['"+str(account)+"','"+str(int(prem)*int(contracts))+"','"+longcall+"','"+str(call)+"','"+str(put)+"','"+longput+ "','"+str(contracts)+"']}}}"
            data[year] = json.loads(val.replace("'", "\""))
    with open('./data/'+username+'/progress.json', 'w') as file:
        file.write(str(data).replace("'", "\""))
        file.close()
    data2 = []
    dt_counter = 0
    with open('./data/' + username + '/gains.json', 'r') as data_file2:
        data2 = json.loads(data_file2.read())
        for vals in data2:
            for x in vals.keys():
                if str(x) == str(dt.datetime.strptime(str(exp), '%Y-%m-%d').strftime('%Y-%m')):
                    addSubGains(username, x, 0, str(int(prem)*int(contracts)))
                    dt_counter = 1
                break
        if dt_counter==0:
            gains = "{'" + str(dt.datetime.strptime(str(exp), '%Y-%m-%d').date().strftime("%Y-%m")) + "': {'realized': 0,'unrealized': 0,'expected': "+str(int(prem)*int(contracts))+"}}"
            data2.append(json.loads(gains.replace("'", "\"")))
            with open('./data/'+username+'/gains.json', 'w') as file2:
                file2.write(str(data2).replace("'", "\""))
                file2.close()
    print(str(
        "['Value:  " + account + ' - ' + ticker + ' - ' + exp + ' - ' + call + ' - ' + put + ' - ' + prem + " added successfully!']").replace(
        "'", "\""))
    return str(
        "['Value for:  " + account + ' - ' + ticker + " added successfully!']").replace(
        "'", "\"")


@app.route('/data/<username>/gains/monthly')
def getGainsDataForProgeress(username):
    ret = []
    month = []
    realized = []
    with open('./data/'+username+'/gains.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            for y in x.keys():
                month.append(y)
                realized.append(x[y]['realized'])
                break
        ret.append(month)
        ret.append(realized)
        return str(ret).replace("'", "\"")

@app.route('/data/<username>/stocks/get')
def getLongStock(username):
    data = {}
    temp_data = {}
    with open('./data/'+username+'/stocks_temp.json', 'r') as data_file3:
        temp_data = json.loads(data_file3.read())
    with open('./data/' + username + '/stocks.json', 'r') as data_file:
        data = json.loads(data_file.read())
        index = 0
        for x in data:
            try:
                shares_before = temp_data[index]['shares']
                resp = cm.getHtml("quote", data[index]['ticker'])
                if resp[0] == 200:
                    try:
                        df = parse(resp[1])
                        data[index]['current'] = df.iloc[0]['value']
                    except:
                        pass
                data[index]['pnl'] = str(round(float((float(data[index]['current']) - float(data[index]['price']))/float(data[index]['price']))*100, 2))
                data[index]['div'] = getDiv(resp[1])
                divList = divListNasdaq(data[index]['ticker'], data[index]['shares'])
                if int(shares_before) != int(data[index]['shares']):
                    data[index]['total'] = str(round(float(data[index]['pershare'])*int(data[index]['shares']), 2))
                if len(str(data[index]['date'])) == 0 and len(str(data[index]['pershare'])) == 0 and len(str(data[index]['total'])) == 0:
                    data[index]['date'] = divList[0]
                    data[index]['pershare'] = divList[1]
                    data[index]['total'] = divList[2]
                elif str(data[index]['date']) != str(divList[0]):
                    populateDividendRealized(username, data[index]['total'])
                    data[index]['date'] = divList[0]
                    data[index]['pershare'] = divList[1]
                    data[index]['total'] = divList[2]
                    #populate dividend into realized gains for current month
                index = index + 1
            except:
                pass
    with open('./data/'+username+'/stocks.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        data_file2.close()
    with open('./data/'+username+'/stocks_temp.json', 'w') as data_file3:
        data_file3.write(str(data).replace("'", "\""))
        data_file3.close()
    return str(data).replace("'", "\"")

def populateDividendRealized(username, realized):
    data2 = {}
    with open('./data/' + username + '/gains.json', 'r') as data_file2:
        data2 = json.loads(data_file2.read())
        dt_counter = 0
        check = 0
        for vals in data2:
            for x in vals.keys():
                if str(x) == str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').strftime('%Y-%m')):
                    try:
                        check = 1
                        data2[dt_counter][x]['realized'] = str(round(float(data2[dt_counter][x]['realized']) + float(realized)))
                        break
                    except:
                        pass
            dt_counter = dt_counter + 1
        if check == 0:
            gains = "{'" + str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date().strftime("%Y-%m")) + "': {'realized': "+str(round(float(realized)))+",'unrealized': 0,'expected': 0}}"
            data2.append(json.loads(gains.replace("'", "\"")))
            with open('./data/' + username + '/gains.json', 'w') as file2:
                file2.write(str(data2).replace("'", "\""))
                file2.close()
    with open('./data/'+username+'/gains.json', 'w') as file2:
        file2.write(str(data2).replace("'", "\""))
        file2.close()

def divListNasdaq(stock, shares):
    try:
        req = r.get("https://finance.yahoo.com/quote/"+stock+"/history?filter=div&frequency=1d&includeAdjustedClose=true").text
        soup = BeautifulSoup(req, 'html.parser')
        l1 = soup.select(y.yahoo_dividend_table_first())
        l4 = soup.select(y.yahoo_dividend_table_fourth())
        return [str(l4[0].text.split(" ")[0] + " " + l4[0].text.split(" ")[1])[:-1], str(l1[1].text).split(" ")[0], str(round(float(str(l1[1].text).split(" ")[0])*float(shares), 2))]
    except:
        return ["Err", "Err", "0"]

@app.route('/data/<username>/stocks/get/temp')
def getLongStockTemp(username):
    data = {}
    with open('./data/'+username+'/stocks.json', 'r') as data_file:
        data = json.loads(data_file.read())
    with open('./data/'+username+'/stocks_temp.json', 'w') as data_file2:
        data_file2.write(str(data).replace("'", "\""))
        data_file2.close()
    return str(data).replace("'", "\"")

@app.route('/data/<username>/stocks/<stock>/<price>/<account>/<shares>')
def addLongStock(username, stock, price, account, shares):
    data = []
    counter = 0
    index = 0
    with open('./data/' + username + '/stocks.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for x in data:
            if str(x['ticker']) == str(stock) and str(x['account']) == str(account):
                data[index]['price'] = str(round((float(data[index]['price'])*float(data[index]['shares']) + float(price)*float(shares))/(int(shares) + int(data[index]['shares'])), 2))
                data[index]['shares'] = str(int(data[index]['shares']) + int(shares))
                counter = 1
                break
            index = index + 1
        if counter ==0:
            gains = "{'ticker': '"+stock+"', 'price':'"+price+"', 'account':'"+account+"', 'pnl': '','shares': '"+shares+"','current': '','div': '','date': '','pershare': '','total': ''}"
            data.append(json.loads(gains.replace("'", "\"")))
    with open('./data/'+username+'/stocks.json', 'w') as file2:
        file2.write(str(data).replace("'", "\""))
        file2.close()
    return str(data).replace("'", "\"")

@app.route('/data/<username>/delstocks/<stock>/<account>/<shares>')
def delLongStock(username, stock, account, shares):
    data = []
    with open('./data/' + username + '/stocks.json', 'r') as data_file:
        data = json.loads(data_file.read())
        index = 0
        for x in data:
            if x['ticker'] == stock and int(shares) >= int(x['shares']) and x['account'] == account:
                data.pop(index)
            elif x['ticker'] == stock and int(shares) < int(x['shares']) and x['account'] == account:
                data[index]['shares'] = str(int(data[index]['shares']) - int(shares))
            index = index + 1
    with open('./data/'+username+'/stocks.json', 'w') as file2:
        file2.write(str(data).replace("'", "\""))
        file2.close()
    return str(data).replace("'", "\"")

def removeFromProgress(username, removerVals, ticker, account, cost, contracts, premium):
    data = {}
    ret = "["
    year = ""
    with open('./data/'+username+'/progress.json', 'r') as data_file:
        data = json.loads(data_file.read())
        t = dt.datetime.strptime(str(removerVals[2]), '%d-%b')
        for y in data:
            try:
                id = str(y) + str(t.strftime('%m%d')) + ticker.upper() + str(removerVals[4])
                del data[str(y)][str(t.strftime('%m-%d'))][str(ticker)][id]
                year = str(y)
                if len(str(data[year][str(t.strftime('%m-%d'))][str(ticker)])) < 4:
                    del data[year][str(t.strftime('%m-%d'))][str(ticker)]
                    if len(str(data[year][str(t.strftime('%m-%d'))])) < 4:
                        del data[year][str(t.strftime('%m-%d'))]
            except:
                pass
        addSubGains(username, year + "-" + str(t.strftime('%m')), str(int(int(premium) - int(cost))*int(contracts)), "-"+str(int(premium)*int(contracts)))
    with open('./data/'+username+'/progress.json', 'w') as file:
        file.write(str(data).replace("'", "\""))
        file.close()
    return ""

def addSubGains(username, yearmonth, realizedcost, expectedcost):
    data = []
    index = 0
    with open('./data/' + username + '/gains.json', 'r') as data_file2:
        data = json.loads(data_file2.read())
        for x in data:
            for k in x.keys():
                if k == yearmonth:
                    data[index][yearmonth]['realized'] = int(x[yearmonth]['realized']) + int(realizedcost)
                    data[index][yearmonth]['expected'] = int(x[yearmonth]['expected']) + int(expectedcost)
            index = index + 1
    with open('./data/'+username+'/gains.json', 'w') as file2:
        file2.write(str(data).replace("'", "\""))
        file2.close()
    return str(data).replace("'", "\"")

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    dict = {'value':soup.select(y.current_value())[0].text}
    l = soup.select(y.quote_table())
    data = [j.text for j in l]
    for i in range(0, len(data), 2):
        dict[data[i]] = data[i+1:i+2]

    df = pd.DataFrame(dict)
    return df

def getDiv(html):
    soup = BeautifulSoup(html, 'html.parser')
    l = soup.select(y.quote_table_right_vals())
    index = 0
    for vals in l:
        if "Yield" in vals.text:
            return l[index + 1].text
        index = index + 1
    return "NA"

def options(tickers):
    resp = cm.getHtml("quote", tickers)
    price = 0.0
    if resp[0] == 200:
        try:
            df = parse(resp[1])
            price = float(df.iloc[0]['value'].replace(',', ''))
        except Exception:
            #print(traceback.format_exc())
            pass
    return str(price)


#Not being used now
#@app.route('/data/<username>/progress/close')
def closeExpired(username):
    counter = 0
    with open('./data/'+username+'/progress.json', 'r') as data_file:
        data = json.loads(data_file.read())
        for y in data:
            for d in data[y]:
                for t in data[y][d]:
                    for id in data[y][d][t]:
                        nowDate = dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date()
                        tradeDate = dt.datetime.strptime(str(y)+'-'+str(d), '%Y-%m-%d').date()
                        if tradeDate<nowDate:
                            counter = counter + 1
                            returnMonitoringDelStrike(t, list(data[y][d][t][id])[0], 'call', list(data[y][d][t][id])[3], 0, list(data[y][d][t][id])[6])
    print("Closed "+str(counter)+" trades!")
    return str("['Closed "+str(counter)+" trades! Please refresh!!']").replace("'", "\"")

#Not being used now
#@app.route('/data/<username>/progress/current')
def getProgressData(username):
    with open('./data/'+username+'/progress.json', 'r') as data_file:
        data = json.loads(data_file.read())
        ret = "["
        for y in data:
            year = y[-2:]
            for d in data[y]:
                date = str(d).replace("-", "")
                for t in data[y][d]:
                    ticker = t
                    for id in data[y][d][t]:
                        counter = 0
                        lst = []
                        for x in list(data[y][d][t][id]):
                            if counter==2 or counter==3:
                                strike = float(data[y][d][t][id][counter])
                                try:
                                    if len(str(strike).split(".")[0]) == 1:
                                        lst.append(int(float((options(str(ticker+year+date+"C0000"+str(int(strike*1000))))))*100))
                                    elif len(str(strike).split(".")[0]) == 2:
                                        lst.append(int(float((options(str(ticker+year+date+"C000"+str(int(strike*1000))))))*100))
                                    elif len(str(strike).split(".")[0]) == 3:
                                        lst.append(int(float((options(str(ticker+year+date+"C00"+str(int(strike*1000))))))*100))
                                    elif len(str(strike).split(".")[0]) == 4:
                                        lst.append(int(float((options(str(ticker+year+date+"C0"+str(int(strike*1000))))))*100))
                                except Exception:
                                    lst.append("0")
                                    #print(traceback.format_exc())
                                    pass
                                counter = counter + 1
                            elif counter == 4 or counter == 5:
                                strike = float(data[y][d][t][id][counter])
                                try:
                                    if len(str(strike).split(".")[0]) == 1:
                                        lst.append(int(float((options(
                                            str(ticker + year + date + "P0000" + str(int(strike * 1000)))))) * 100))
                                    elif len(str(strike).split(".")[0]) == 2:
                                        lst.append(int(float((options(
                                            str(ticker + year + date + "P000" + str(int(strike * 1000)))))) * 100))
                                    elif len(str(strike).split(".")[0]) == 3:
                                        lst.append(int(float((options(
                                            str(ticker + year + date + "P00" + str(int(strike * 1000)))))) * 100))
                                    elif len(str(strike).split(".")[0]) == 4:
                                        lst.append(int(float((options(
                                            str(ticker + year + date + "P0" + str(int(strike * 1000)))))) * 100))
                                except Exception:
                                    lst.append("0")
                                    #print(traceback.format_exc())
                                    pass
                                counter = counter + 1
                            elif counter == 6:
                                lst = [ele*float(data[y][d][t][id][counter]) for ele in lst]
                                break
                            else:
                                counter = counter + 1
                        cur = int((float(lst[1]) - float(lst[0])) + (float(lst[2]) - float(lst[3])))
                        pnl = int(int(data[y][d][t][id][1]) - cur)
                        perc = (int(data[y][d][t][id][1]) - cur)*100/int(data[y][d][t][id][1])
                        ret = ret + "['"+ data[y][d][t][id][0]+"','"+t+"','"+str(data[y][d][t][id][3] + "-" + data[y][d][t][id][4])+"','"+str(y+"-"+d)+"','"+data[y][d][t][id][1]+"','"+str(cur)+"','"+str(pnl)+"','"+ str(round(perc, 2)) + "'],"

        data2 = json.loads(str(ret[:-1]+"]").replace("'", "\""))
        ur = {}
        expect = {}
        for vals in data2:
            if str(vals[3])[:-3] in ur:
                ur[str(vals[3])[:-3]] = int(ur[str(vals[3])[:-3]]) + int(vals[6])
                expect[str(vals[3])[:-3]] = int(expect[str(vals[3])[:-3]]) + int(vals[4])
            else:
                ur[str(vals[3])[:-3]] = int(vals[6])
                expect[str(vals[3])[:-3]] = int(vals[4])
        with open('./data/'+username+'/gains.json', 'r') as data_file2:
            data3 = json.loads(data_file2.read())
            for vals in ur:
                isFound = False
                counter = 0
                for d in data3:
                    for date in data3[counter]:
                        if str(date) == str(vals):
                            data3[counter][date]['unrealized'] = ur[vals]
                            data3[counter][date]['expected'] = expect[vals]
                            isFound = True
                    counter = counter + 1
                if isFound==False:
                    data3.append({str(vals): {'realized':0, 'unrealized':ur[vals], 'expected':expect[vals]}})
            with open('./data/'+username+'/gains.json', 'w') as file2:
                file2.write(str(data3).replace("'", "\""))
                file2.close()
        return str(ret[:-1]+"]").replace("'", "\"")

