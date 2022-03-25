#!/usr/bin/python

import time

def get_cur_timestamp():
    ts = time.time()
    return ts

def get_cur_timestamp_ms():
    t = get_cur_timestamp()
    return (int(round(t * 1000)))


  
