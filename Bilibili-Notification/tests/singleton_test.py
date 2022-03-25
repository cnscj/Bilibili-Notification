#!/usr/bin/python
#coding:utf-8
from commons import dispatcher

   
if __name__ == "__main__":
    dispatcher1 = dispatcher.Dispatcher()
    dispatcher2 = dispatcher.Dispatcher()

    print(id(dispatcher1))
    print(id(dispatcher2))