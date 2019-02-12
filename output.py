'''
Author: Manu Babanu
Date: 09/04/2018
Description: Script to run the app and render all log values into html
 pageself.Table with logs, most used ip, geolocation, most
 common/least domain ...
'''

from flask import Flask, render_template, url_for
from getLst import *
import os

app = Flask(__name__)


# initiate the flask
script = Flask(__name__)


# route for homepage
@app.route('/')
def homepage():

    # change to directory
    folder = os.path.abspath(os.path.dirname(__file__))
    ze_path = folder + '/20140315/http.log'

    # get fields and values from all files
    nestLst, fieldsLst,  ipLst, mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)

    # dictionary for geolocation records
    recordDict = {}
    setipLst = set(ipLst)
    # returns dicitonary with records for ip with more than 2 occurences
    for ip in setipLst:
        if ipLst.count(ip) > 2:
            record = ipLocator(ip)
            recordDict[ip] = record
    agentList = []
    for agent in nestLst:
        agentList.append(agent[11])
    setAgentLst = set(agentList)

    # dictionary for user agent and occurences count
    agentDict = {}
    for agent in setAgentLst:
        if agentList.count(agent) >= 1:
            agentCount = agentList.count(agent)
            agentDict[agent] = agentCount
    # most used domain dictionary with counter for occurences
    domainDict = {}
    for domain in mostDomLst:
        if mostDomLst.count(domain) >= 1:
            domainCount = mostDomLst.count(domain)
            domainDict[domain] = domainCount

    # most active private and public IP
    privIPLst = []
    for ip in nestLst:
        privIPLst.append(ip[2])
    setPrivIP = set(privIPLst)

    return render_template("homepage.html", nestLst=nestLst,
                           fieldsLst=fieldsLst, ipLst=ipLst, ipLstSet=ipLstSet,
                           record=record, recordDict=recordDict,
                           agentDict=agentDict, domainDict=domainDict, setPrivIP=setPrivIP, privIPLst=privIPLst)


# route for page where conn.log is analyzed
@app.route('/connpage/')
def connpage():

    # change to directory
    folder = os.path.abspath(os.path.dirname(__file__))
    ze_path = folder + '/20140315/conn.log'

    # get fields and values from all files
    nestLst, fieldsLst,  ipLst,  mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)
    # dictionary for ip with most occurences for geolocation
    recordDict = {}
    setipLst = set(ipLst)
    for ip in setipLst:
        if ipLst.count(ip) > 2:
            record = ipLocator(ip)
            recordDict[ip] = record
    return render_template("connpage.html", nestLst=nestLst, fieldsLst=fieldsLst, ipLst=ipLst, ipLstSet=ipLstSet, record=record, recordDict=recordDict)


# route for page whre dns.log is analyzed
@app.route('/dnspage/')
def dnspage():

    # upload folder
    folder = os.path.abspath(os.path.dirname(__file__))
    ze_path = folder + '/20140315/dns.log'

    # get fields and values from all files
    nestLst, fieldsLst,  ipLst,  mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)
    # dictionary for ip with most occurences for geolocation
    recordDict = {}
    setipLst = set(ipLst)
    for ip in setipLst:
        if ipLst.count(ip) >= 2:
            record = ipLocator(ip)
            recordDict[ip] = record
    return render_template("dnspage.html", nestLst=nestLst, fieldsLst=fieldsLst, ipLst=ipLst, ipLstSet=ipLstSet, record=record, recordDict=recordDict)

# route for page whre dns.log is analyzed


@app.route('/dhcppage/')
def dhcppage():

    # upload folder
    folder = os.path.abspath(os.path.dirname(__file__))
    ze_path = folder + '/20140315/dhcp.log'

    # get fields and values from all files
    nestLst, fieldsLst,  ipLst, mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)
    # dictionary for ip with most occurrences for geolocation
    recordDict = {}
    setipLst = set(ipLst)
    for ip in setipLst:
        if ipLst.count(ip) >= 2:
            record = ipLocator(ip)
            recordDict[ip] = record

    #  use the mac_info to get the company manufacturer of nic card from mac Address
    nicList = []
    for nic in nestLst:
        nicList.append(nic[6])
        company = mac_info(nic[6])
    setNicList = set(nicList)

    return render_template("dhcppage.html", nestLst=nestLst, fieldsLst=fieldsLst, setNicList=setNicList, company=company)


#  funny about page
@app.route('/about/')
def about():
    return render_template("about.html")


#  run the page
if __name__ == "__main__":
    app.run()
