#!/usr/bin/python

#消息轮询服务
from configs import services_config
from servers import service
from defines import event_type
from commons.bili_query import capturer

class NotificationPollService(service.Service):
    __bilibili_capturers = []

    __dynamic_dict = {}
    __living_status_dict = {}

    def __init__(self):
        uid_list = services_config.UID_LIST
        for _,uid in enumerate(uid_list):
            capturer = capturer.BilibiliCapturer(uid)
            self.__bilibili_capturers.append(capturer)

    def onUpdate(self):
        pass
