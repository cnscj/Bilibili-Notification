#!/usr/bin/python
#coding:utf-8

import time
from managers.service_manager import service_manager
from servers import service


class TestService(service.Service):
    def __init__(self):
        self.is_async = True

    def pp(self):
        print("@@@@@@")

    def _onUpdate(self):
        print("!!!")
        time.sleep(5)

if __name__ == "__main__":
    service_manager.register_service(TestService())
    service_manager.execute()
