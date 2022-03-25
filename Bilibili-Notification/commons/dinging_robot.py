#!/usr/bin/python
#coding:utf-8

import time
import hmac
import hashlib
import base64
import urllib.parse
from utils import http_util

#钉钉推送
DINGDING_PUSH_WEBHOOK_URL = "https://oapi.dingtalk.com/robot"
#钉钉推送接口
DINGDING_PUSH_WEBHOOK_SEND_ACTION = "send"
#钉钉推送token字段
DINGDING_PUSH_WEBHOOK_TOKEN_FIELD = "access_token"
DINGDING_PUSH_WEBHOOK_TIMESTAMP_FIELD = "timestamp"
DINGDING_PUSH_WEBHOOK_SIGN_FIELD = "sign"

class DingDingRobot:
    #获取sign
    def get_webhook_sign(cls, secret):
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign,timestamp

    def get_send_url(cls, attrs = None):
        attrStr = ""
        if attrs != None :
            for k,v in attrs.items():
                attrStr = attrStr + "{0}={1}".format(k,v) + "&"
            attrStr.strip('&')

        return "{0}/{1}?{2}".format(DINGDING_PUSH_WEBHOOK_URL,DINGDING_PUSH_WEBHOOK_SEND_ACTION,attrStr)

    __token = ""
    __secret = ""
    def __init__(self, token, secret = ""):
        self.__token = token
        self.__secret = secret
        
    def send_text(self, content):
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
        }
        self.send(data)

    def send_link(self, text, title, picUrl, messageUrl):
        data = {
            "msgtype": "link", 
            "link": {
                "text": text, 
                "title": title, 
                "picUrl": picUrl, 
                "messageUrl": messageUrl
            }
        }
        self.send(data)

    def send_markdown(self, title, text):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text,
            },
            # "at": {
            #     "atMobiles": [
            #         "150XXXXXXXX"
            #     ],
            #     "atUserIds": [
            #         "user123"
            #     ],
            #     "isAtAll": "false"
            # }
        }
        self.send(data)

    def send_action_card(self, title, text, singleTitle, singleURL):
        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title, 
                "text": text, 
                "btnOrientation": "0", 
                "singleTitle" : singleTitle,
                "singleURL" : singleURL
            }, 
        }
        self.send(data)

    def send(self, data):
        attr_dict = {}

        if self.__token != "":
            attr_dict[DINGDING_PUSH_WEBHOOK_TOKEN_FIELD] = self.__token

        if self.__secret != "":
            sign,timestamp = self.get_webhook_sign(self.__secret)
            attr_dict[DINGDING_PUSH_WEBHOOK_TIMESTAMP_FIELD] = timestamp
            attr_dict[DINGDING_PUSH_WEBHOOK_SIGN_FIELD] = sign

        send_url = self.get_send_url(attr_dict)

        http_util.post(url = send_url, json = data)

