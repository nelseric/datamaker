# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 17:13:27 2014

@author: nater
"""

import httplib
import urllib
import json
import sys
import time
import datetime
import numpy as np
import socket
import urllib2
import re
import time
import pandas as pd
import requests
from optparse import OptionParser


def query_broker_hist(startTime):
    """
    Connects to broker and retrieves count records
    Environment           <Domain>
    fxTrade               stream-fxtrade.oanda.com
    fxTrade Practice      stream-fxpractice.oanda.com
    sandbox               stream-sandbox.oanda.com
    """

    #Time format should follow the format eg: 2012-08-29T12:07:00.000000Z
    domain = 'api-fxpractice.oanda.com'
    access_token = '60246d7866f27504023d7bc022336292-df363650e09c89ee4f3782a178a17fe1'
    account_id = '7927251'
    instrument = "EUR_USD"
    gran = 'M1'
    count = 5000
    cForm = 'bidask'
    try:
        s = requests.Session()
        url = "https://" + domain + "/v1/candles"
        headers = {'Authorization' : 'Bearer ' + access_token,
                   # 'X-Accept-Datetime-Format' : 'unix'
                  }
        params = {'instrument' : instrument,  'granularity' : gran, 'candleFormat' : cForm, 'start' : startTime, 'count' : count}
        req = requests.Request('GET', url, headers = headers, params = params)
        pre = req.prepare()
        resp = s.send(pre, stream = True, verify = False)
        return resp
    except Exception as e:
        s.close()
        print "Caught exception when connecting to stream\n" + str(e) 

def cur_allocation_is_small(dd_thresh):
    """
    Checks the amount of money allocated for current orders;
    checks if this value is greater than dd_thresh
    """
    domain = 'api-fxpractice.oanda.com'
    access_token = '60246d7866f27504023d7bc022336292-df363650e09c89ee4f3782a178a17fe1'
    account_id = '7927251'
    
    try:
        s = requests.Session()
        url = 'https://' + domain + '/v1/accounts/' + account_id + '/positions'
        headers = {'Authorization' : 'Bearer ' + access_token,
                  }
        params = { }
        req = requests.Request('GET', url, headers = headers, params = params)
        pre = req.prepare()
        resp = s.send(pre, stream = True, verify = False)
        resp_dict = json.loads(resp.text)['positions']
        total_units = [item['units'] for item in resp_dict]
        if (sum(total_units) < dd_thresh):
            return True
        return False
        
    except Exception as e:
        s.close()
        print "Caught exception when connecting to stream\n" + str(e)
        return False

def place_order(order_params):
    """
    Requests an order on broker given a dict of parameters
    """
    account_id = '7927251'
    pair = 'EUR_USD'
    access_token = '60246d7866f27504023d7bc022336292-df363650e09c89ee4f3782a178a17fe1'
    conn = httplib.HTTPConnection("api-fxpractice.oanda.com", timeout=5)    
    
    conn = httplib.HTTPSConnection("api-sandbox.oanda.com")
    params = urllib.urlencode({"instrument": "EUR_USD",
                               "units" : order_params['units'],
                               "side" : "buy",
                               "type" : "market"
                               })
    headers = {"Content-Type" : "application/x-www-form-urlencoded", 
                "Authorization" : "Bearer " +access_token}
    conn.request("POST", "/v1/accounts/" + account_id + "/orders", params, headers)
    print conn.getresponse().read()
    return True

def gather_data(startTimeArg):
    """
    Generates ohlcv dataset with broker data from startTimeArg to current time
    """
    outData = []
    startTime = startTimeArg
    data_complete = False
    while (data_complete != True): 
        response = query_broker_hist(startTime)
        if response.status_code != 200:
            print response.text
            print "nope"
            return
        rawData = json.loads(response.text)
        rawData = rawData['candles']
        outData = outData + rawData
        startTime = rawData[-1]['time']
        if (len(rawData) < 5000):
            data_complete = True
    print "here"
        
    return outData

def extract_h2o_data(predOut):
    """
    Extracts values of the outputs from h2o
    """
    tempA = re.findall('\d+',predOut[predOut.find('row_0'):])
    output = [0,0]
    output[0] = (float('.'+str(tempA[4])))
    output[1] = (float('.'+str(tempA[6])))
    return output
    
def list_to_df(data):
    """
    Converts list of dictionaries to dataframe
    """
    indices = pd.tseries.index.DatetimeIndex([data[x]['time'] for x in range(0,len(data))])
    outData = pd.DataFrame(data,index = indices)
    return outData
    
def update_data(data):
    """
    Updates old dataframe with new broker ohlcv data
    """
    startTime = data.index[-1].strftime("%Y-%m-%dT%H:%M:%S.000000Z")
    newData = gather_data(startTime)
    newData = list_to_df(newData)
    outData = data.append(newData)
    return outData

def generate_indicators(data):
    """
    Generates indicator DF from broker ohlcv data
    """    
    outData = []    
    return outData
    
def poll_h2o(data):
    """
    Evaluates NN output on current ohlcv data
    """
    path_name = 'home/nater/TempOut/'
    file_name = 'tempPred.csv'
    model_name = 'BestModel2'
    pred_name = file_name.split('.')[0]
    #save the data
    data[-1].to_csv(path_name+file_name)
    #load the data in H2o    
    urlImp1 = 'http://localhost:54321/ImportFiles.json?path=/' + path_name + file_name
    urllib2.urlopen(urlImp1)
    #parse the data in H2o
    urlImp2 = 'http://localhost:54321/Parse.json?parser_type=AUTO&separator=-1&header=0&single_quotes=0&header_from_file=&exclude=&source_key=' + urllib.quote('nfs://' + path_name + file_name, safe='') + '&preview=0'
    urllib2.urlopen(urlImp2)
    #run the data on NN
    urlPred1 = 'http://localhost:54321/2/Predict.json?model=' + model_name + '&data=' + pred_name + '.hex&prediction=test1.hex'
    urllib2.urlopen(urlPred1)
    #inspect the predictions on the NN
    urlPred2 = 'http://localhost:54321/2/Inspect2.html?src_key=test1.hex'
    urllib2.urlopen(urlPred2)
    predOut = urllib2.urlopen(urlPred2).read()
    preds = extract_h2o_data(predOut)
    #delete the prediction 
    urlPost1 = 'http://localhost:54321/Remove.json?key=tempPred.hex'
    urllib2.urlopen(urlPost1)
    return preds

def manage_orders(h2o_data,order_params):
    """
    Places order if confidence is high and enough money is availiable
    """
    thresh = .7
    make_order = True
    #this is in units of units
    dd_thresh = 10  
    #check confidence    
    if (h2o_data[1] < thresh):
        make_order = False
    elif(cur_allocation_is_small(dd_thresh) == False):
        make_order = False
    
    if (make_order):
        place_order(order_params)
    
    return make_order
        
    
def broker_interact():
    """
    Executes real-time trading
    """
    print "Generating Oanda data"
    startTime = '2014-08-11T00:00:00.000000Z'
    looping = True
    order_params = {'units' : 2 }
    data = gather_data(startTime)
    data = list_to_df(data)
    data = data[:5]
    
    while (looping):
        #refresh dataframe with real-time data    
        data = update_data(data)
        #calculate indicators with real-time data
        ind_data = generate_indicators(data)
        #Poll H2O for predictions
        h2o_data = poll_h2o(data)
        #Use predictions for placing orders
        manage_orders(h2o_data,order_params)
        #wait until the next minute to make another evaluation

if __name__=='__main__':
    broker_interact()
      