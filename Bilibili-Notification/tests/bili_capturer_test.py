#!/usr/bin/python
#coding:utf-8
import sys,pprint
 

from commons.bili_query import capturer
if __name__ == "__main__":
    pprint.pprint(sys.path)
    capturer = capturer.BilibiliCapturer(672328094)
    print(capturer.capture_dynamic())