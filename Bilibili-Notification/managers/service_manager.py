#!/usr/bin/python
import queue
import threading
import time
from patterns import singleton
def update_server(service):
    if not service:
        return
    service.update()
    # time.sleep(0.001) #减少CPU占用

def poll_service(service):
    if not service:
        return
        
    while (True):
        if service._is_async_stop:
            break
        update_server(service)

class ServiceManager(singleton.Singleton):
    __sync_services = {}
    __async_services = {}
    __async_services_start = queue.Queue()
    __async_services_stop = queue.Queue()

    def __init__(self):
        pass

    def register_service(self, service):
        services_name = type(service).__name__
        is_async = service.is_async

        if is_async:
            service_in_dict = self.__async_services.get(services_name)
            if not service_in_dict:
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
            service_in_dict = self.__async_services.get(services_name)
            if service_in_dict:
                self.__async_services_stop.put(service)
        else:
            service_in_dict = self.__sync_services.get(services_name)
            if service_in_dict:
                service._onExit()
                del self.__sync_services[services_name]
                
    def execute(self):
        #开始异步服务的
        while (True):
            while (not self.__async_services_start.empty()):
                service = self.__async_services_start.get()
                services_name = type(service).__name__
                service_in_dict = self.__async_services.get(services_name)
                if not service_in_dict: 
                    service._onStart()
                    service._is_async_stop = False
                    thread = threading.Thread(target=poll_service,args=[service])
                    self.__async_services[services_name] = thread
                    thread.start()
                    
            while (not self.__async_services_stop.empty()):
                service = self.__async_services_stop.get()
                services_name = type(service).__name__
                service_in_dict = self.__async_services.get(services_name)
                if service_in_dict: 
                    service._onExit()
                    service._is_async_stop = True
                    del self.__async_services[services_name]
            
            #同步服务轮询
            for _,v in self.__sync_services.items():
                update_server(v)

service_manager = ServiceManager()