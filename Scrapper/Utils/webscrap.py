import json
import requests
import hashlib
import base64
import datetime
import boto3, os
import numpy as np


def base64_encode(string):
    message = string
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    return(base64_message)

def api_call(headers, encoded_data):
    r = requests.post("https://app.cpcbccr.com/caaqms/advanced_search", headers=headers, data=encoded_data,
                      verify=False)
    time_lst = []
    if r.status_code == 200:
        #print("Awesome response code 200")
        json_dict = r.json()
        aqi_data = json_dict['tabularData']['bodyContent']
        req_list = ['from date', 'to date', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'Ozone']
        add_lst = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'Ozone']
        delete_keys = ['from date', 'exceeding']
        for ele_dict in aqi_data:
            if ele_dict['from date'] not in time_lst:
                time_lst.append(ele_dict['from date'])
            for d in delete_keys:
                del ele_dict[d]
        for i in range(len(aqi_data)):
            for key in add_lst:
                res_list[i][key].append(aqi_data[i][key])

    elif r.status_code == 404:
        #print("response code 404")
        api_call(headers, encoded_data)
    else:
        pass
        #print(r.status_code)
    return time_lst


def scrapper():
    headers = {'Origin': 'https://app.cpcbccr.com'}
    headers['Accept-Encoding'] ="gzip, deflate, br"
    headers['Accept-Language'] ="en-GB,en-US;q=0.9,en;q=0.8"
    headers['User-Agent'] ="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    headers['Content-Type'] ="application/x-www-form-urlencoded"
    headers['Accept'] ="application/json, text/plain, */*"
    headers['Referer'] ="https://app.cpcbccr.com/ccr/"
    headers['Connection'] ="keep-alive"
    headers['Host'] ="app.cpcbccr.com"


    site_list = ["site_5129", "site_5238", "site_5110", "site_5111", "site_296", "site_5126", "site_309"]
    month = [1,4,7,8,10,12]

    global res_list
    res_list = [{}, {}, {}, {}]
    lst = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'Ozone']
    for t in range(4):
        for key in lst:
            res_list[t][key] = []

    for site in site_list:
        toDate = datetime.datetime.now().strftime("%d-%m-%Y T%H:%M:%SZ")
        now = toDate.split('T')[0] + toDate.split()[1][:3] + ":00:00Z"
        fromdate = datetime.datetime.now() - datetime.timedelta(hours=4, minutes=0)
        format_data = fromdate.strftime("%d-%m-%Y T%H:%M:%SZ")
        format_data = format_data.split('T')[0] + format_data.split()[1][:3] + ":00:00Z"
        data = {"criteria": "1 Hours",
                "reportFormat": "Tabular",
                "fromDate": format_data,
                "toDate": now,
                "state": "West Bengal",
                "city": "Kolkata",
                "station": site,
                "parameter": ["parameter_215", "parameter_193", "parameter_226", "parameter_225",
                              "parameter_194", "parameter_311", "parameter_312", "parameter_203", "parameter_222"],
                "parameterNames": ["PM10", "PM2.5", "NO", "NOx", "NO2", "NH3", "SO2",
                                   "CO", "Ozone"]
                }
        json_str = json.dumps(data)
        encoded_data = base64_encode(json_str)
        time = api_call(headers, encoded_data)
    for j in range(len(res_list)):
        res_list[j]['Date-Time'] = time[j]
        for k in lst:
            arr = np.array(res_list[j][k], dtype = np.float64())
            avg = np.nanmean(arr)
            res_list[j][k] = round(avg, 5)
    return res_list

res = scrapper()
print(res)