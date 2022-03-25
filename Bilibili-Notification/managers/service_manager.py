#!/usr/bin/python
from patterns import singleton
class ServiceManager(singleton.Singleton):
    __services = {}

    def __init__(self):
        pass

    def register_service(self, service):
        services_name = type(service).__name__
        service_in_dict = self.__services.get(services_name)
        if not service_in_dict:
            service.onStart()
            self.__services[services_name] = service

    def unregister_service(self, service):
        services_name = type(service).__name__
        service_in_dict = self.__services.get(services_name)
        if service_in_dict:
            service.onExit()
            del self.__services[services_name]

    def execute(self):
        while (True):
            for _,v in self.__services.items():
                v.onUpdate()

service_manager = ServiceManager()