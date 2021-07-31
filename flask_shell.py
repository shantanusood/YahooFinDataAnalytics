from flask import Flask, request, redirect, url_for, render_template
import re
import time
import datetime as dt
from datetime import timedelta
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
from src.helpers import calendar as cl
from data import tickers_list as tl
import traceback
import collections
import requests as r
from src.mongo import Connect as con
from bson.json_util import dumps

app = Flask(__name__)
CORS(app)

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

@app.route('/data/<username>/getit')
def getit(username):
    st = list(username)
    st_num = ""
    for x in st:
        st_num = st_num + str(int(str(ord(x)-96)[-1:])*2)[-1:]
    return str("{'this':'"+str(int(str(st_num)[0])*3)[-1:] + str(st_num)[1:5] + str(int(str(st_num)[5])*3)[-1:]+"'}").replace("'", "\"")

@app.route("/data/roles/get")
def getRoles():
    return str(json.loads(dumps(con.getCollection("Roles").find()))).replace("'", "\"").replace("_id", "userid")

@app.route("/data/roles/change/<username>/<newrole>")
def changeRole(username, newrole):
    con.getCollection("Roles").find_one_and_update({"_id": username}, {"$set": {"role": newrole}})
    return str(json.loads(dumps(con.getCollection("Roles").find()))).replace("'", "\"")

@app.route("/data/roles/updateqa/<username>", methods=['GET', 'POST'])
def updateQA(username):
    con.getCollection("Roles").find_one_and_update({"_id": username}, {"$set": {"question": request.json['question']}})
    con.getCollection("Roles").find_one_and_update({"_id": username}, {"$set": {"answer": request.json['answer']}})
    return str(json.loads(dumps(con.getCollection("Roles").find()))).replace("'", "\"")

@app.route("/data/roles/changestatus/<username>/<status>")
def changeUserStatus(username, status):
    con.getCollection("Roles").find_one_and_update({"_id": username}, {"$set": {"status": status}})
    return str(json.loads(dumps(con.getCollection("Roles").find()))).replace("'", "\"")

@app.route("/data/bug/get")
def getBugFeature():
    return str(json.loads(dumps(con.getCollection("Bug_feature").find()))[0]['bug_feature']).replace("'", "\"")

@app.route("/data/bug/add/<type>", methods=['GET', 'POST'])
def addBugFeature(type):
    data = json.loads(dumps(con.getCollection("Bug_feature").find()))[0]['bug_feature']
    addthis = data[type]
    addthis.insert(0, request.json)
    data[type] = addthis
    con.getCollection("Bug_feature").find_one_and_update({"_id": "bug_feature"}, {"$set": {"bug_feature": data}})
    return json.loads(dumps(con.getCollection("Bug_feature").find()))[0]['bug_feature']

@app.route("/data/bug/delete/<type>", methods=['GET', 'POST'])
def deleteBugFeature(type):
    data = json.loads(dumps(con.getCollection("Bug_feature").find()))[0]['bug_feature']
    addthis = data[type]
    addthis.remove(request.json)
    data[type] = addthis
    con.getCollection("Bug_feature").find_one_and_update({"_id": "bug_feature"}, {"$set": {"bug_feature": data}})
    return json.loads(dumps(con.getCollection("Bug_feature").find()))[0]['bug_feature']

@app.route("/data/notifications/get")
def getNotification():
    return str(json.loads(dumps(con.getCollection("Notifications").find()))[0]['notifications']).replace("'", "\"")

@app.route("/data/notifications/add", methods=['GET', 'POST'])
def captureNotification():
    data = json.loads(dumps(con.getCollection("Notifications").find()))[0]['notifications']
    data.append(request.json['data'])
    con.getCollection("Notifications").find_one_and_update({"_id": "notifications"}, {"$set": {"notifications": data}})
    return str(json.loads(dumps(con.getCollection("Notifications").find()))[0]['notifications']).replace("'", "\"")

@app.route("/data/notifications/delete", methods=['GET', 'POST'])
def delNotification():
    data = json.loads(dumps(con.getCollection("Notifications").find()))[0]['notifications']
    data.remove(request.json['data'])
    con.getCollection("Notifications").find_one_and_update({"_id": "notifications"}, {"$set": {"notifications": data}})
    return str(json.loads(dumps(con.getCollection("Notifications").find()))[0]['notifications']).replace("'", "\"")

@app.route("/data/subscriber/add", methods=['GET', 'POST'])
def addToSubscriber():
    data = json.loads(dumps(con.getCollection("Subscribers").find()))[0]['subscribers']
    data.append(request.json)
    con.getCollection("Subscribers").find_one_and_update({"_id": "subscribers"}, {"$set": {"subscribers": data}})
    strx = "User "+ request.json['username'] + " with paypal " + request.json['paypal'] + " clicked on subscribe at " + request.json['datetime']
    data2 = json.loads(dumps(con.getCollection("Notifications").find()))[0]['notifications']
    data2.append(strx)
    con.getCollection("Notifications").find_one_and_update({"_id": "notifications"}, {"$set": {"notifications": data}})
    return ""

@app.route('/data/<username>/updatedmycontact/<email>/<phone>')
def updateContact(username, email, phone):
    data = json.loads(dumps(con.getCollection("PayHist").find()))[0]['hist']
    data['email'] = email
    data['phone'] = phone
    con.getCollection("PayHist").find_one_and_update({"_id": username}, {"$set": {"hist": data}})
    return str(data).replace("'", "\"")

@app.route('/data/<username>/accounts')
def readRawData(username):
    data = json.loads(dumps(con.getCollection("Accounts").find({"_id": str(username)})))[0]['accounts']
    final_data = {}
    for x in data:
        final_data[x['name_id']] = x['name']
    return str(final_data).replace("'", "\"")

@app.route('/data/<username>/accounts/colors')
def accountColors(username):
    data = json.loads(dumps(con.getCollection("Accounts").find({"_id": str(username)})))[0]['accounts']
    final_data = {}
    for x in data:
        final_data[x['name']] = x['color']
    return str(final_data).replace("'", "\"")

@app.route("/data/<username>/accounts/add", methods=['GET', 'POST'])
def addAccounts(username):
    data = json.loads(dumps(con.getCollection("Accounts").find({"_id": str(username)})))[0]['accounts']
    dict_add ={
        "id": int(data[-1]['id']) + 1,
        "name_id": request.json['acc_name'],
        "name": request.json['acc_value'],
        "color": "wheat",
    }
    data.append(dict_add)
    con.getCollection("Accounts").find_one_and_update({"_id": username}, {"$set": {"accounts": data}})
    return readRawData(username)

@app.route("/data/<username>/accounts/delete/<account>", methods=['GET', 'POST'])
def delAccounts(username, account):
    data = json.loads(dumps(con.getCollection("Accounts").find({"_id": str(username)})))[0]['accounts']
    acc_num = int(str(account).split("_")[1])
    toBePoped = {}
    for x in data:
        if str(account) == x['name_id']:
            toBePoped = x
            break
    data.remove(toBePoped)
    count = 1
    acc_count = 0
    for acc in data:
        if count >= acc_num:
            data[acc_count]['name_id'] = "account_" + str(count)  
        acc_count = acc_count + 1
        count = count + 1
    con.getCollection("Accounts").find_one_and_update({"_id": username}, {"$set": {"accounts": data}})
    return readRawData(username)

@app.route("/data/<username>/accounts/update/<account>", methods=['GET', 'POST'])
def updateAccount(username, account):
    data = json.loads(dumps(con.getCollection("Accounts").find({"_id": str(username)})))[0]['accounts']
    count = 0
    for x in data:
        if str(account) in x['name_id']:
            data[count]['name'] = request.json['name']
            break
        count = count + 1
    con.getCollection("Accounts").find_one_and_update({"_id": username}, {"$set": {"accounts": data}})
    return readRawData(username)

@app.route('/data/<username>/accounts/<account1>/<account2>/<account3>')
def updateAccounts(username, account1, account2, account3):
    data = json.loads(dumps(con.getCollection("Accounts").find({"_id": str(username)})))[0]['accounts']
    count = 0
    for x in data:
        if "fidelity" in x['name_id']:
            data[count]['name'] = account1
        elif "robinhood" in x['name_id']:
            data[count]['name'] = account2
        elif "tastyworks" in x['name_id']:
            data[count]['name'] = account3
        count = count + 1
    con.getCollection("Accounts").find_one_and_update({"_id": username}, {"$set": {"accounts": data}})
    return "['Successfully wrote to accounts!']".replace("'", "\"")

@app.route('/data/<username>/daily')
def dailyProgress(username):
    return str(json.loads(dumps(con.getCollection("Progress").find({"_id": str(username)})))[0]['daily']).replace("'", "\"")

@app.route('/data/<username>/daily/<fidelity>/<robinhood>/<tastyworks>/<retirement>/<fidelityc>/<robinhoodc>/<tastyworksc>/<retirementc>')
def dailyProgressModify(username, fidelity, robinhood, tastyworks, retirement, fidelityc, robinhoodc, tastyworksc, retirementc):
    wrt = "["
    data_lst = []
    data = json.loads(dumps(con.getCollection("Progress").find({"_id": str(username)})))[0]['daily']
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
        con.getCollection("Progress").find_one_and_update({"_id": username}, {"$set": {"daily": data_lst}})
        return "['SUCCESS']".replace("'", "\"")
    else:
        return "['Duplicate edit instead']".replace("'", "\"")

@app.route('/data/<username>/daily/get')
def getDailyProgressRecent(username):
    wrt = "["
    data_lst = []
    data = json.loads(dumps(con.getCollection("Progress").find({"_id": str(username)})))[0]['daily']
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
    print(datec)
    data = json.loads(dumps(con.getCollection("Progress").find({"_id": str(username)})))[0]['daily']
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
    con.getCollection("Progress").find_one_and_update({"_id": username}, {"$set": {"daily": data}})
    return "DONE"

@app.route('/data/<username>/deletedaily', methods=["GET", "POST"])
def dailyProgressDeleteRecent(username):
    wrt = "["
    data_lst = []
    data = json.loads(dumps(con.getCollection("Progress").find({"_id": str(username)})))[0]['daily']
    data_lst = list(data)
    i = data_lst[0]['date'].index(request.json['date'])
    data_lst[0]['date'].pop(i)
    data_lst[1]['fidelity'].pop(i)
    data_lst[2]['robinhood'].pop(i)
    data_lst[3]['tastyworks'].pop(i)
    data_lst[4]['retirement'].pop(i)
    data_lst[5]['total'].pop(i)
    data = data_lst
    con.getCollection("Progress").find_one_and_update({"_id": username}, {"$set": {"daily": data}})
    return "DONE"

@app.route('/data/<username>/daily/<index>/<type>/<filter>')
def filterHistData(username, index, type, filter):
    data = json.loads(dumps(con.getCollection("Progress").find({"_id": str(username)})))[0]['daily']
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

################################################################################
###################################RENTAL#######################################
################################################################################
@app.route('/data/<username>/rental/addquotes')
def send_rent_quotes(username):
    data = json.loads(dumps(con.getCollection("PayHist").find({"_id": username})))[0]['hist']
    history = data['history']
    val = "{'due_date': '" + str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date())[
                             :-2] + "01" + "', 'paid_date': 'NA', 'rent': '" + str(
        data['recurring']) + "', 'utilities': '0', 'late': '0', 'additional': '0', 'total': '" + str(
        data['recurring']) + "', 'status': 'N'}"
    jval = json.loads(val.replace("'", "\""))
    history.insert(0, jval)
    data['history'] = history
    con.getCollection("PayHist").find_one_and_update({"_id": username}, {"$set": {"hist": data}})
    return "['Successfully wrote to accounts!']".replace("'", "\"")

@app.route('/data/<username>/rental/editquotes/<delete_or_edit>/<due_date>/<paid_date>/<rent>/<utilities>/<late>/<additional>/<total>/<status>')
def edit_rent_quotes(username, delete_or_edit, due_date, paid_date, rent, utilities, late, additional, total, status):
    data = {}
    history = []
    index = 0
    data = json.loads(dumps(con.getCollection("PayHist").find({"_id": username})))[0]['hist']
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
    con.getCollection("PayHist").find_one_and_update({"_id": username}, {"$set": {"hist": data}})
    return "['Successfully wrote to accounts!']".replace("'", "\"")

@app.route('/data/<username>/rental/history')
def payment_history(username):
    return json.loads(dumps(con.getCollection("PayHist").find({"_id": username})))[0]['hist']

@app.route('/data/<username>/rental/outstanding')
def outstanding(username):
    total_out = 0
    data = json.loads(dumps(con.getCollection("PayHist").find({"_id": username})))[0]['hist']
    for hist in data['history']:
        if hist['status'] == 'N':
            total_out = total_out + int(hist['total'])
    return str(total_out)

@app.route('/data/<username>/rental/extend/<period>')
def extention(username, period):
    data = {}
    total_out = 0
    data = json.loads(dumps(con.getCollection("PayHist").find({"_id": username})))[0]['hist']
    data['request'] = period
    con.getCollection("PayHist").find_one_and_update({"_id": username}, {"$set": {"hist": data}})
    return data

@app.route('/data/<username>/rental/extend/approve/<period>')
def extentionApprove(username, period):
    data = json.loads(dumps(con.getCollection("PayHist").find({"_id": username})))[0]['hist']
    data['request'] = "false"
    data['expiry'] = period
    con.getCollection("PayHist").find_one_and_update({"_id": username}, {"$set": {"hist": data}})
    return data

@app.route("/properties/add", methods=["POST"])
def addNewProperty():
    val = "{'_id': '"+request.json['name']+"', 'address': '"+request.json['address']+"', 'workorders': []}"
    jval = json.loads(val.replace("'", "\""))
    con.getCollection("Properties").insert_one(jval)
    return "['Successfully created new property']".replace("'", "\"")

@app.route("/properties/get")
def getAllProperties():
    return str(con.getCollection("Properties").find().distinct('_id')).replace("'", "\"")

@app.route("/properties/<properties>/get")
def getProperty(properties):
    return str(json.loads(dumps(con.getCollection("Properties").find({"_id": properties})))[0]).replace("'", "\"")

@app.route("/properties/<properties>/workorder", methods=['GET', 'POST'])
def createWorkOrder(properties):
    data = json.loads(dumps(con.getCollection("Properties").find({"_id": properties})))[0]        
    workorder = data['workorders']
    workorder.insert(0, request.json)
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"workorders": workorder}})
    return str(data).replace("'", "\"")

@app.route("/properties/inprogress")
def getAllInprogress():
    final_data = []
    onlyfiles = con.getCollection("Properties").find().distinct('_id')
    for file in onlyfiles:
        data = json.loads(dumps(con.getCollection("Properties").find({"_id": file})))[0]
        for x in data['workorders']:
                if(x['status'] == 'In progress'):
                    final_data.append(x)
    return str(final_data).replace("'", "\"")

@app.route("/properties/workorder/delete", methods=['GET', 'POST'])
def getDelete():
    onlyfiles = con.getCollection("Properties").find().distinct('_id')
    for file in onlyfiles:
        data = json.loads(dumps(con.getCollection("Properties").find({"_id": file})))[0]
        lst_data = data['workorders']
        index = 0
        for x in lst_data:
            if (x['address'] == request.json['address'] and x['submitdate'] == request.json['time']):
                lst_data.pop(index)
                data['workorders'] = lst_data
                break
            index = index + 1
        con.getCollection("Properties").find_one_and_update({"_id": file}, {"$set": {"workorders": lst_data}})
    return str(['Successfully deleted']).replace("'", "\"")

@app.route("/properties/workorder/completed", methods=['GET', 'POST'])
def getMarkCompleted():
    onlyfiles = con.getCollection("Properties").find().distinct('_id')
    for file in onlyfiles:
        data = json.loads(dumps(con.getCollection("Properties").find({"_id": file})))[0]
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
        con.getCollection("Properties").find_one_and_update({"_id": file}, {"$set": {"workorders": lst_data}})
    return str(['Successfully changed to completed']).replace("'", "\"")

@app.route("/properties/workorder/inprogress", methods=['GET', 'POST'])
def getMarkProgress():
    onlyfiles = con.getCollection("Properties").find().distinct('_id')
    for file in onlyfiles:
        data = json.loads(dumps(con.getCollection("Properties").find({"_id": file})))[0]
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
        con.getCollection("Properties").find_one_and_update({"_id": file}, {"$set": {"workorders": lst_data}})
    return str(['Successfully changed to in progress']).replace("'", "\"")

@app.route("/data/<username>/updatetenant", methods=['GET', 'POST'])
def updateTenant(username):
    data = json.loads(dumps(con.getCollection("PayHist").find({"_id": username})))[0]['hist']
    data['propetyname'] = request.json['propetyname']
    prop = json.loads(dumps(con.getCollection("Properties").find({"_id": data['propetyname']})))[0]
    data['address'] = prop['address']
    data['recurring'] = request.json['recurring']
    data['deposit'] = request.json['deposit']
    data['durations'] = request.json['durations'].split(",")
    data['status'] = request.json['status']
    data['email'] = request.json['email']
    data['phone'] = request.json['phone']
    data['expiry'] = request.json['expiry']
    con.getCollection("PayHist").find_one_and_update({"_id": username}, {"$set": {"hist": data}})
    return str(data).replace("'", "\"")

@app.route("/properties/<properties>/update", methods=['GET', 'POST'])
def updateProperty(properties):
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"address": request.json['address']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"image": request.json['image']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"desc": request.json['desc']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"circuitbreaker": request.json['circuitbreaker']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"watermain": request.json['watermain']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"alarm'": request.json['alarm']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"fire": request.json['fire']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"centralheat": request.json['centralheat']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"heatage": request.json['heatage']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"pet": request.json['pet']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"police": request.json['police']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"hospital": request.json['hospital']}})
    con.getCollection("Properties").find_one_and_update({"_id": properties}, {"$set": {"dmv": request.json['dmv']}})
    return "['Successfully wrote to accounts!']".replace("'", "\"")

################################################################################
###########################CREATE AND DELETE USER###############################
################################################################################
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
    gains = "[{'"+  str((dt.date.today().replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")) +"': {'realized': 0,'unrealized': 0,'expected': 0}},{'"+ str(dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d').date().strftime("%Y-%m"))+"': {'realized': 0,'unrealized': 0,'expected': 0}}]"
    monitoring = "[{'ticker': 'spy','price': '59.42','total': 0,'positions': {'fidelity': {'call': ['63'],'put': ['0'],'exp': ['18-Sep'],'coll': ['0'],'prem': ['42']},'robinhood': {'call': [],'put': [],'exp': [],'coll': [],'prem': []},'tastyworks': {'call': [],'put': [],'exp': [],'coll': [],'prem': []}},'ordered': {'call': [{'63': ['fidelity','18-Sep','0','42','6.02']}],'put': [{'0': ['fidelity','18-Sep','0','42','100.0']}]}}]"
    progress = "{}"
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
