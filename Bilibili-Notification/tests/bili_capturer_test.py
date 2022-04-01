#!/usr/bin/python
#coding:utf-8
import sys,pprint
from commons import bilibili_capturer

if __name__ == "__main__":
    pprint.pprint(sys.path)
    bilibili_capturer = bilibili_capturer.BilibiliCapturer(672328094)
    print(bilibili_capturer.capture_dynamic())