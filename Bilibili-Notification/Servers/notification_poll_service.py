#!/usr/bin/python

#消息轮询服务
from servers import service
from defines import event_type
class NotificationPollService(service.Service):
    def __init__(self):
        super().__init__()

    def onUpdate(self):
        print("2222")