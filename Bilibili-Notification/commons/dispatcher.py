#!/usr/bin/python

from patterns import singleton

class Dispatcher(singleton.Singleton):
    __event_listeners = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_event_listener(self, name, listener_or_caller, priority = -1):
        if name == "":
            return
        if listener_or_caller == None:
            return

        event_listeners_list = self.__event_listeners.get(name)
        if not event_listeners_list:
            event_listeners_list = []
            self.__event_listeners[name] = event_listeners_list
        
        temp_listener_info = {
            'name' : name,
            'listener_or_caller' : listener_or_caller,
        }

        if priority > 0 :
            event_listeners_list.insert(priority,temp_listener_info)
        else :
            event_listeners_list.append(temp_listener_info)  
        

    def remove_event_listener(self, name, listener_or_caller):
        event_listeners_list = self.__event_listeners.get(name)
        if event_listeners_list:
            for i, v in enumerate(event_listeners_list):
                if v['listener_or_caller'] == listener_or_caller:
                    del self.__event_listeners[i]

    def dispatch_event(self, name, *args, **kwargs):
        event_listeners_list = self.__event_listeners.get(name)
        if event_listeners_list :
            for _,v in enumerate(event_listeners_list):
                listener_or_caller = v['listener_or_caller']
                listener_or_caller(*args, **kwargs)

dispatcher = Dispatcher()