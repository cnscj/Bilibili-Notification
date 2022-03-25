#!/usr/bin/python
#coding:utf-8

_eventUid = 10000

def get_event_uid():
    global _eventUid 
    _eventUid = _eventUid + 1
    return _eventUid