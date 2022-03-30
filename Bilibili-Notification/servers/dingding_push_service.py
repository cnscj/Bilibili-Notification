#!/usr/bin/python

#轮询推送服务
import queue
import time
import json
from commons import dinging_robot
from servers import service
from defines import event_type
from defines import message_type
from configs import dingding_config
from configs import language_config
from commons.dispatcher import dispatcher
from utils.logger import logger

class DingdingPushService(service.Service):
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
            logger.info('【推送服务机{type}】准备推送:【{title}】'.format(type=msg_type,title=msg_title))
            if msg_type == message_type.MessageType.Dynamic:
                self.__dynamic_robot.send_markdown(title=msg_title,text=msg_text)
    
            elif msg_type == message_type.MessageType.Live:
                self.__live_robot.send_markdown(title=msg_title,text=msg_text)
                
            elif msg_type == message_type.MessageType.Notice:
                self.__notice_robot.send_markdown(title=msg_title,text=msg_text)

    def __push_message(self,msg):
        msg_type = msg['type']
        msg_item = msg['item']

        title,text = None,None
        if msg_type == message_type.MessageType.Dynamic:
            title,text = self.__convert_dynamic_content_to_message(msg_item)
        elif msg_type == message_type.MessageType.Live:
           title,text = self.__convert_live_status_content_to_message(msg_item)
        elif msg_type == message_type.MessageType.Notice:
            title,text = self.__convert_dynamic_content_to_message(msg_item)

        if title and text:
            self.__message_queue.put({
                'type' : msg_type,
                'title' : title,
                'text' : text
            })

    #将内容转换成消息推送
    def __convert_dynamic_content_to_message(self,item):
        uid = item['desc']['uid']
        uname = item['desc']['user_profile']['info']['uname']
        dynamic_type = item['desc']['type']
        dynamic_id = item['desc']['dynamic_id']
        timestamp = item['desc']['timestamp']
        dynamic_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        card_str = item['card']
        card = json.loads(card_str)

        content = None
        pic_url = None
        if dynamic_type == 1:
            # 转发动态
            content = card['item']['content']
        elif dynamic_type == 2:
            # 图文动态
            content = card['item']['description']
            pic_url = card['item']['pictures'][0]['img_src']
        elif dynamic_type == 4:
            # 文字动态
            content = card['item']['content']
        elif dynamic_type == 8:
            # 投稿动态
            content = card['title']
            pic_url = card['pic']
        elif dynamic_type == 64:
            # 专栏动态
            content = card['title']
            pic_url = card['image_urls'][0]
        
        return language_config.get_string(1000001,name=uname),language_config.get_string(1000002,name=uname,content=content,pic_url=pic_url,dynamic_id=dynamic_id)

    def __convert_live_status_content_to_message(self,content):
        name = content['data']['name']
        room_id = content['data']['live_room']['roomid']
        room_title = content['data']['live_room']['title']
        room_cover_url = content['data']['live_room']['cover']

        return language_config.get_string(1000003,name=name),language_config.get_string(1000004,name=name,content=room_title,pic_url=room_cover_url,room_id=room_id)

    def _onStart(self):
        dispatcher.add_event_listener(event_type.MESSAGE_PUSH,self.__push_message)

    def _onExit(self):
        dispatcher.remove_event_listener(event_type.MESSAGE_PUSH,self.__push_message)
                

