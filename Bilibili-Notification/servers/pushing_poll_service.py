#!/usr/bin/python

#轮询推送服务
import queue

from commons import dinging_robot
from servers import service
from defines import event_type
from defines import message_type
from configs import dingding_config
from commons.dispatcher import dispatcher
from utils.logger import logger

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

    def _onUpdate(self):
        while (not self.__message_queue.empty()):
            msg = self.__message_queue.get()
            msg_type = msg['type']
            msg_title = msg['title']
            msg_text = msg['text']
            if msg_type == message_type.MessageType.Dynamic:
                self.__dynamic_robot.send_markdown(title=msg_title,text=msg_text)
    
            elif msg_type == message_type.MessageType.Live:
                self.__live_robot.send_markdown(title=msg_title,text=msg_text)
                
            elif msg_type == message_type.MessageType.Notice:
                self.__notice_robot.send_markdown(title=msg_title,text=msg_text)

    def __push_message(self,msg):
        msg_title = msg['title']
        logger.info('【推送服务】准备推送:【{title}】'.format(title=msg_title))
        self.__message_queue.put(msg)

    def _onStart(self):
        dispatcher.add_event_listener(event_type.MESSAGE_PUSH,self.__push_message)

    def _onExit(self):
        dispatcher.remove_event_listener(event_type.MESSAGE_PUSH,self.__push_message)
                

