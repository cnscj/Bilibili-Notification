#!/usr/bin/python
#coding:utf-8

import os
import sys
from utils import time_util

def main():
    timestamp = time_util.get_cur_timestamp()
    timestr = time_util.time_stamp_to_time_str(timestamp)
    print(timestamp)
    print(timestr)
    print(time_util.time_stamp_to_time_array(timestamp))
    print(time_util.time_str_to_time_stamp(timestr))

if __name__ == "__main__":
    main()
 