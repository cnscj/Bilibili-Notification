#!/usr/bin/python

import time

def get_cur_timestamp():
    ts = time.time()
    return ts

def get_cur_timestamp_ms():
    t = get_cur_timestamp()
    return (int(round(t * 1000)))

def time_array_to_time_stamp(array):
    return int(time.mktime(array))

def time_str_to_time_stamp(str):
    time_array = time.strptime(str,"%Y-%m-%d %H:%M:%S")
    return time_array_to_time_stamp(time_array)

def time_stamp_to_time_str(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def time_stamp_to_time_array(time_stamp):
    str = time_stamp_to_time_str(time_stamp)
    return time.strptime(str, "%Y-%m-%d %H:%M:%S")
