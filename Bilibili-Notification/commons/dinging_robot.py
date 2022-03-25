#!/usr/bin/python
#coding:utf-8

from commons import dingding_util
from utils import http_util
from configs import dingding_config

class DingDingRobot:
    __token = ""
    __secret = ""
    def __init__(self, token, secret=""):
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

    def send_link(self, content):
        data = {
            "msgtype": "link", 
            "link": {
                "text": "这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林", 
                "title": "时代的火车向前开", 
                "picUrl": "", 
                "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
            }
        }
        self.send(data)

    def send_markdown(self):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":"杭州天气",
                "text": "#### 杭州天气 @150XXXXXXXX \n > 9度，西北风1级，空气良89，相对温度73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
            },
            "at": {
                "atMobiles": [
                    "150XXXXXXXX"
                ],
                "atUserIds": [
                    "user123"
                ],
                "isAtAll": "false"
            }
        }
        self.send(data)

    def send_action_card(self):
        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身", 
                "text": "![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png) ### 乔布斯 20 年前想打造的苹果咖啡厅 Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划", 
                "btnOrientation": "0", 
                "singleTitle" : "阅读全文",
                "singleURL" : "https://www.dingtalk.com/"
            }, 
        }
        self.send(data)

    def send(self, data):
        attr_dict = {}

        if self.__token != "":
            attr_dict[dingding_config.DINGDING_PUSH_WEBHOOK_TOKEN_FIELD] = self.__token

        if self.__secret != "":
            sign,timestamp = dingding_util.get_webhook_sign(self.__secret)
            attr_dict[dingding_config.DINGDING_PUSH_WEBHOOK_TIMESTAMP_FIELD] = timestamp
            attr_dict[dingding_config.DINGDING_PUSH_WEBHOOK_SIGN_FIELD] = sign

        send_url = dingding_config.get_send_url(attr_dict)

        http_util.post(url = send_url, json = data)
