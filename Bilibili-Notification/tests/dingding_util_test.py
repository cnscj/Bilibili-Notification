#!/usr/bin/python
#coding:utf-8

from commons import dingding_util
if __name__ == "__main__":
    print(dingding_util.get_webhook_sign("this is secret"))