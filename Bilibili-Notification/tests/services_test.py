#!/usr/bin/python
#coding:utf-8

from managers.service_manager import service_manager
from servers import service


class TestService(service.Service):
    def _onUpdate():
        pass

if __name__ == "__main__":
    service_manager.register_service(TestService.TestService())

    service_manager.execute()
