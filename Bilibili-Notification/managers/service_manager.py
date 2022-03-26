#!/usr/bin/python
import queue
from turtle import update
import thread
from patterns import singleton
class ServiceManager(singleton.Singleton):
    __sync_services = {}
    __async_services = {}
    __async_services_start = queue.Queue() #推送队列
    __async_services_stop = queue.Queue() #推送队列

    def __init__(self):
        pass

    def register_service(self, service):
        services_name = type(service).__name__
        is_async = service.is_async

        if is_async:
            if not self.__async_services:
                self.__async_services_start.put(service)
        else :
            service_in_dict = self.__sync_services.get(services_name)
            if not service_in_dict:
                service._onStart()
                self.__sync_services[services_name] = service

    def unregister_service(self, service):
        services_name = type(service).__name__
        is_async = service.is_async

        if is_async:
            self.__async_services_stop.put(service)
        else:
            service_in_dict = self.__sync_services.get(services_name)
            if service_in_dict:
                service._onExit()
                del self.__sync_services[services_name]
                
    def execute(self):
        #TODO:开始异步服务的
        while (not self.__async_services_start.empty()):
            service = self.__async_services_start.get()
            services_name = type(service).__name__
            service_in_dict = self.__async_services.get(services_name)
            if not service_in_dict: 
                service._onStart()
                # func = lambda : 
                #     while (True):
                #         service.update()
                # self.__async_services[services_name] = thread.start_new_thread(func)

        while (not self.__async_services_stop.empty()):
            service = self.__async_services_stop.get()
            services_name = type(service).__name__
            service_in_dict = self.__async_services.get(services_name)
            if not service_in_dict: 
                service._onExit()
                del self.__async_services[services_name]
            


        #同步服务轮询
        while (True):
            for _,v in self.__sync_services.items():
                v.update()

service_manager = ServiceManager()