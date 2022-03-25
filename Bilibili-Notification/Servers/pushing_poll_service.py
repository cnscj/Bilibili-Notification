#!/usr/bin/python

#轮询推送服务
from servers import service
from defines import event_type
class PushingPollService(service.Service):
    def __init__(self):
        super().__init__()