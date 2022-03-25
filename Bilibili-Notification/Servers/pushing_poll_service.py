#!/usr/bin/python

#轮询推送服务
import queue
from commons import dinging_robot
from servers import service
from defines import event_type
from defines import message_type
from configs import dingding_config

class PushingPollService(service.Service):
    __dynamic_robot = None  #动态推送
    __live_robot = None     #直播状态推送
    __notice_robot = None   #官号公告推送
    __message_queue = queue.Queue() #推送队列

    def __init__(self):
        super().__init__()
        self.__dynamic_robot = dinging_robot.DingDingRobot(dingding_config.DINGDING_PUSH_ROBOT_TOKEN_1,dingding_config.DINGDING_PUSH_ROBOT_SEC_1)
        self.__live_robot = dinging_robot.DingDingRobot(dingding_config.DINGDING_PUSH_ROBOT_TOKEN_2,dingding_config.DINGDING_PUSH_ROBOT_SEC_2)
        self.__notice_robot = dinging_robot.DingDingRobot(dingding_config.DINGDING_PUSH_ROBOT_TOKEN_3,dingding_config.DINGDING_PUSH_ROBOT_SEC_3)

    def onUpdate(self):
        while (not self.__message_queue.empty()):
            message = self.__message_queue.get()
            if message.type == message_type.MessageType.Dynamic:
                self.__dynamic_robot
                
            elif message.type == message_type.MessageType.Live:
                self.__live_robot
                
            elif message.type == message_type.MessageType.Notice:
                self.__notice_robot

    
    def onStart(self):
        pass

    def onExit(self):
        pass
                

