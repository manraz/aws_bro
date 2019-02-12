'''
Author: Manu Babanu
Date: 09/04/2018
Description: Script to parse bro IDS log files. Takes log fields and fields
data from logs into list for use in application.
'''

import datetime
import pygeoip
import urllib.request


# function to parse all fields from log file into lists
def getNestLst(path):
    file = open(path, 'r')
    valuesLst = []
    fieldsLst = []
    nestLst = []
    ipLst = []
    mostDomLst = []
    for line in file:
        if '#fields' in line:
            fieldsLst = line.split()
            fieldsLst.remove('#fields')
        elif '#' in line:
            continue
        else:
            valuesLst = line.split('\t')
            # takes the epoch timestamp and replace it with formated date
            if valuesLst[0]:
                valuesLst.insert(0, datetime.datetime.fromtimestamp(
                    float(valuesLst[0])).strftime('%Y-%m-%d %H:%M:%S'))
                valuesLst.pop(1)
            nestLst.append(valuesLst)
            ipLst.append(valuesLst[4])
            mostDomLst.append(valuesLst[8])
    return nestLst, fieldsLst, ipLst, mostDomLst


# takes ip and return geolocation json
def ipLocator(ip):
    GeoIPDatabase = '/home/ubuntu/aws_bro/GeoLiteCity.dat'
    ipData = pygeoip.GeoIP(GeoIPDatabase)
    record = ipData.record_by_name(ip)
    return record


# get company name of nic card from mac address. The best and easiest will be to use the IEEE Registration Autorithy oui.txt
def mac_info(mac):
    url = "http://api.macvendors.com/"
    response = urllib.request.urlopen(url + mac)
    company = response.read().decode()
    return company
