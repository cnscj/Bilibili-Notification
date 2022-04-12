#!/usr/bin/python
#coding:utf-8

import json
import time
from utils import http_util
from utils.logger import logger

class BilibiliCapturer:
    __uid = ""

    def get_headers(cls, uid):
        return {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'l=v;',
        'origin': 'https://space.bilibili.com',
        'pragma': 'no-cache',
        'referer': 'https://space.bilibili.com/{}/dynamic'.format(uid),
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
    }

    def __init__(self,uid):
        self.set_uid(uid)

    def set_uid(self,uid):
        self.__uid = str(uid)

    def get_uid(self):
        return self.__uid

    def capture_dynamic(self):
        uid = self.__uid
        if uid is None:
            return ""
        query_url = 'http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history' \
                '?host_uid={uid}&offset_dynamic_id=0&need_top=0&platform=web&my_ts={my_ts}'.format(uid = uid, my_ts = int(time.time()))
        headers = self.get_headers(uid)
        response = http_util.requests_get(query_url, '查询动态状态', headers=headers, use_proxy=True)
        if http_util.check_response_is_ok(response):
            try:
                result = json.loads(str(response.content, 'utf-8'))
                return result
            except UnicodeDecodeError:
                logger.error('【查询动态状态】【{uid}】解析content出错'.format(uid=uid))
        return ""

    def capture_live_status(self):
        uid = self.__uid
        if uid is None:
            return
        query_url = 'http://api.bilibili.com/x/space/acc/info?mid={}&my_ts={}'.format(uid, int(time.time()))
        headers = self.get_headers(uid)
        response = http_util.requests_get(query_url, '查询直播状态', headers=headers, use_proxy=True)
        if http_util.check_response_is_ok(response):
            try:
                result = json.loads(str(response.content, 'utf-8'))
                return result
            except UnicodeDecodeError:
                logger.error('【查询直播状态】【{uid}】解析content出错'.format(uid=uid))
        return ""
