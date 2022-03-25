#!/usr/bin/python

import requests
def post(**kwargs):
    request = requests.post(**kwargs) #接口调用
    return request

def get(**kwargs):
    request = requests.get(**kwargs) #接口调用
    return request


