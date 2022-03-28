#!/usr/bin/python
from utils import time_util
class Service:
    
    enabled = True  #是否开启
    interval = -1   #轮询间隔

    is_async = False #是否异步
    _is_async_stop = True #异步暂停用

    __next_timestamp = 0

    def __init__(self):
        pass

    def update(self):
        if not self.enabled:
            return
        
        if self.interval > 0 :
            cur_timestamp = time_util.get_cur_timestamp()
            if cur_timestamp < self.__next_timestamp:
                return
            self.__next_timestamp = cur_timestamp + self.interval

        self._onUpdate()
        self._onAfterUpdate()

    def _onUpdate(self):
        pass
    
    def _onAfterUpdate(self):
        pass

    def _onStart(self):
        pass 

    def _onExit(self):
        pass 


        
    

