#!/usr/bin/python
#coding:utf-8

import os,sys

#钉钉推送
DINGDING_PUSH_WEBHOOK_URL = "https://oapi.dingtalk.com/robot"
#钉钉推送接口
DINGDING_PUSH_WEBHOOK_SEND_ACTION = "send"
#钉钉推送token字段
DINGDING_PUSH_WEBHOOK_TOKEN_FIELD = "access_token"
DINGDING_PUSH_WEBHOOK_TIMESTAMP_FIELD = "timestamp"
DINGDING_PUSH_WEBHOOK_SIGN_FIELD = "sign"


#钉钉1号推送机TOKEN及SEC
DINGDING_PUSH_ROBOT_TOKEN_1 = "79843976c51811a4632e98abb473b2512b62562819b71ac1c3631a9937f59ed2"
DINGDING_PUSH_ROBOT_SEC_1 = "SEC69e94af8174169d28539161ee86c726ad4a1d893ecac2fc19c8edeb7fa2d316a"

#钉钉2号推送机TOKEN及SEC
DINGDING_PUSH_ROBOT_TOKEN_2 = "460f15a4da74f59a5107f0b5b73b3847615f9851637a9631fd17738d9c50090a"
DINGDING_PUSH_ROBOT_SEC_2 = "SEC20205c8f18db265f91f7bedab54cdcb76bc1a980594f882651c50b8462dc1456"


def get_send_url(attrs = None):
    attrStr = ""
    if attrs != None :
        for k,v in attrs.items():
            attrStr = attrStr + "{0}={1}".format(k,v) + "&"
        attrStr.strip('&')

    return "{0}/{1}?{2}".format(DINGDING_PUSH_WEBHOOK_URL,DINGDING_PUSH_WEBHOOK_SEND_ACTION,attrStr)