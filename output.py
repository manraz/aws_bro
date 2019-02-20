'''
Author: Manu Babanu
Date: 09/04/2018
Description: Script to run the app and render all log values into html
 pageself.Table with logs, most used ip, geolocation, most
 common/least domain ...
'''

from flask import Flask, render_template, flash, redirect, request, session, abort
from getLst import *
import os
import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)

folder = os.path.abspath(os.path.dirname(__file__))
# ze_path = folder + '/20110919/http.log'
# route for homepage
@app.route('/')
def homepage():
    ze_path = os.path.join(folder, '20110919/http.log')
    # get fields and values from all files
    nestLst, fieldsLst, ipLst, mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)

    # dictionary for geolocation records
    recordDict = {}
    # returns dicitonary with records for ip with more than 2 occurences
    for ip in ipLstSet:
        if ipLst.count(ip) > 2:
            record = ipLocator(ip)
            recordDict[ip] = record
    agentList = []
    for agent in nestLst:
        agentList.append(agent[11])
    setAgentLst = set(agentList)

    # dictionary for user agent and occurrences count
    agentDict = {}
    for agent in setAgentLst:
        if agentList.count(agent) >= 1:
            agentCount = agentList.count(agent)
            agentDict[agent] = agentCount
    # most used domain dictionary with counter for occurrences
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

    ipnumber = []
    hits = []

    def build_pie_most_ip():
        for ip in ipLstSet:
            if ipLst.count(ip) >= 1:
                ipnumber.append(ip)
                hits.append(ipLst.count(ip))

        if hits.__len__() < 10:
            plt.axis('equal')
            plt.pie(hits, labels=ipnumber, autopct='%1.1f%%', shadow=True, startangle=140)
            plt.title('Most used IP\'s')
            plt.savefig('static/images/most_priv_ip.png')
        else:
            y_pos = np.arange(len(ipnumber))
            width = 0.5
            plt.figure(figsize=(10, 4))
            plt.barh(y_pos, hits, width, align='center', alpha=1)
            plt.yticks(y_pos, ipnumber)
            plt.xlabel('Count')
            plt.title('Most used IP\'s')
            plt.savefig('static/images/most_priv_ip.png')
    build_pie_most_ip()

    return render_template("homepage.html", nestLst=nestLst,
                           fieldsLst=fieldsLst, ipLst=ipLst, ipLstSet=ipLstSet,
                           record=record, recordDict=recordDict,
                           agentDict=agentDict, domainDict=domainDict, setPrivIP=setPrivIP, privIPLst=privIPLst,
                           name='Most Active Public IP', url='/../static/images/most_priv_ip.png')


# route for page where conn.log is analyzed
@app.route('/connpage/')
def connpage():
    # get fields and values from all files
    ze_path = os.path.join(folder, '20110919/conn.log')
    nestLst, fieldsLst, ipLst, mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)
    # dictionary for ip with most occurences for geolocation
    recordDict = {}
    for ip in ipLstSet:
        if ipLst.count(ip) > 2:
            record = ipLocator(ip)
            recordDict[ip] = record
    return render_template("connpage.html", nestLst=nestLst, fieldsLst=fieldsLst, ipLst=ipLst, ipLstSet=ipLstSet,
                           record=record, recordDict=recordDict)


# route for page whre dns.log is analyzed
@app.route('/dnspage/')
def dnspage():
    # get fields and values from all files
    ze_path = os.path.join(folder, '20110919/dns.log')
    nestLst, fieldsLst, ipLst, mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)
    # dictionary for ip with most occurences for geolocation
    recordDict = {}
    for ip in ipLstSet:
        if ipLst.count(ip) >= 2:
            record = ipLocator(ip)
            recordDict[ip] = record
    return render_template("dnspage.html", nestLst=nestLst, fieldsLst=fieldsLst, ipLst=ipLst, ipLstSet=ipLstSet,
                           record=record, recordDict=recordDict)


# route for page whre dns.log is analyzed


@app.route('/dhcppage/')
def dhcppage():
    # get fields and values from all files
    ze_path = os.path.join(folder, '20110919/dhcp.log')
    nestLst, fieldsLst, ipLst, mostDomLst = getNestLst(ze_path)
    ipLstSet = set(ipLst)
    # dictionary for ip with most occurrences for geolocation
    recordDict = {}
    for ip in ipLstSet:
        if ipLst.count(ip) >= 2:
            record = ipLocator(ip)
            recordDict[ip] = record

    #  use the mac_info to get the company manufacturer of nic card from mac Address
    nicList = []
    for nic in nestLst:
        nicList.append(nic[6])
        company = mac_info(nic[6])
    setNicList = set(nicList)

    return render_template("dhcppage.html", nestLst=nestLst, fieldsLst=fieldsLst, setNicList=setNicList,
                           company=company)


#  funny about page
@app.route('/about/')
def about():
    return render_template("about.html")


#  run the page
if __name__ == "__main__":
    app.run()
