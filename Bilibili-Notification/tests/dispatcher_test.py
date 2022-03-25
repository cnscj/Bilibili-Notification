#!/usr/bin/python
#coding:utf-8

from commons.dispatcher import dispatcher
from defines import event_type

class AClass:
    def oo(self,text="oo"):
        print(text)

def aa(text):
    print("!!!")

def bb():
    print("@@@@")

if __name__ == "__main__":
    aIns = AClass()
    bIns = AClass()

    dispatcher.add_event_listener(event_type.TEST_EVENT,aa)
    dispatcher.add_event_listener(event_type.TEST_EVENT,aIns.oo)
    dispatcher.add_event_listener(event_type.TEST_EVENT,bIns.oo)

    dispatcher.dispatch(event_type.TEST_EVENT,"TT")