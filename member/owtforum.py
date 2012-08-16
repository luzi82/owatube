# -*- coding: utf-8 -*-
'''
Created on 2012年8月16日

@author: luzi82
'''
import urllib
import httplib

def check_password(username,password):
    params0 = urllib.urlencode({
        'mode': "login",
        'login_check': "1",
    })
    params1 = urllib.urlencode({
        'login': "登入",
        'username': username,
        'password': password,
    })
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    conn = httplib.HTTPConnection("forum.owataiko.com")
    conn.request("POST", "/ucp.php?"+params0, params1, headers)
    response = conn.getresponse()
    if response.status != 200:
        return -1
    data = response.read()
    conn.close()
    try:
        data = int(data)
    except TypeError:
        return -1
    return data
