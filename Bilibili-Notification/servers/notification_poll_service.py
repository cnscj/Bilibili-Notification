#!/usr/bin/python

#消息轮询服务
import time
import json
from collections import deque
from configs import services_config
from configs import language_config
from servers import service
from defines import event_type
from defines import message_type
from commons.dispatcher import dispatcher
from commons.bili_query import capturer
from utils.logger import logger
from utils.proxy import my_proxy

class NotificationPollService(service.Service):
    __bilibili_member_capturers = []
    __bilibili_official_capturers = []

    __dynamic_dict = {}         #记录各个成员间最新的动态id
    __living_status_dict = {}   #记录最新的直播状态

    __is_in_running_time = None

    def __init__(self):
        uid_list_member = services_config.UID_LIST_MEMBER
        uid_list_official = services_config.UID_LIST_OFFICIAL
        for _,uid in enumerate(uid_list_member):
            temp_capturer = capturer.BilibiliCapturer(uid)
            self.__bilibili_member_capturers.append(temp_capturer)
        for _,uid in enumerate(uid_list_official):
            temp_capturer = capturer.BilibiliCapturer(uid)
            self.__bilibili_official_capturers.append(temp_capturer)

    def _onStart(self):
        if services_config.PROXY_ENABLE:
            my_proxy.proxy_pool_url = services_config.PROXY_POOL_URL
            my_proxy.current_proxy_ip = my_proxy.get_proxy()

    def _onUpdate(self):
        if not self.__is_in_poll_time():
            return 

        #成员动态轮询
        for _,capturer in enumerate(self.__bilibili_member_capturers):
            captured_uid = capturer.get_uid()
            captured_dynamic_content = capturer.capture_dynamic()
            if self.__verify_dynamic_is_ok(captured_uid,captured_dynamic_content):
                if self.__check_dynamic_is_new(captured_uid,captured_dynamic_content):
                    self.__push_new_dynamics(captured_uid,message_type.MessageType.Dynamic,captured_dynamic_content)
   

            captured_live_status_content = capturer.capture_live_status()
            if self.__verify_live_status_is_ok(captured_uid,captured_live_status_content):
                if self.__check_live_status_is_new(captured_uid,captured_live_status_content):
                    self.__push_new_live_status(captured_uid,message_type.MessageType.Live,captured_live_status_content)

        #官号公告轮询,不检查直播状态(很少情况在官号直播)
        for _,capturer in enumerate(self.__bilibili_official_capturers):
            captured_uid = capturer.get_uid()
            captured_dynamic_content = capturer.capture_dynamic()
            if self.__verify_dynamic_is_ok(captured_uid,captured_dynamic_content):
                if self.__check_dynamic_is_new(captured_uid,captured_dynamic_content):
                    self.__push_new_dynamics(captured_uid,message_type.MessageType.Notice,captured_dynamic_content)

    #是否在轮询的时间内
    def __is_in_poll_time(self):
        current_time = time.strftime("%H:%M", time.localtime(time.time()))
        begin_time = services_config.BEGIN_TIME
        end_time = services_config.END_TIME

        is_in_poll_time = False
        if begin_time == '' or  end_time == '':
            is_in_poll_time = True
        else :
            is_in_poll_time = (begin_time <= current_time <= end_time)

        if is_in_poll_time != self.__is_in_running_time:
            if is_in_poll_time:
                logger.info('【查询服务机】: 开始轮询服务')
            else :
                logger.info('【查询服务机】: 进入休眠时间')
            self.__is_in_running_time = is_in_poll_time

        return is_in_poll_time

    #验证内容是否正确
    def __verify_dynamic_is_ok(self,uid,content):
        if content == "" :
            return False

        if content['code'] != 0:
            logger.error('【查询动态状态】请求返回数据code错误：{code}'.format(code=content['code']))
            return False
        else:
            data = content['data']
            if len(data['cards']) == 0:
                logger.info('【查询动态状态】【{uid}】动态列表为空'.format(uid=uid))
                return False

            item = data['cards'][0]
            try:
                _ = item['desc']['user_profile']['info']['uname']
            except KeyError:
                logger.error('【查询动态状态】【{uid}】获取不到uname'.format(uid=uid))
                return False
        
        return True

    #是否为最新的动态
    def __check_dynamic_is_new(self,uid,content):
        data = content['data']
        item = data['cards'][0] #获取最新的一条
        uname = item['desc']['user_profile']['info']['uname']
        dynamic_id = item['desc']['dynamic_id']
        if self.__dynamic_dict.get(uid, None) is None:
            self.__dynamic_dict[uid] = {'cur_dynamic_id':dynamic_id, 'handle_dynamic_id':dynamic_id}
            logger.info('【查询动态状态】【{uname}】动态初始化，动态id[{dynamic_id}]'.format(uname=uname,dynamic_id = dynamic_id))
            return False

        if dynamic_id != self.__dynamic_dict[uid]['cur_dynamic_id']:
            previous_dynamic_id = self.__dynamic_dict[uid]['cur_dynamic_id']
            logger.info('【查询动态状态】【{}】上一条动态id[{}]，本条动态id[{}]'.format(uname, previous_dynamic_id, dynamic_id))
            self.__dynamic_dict[uid]['cur_dynamic_id'] = dynamic_id
            return True

        return False
    
    #动态是否可推送
    def __check_dynamic_is_can_push(self,item):
        uid = item['desc']['uid']
        uname = item['desc']['user_profile']['info']['uname']
        dynamic_type = item['desc']['type']
        if dynamic_type not in services_config.HANDLE_DYNAMIC_TYPES:
            logger.info('【查询动态状态】【{uname}】动态有更新，但不在需要推送的动态类型列表中,类型[{dynamic_type}]'.format(uname=uname,dynamic_type=dynamic_type))
            return False
        return True

    #筛选出最新的动态,按照时间推送
    def __push_new_dynamics(self,uid,msgType,content):
        data = content['data']
        items = data['cards']

        previous_handle_dynamic_id = self.__dynamic_dict[uid]['handle_dynamic_id']
        last_dynamic_id_index = 2   #只推最新一条
        itemLen = min(9,len(items)) #最多取9条
        for index in range(itemLen,0,-1):
            item = items[index-1]
            dynamic_id = item['desc']['dynamic_id']
            if dynamic_id == previous_handle_dynamic_id: #XXX:dynamic_id获取错误容易暴毙
                last_dynamic_id_index = index
                break
                
        for index in range(last_dynamic_id_index-1,0,-1):
            item = items[index-1]
            if self.__check_dynamic_is_can_push(item):
                dispatcher.dispatch_event(event_type.MESSAGE_PUSH,{
                    'type' : msgType,
                    'item' : item
                })

        self.__dynamic_dict[uid]['handle_dynamic_id'] = self.__dynamic_dict[uid]['cur_dynamic_id']

    def __verify_live_status_is_ok(self,uid,content):
        if content == "" :
            return False

        if content['code'] != 0:
            logger.error('【查询直播状态】请求返回数据code错误：{code}'.format(code=content['code']))
            return False 
        try:
            _ = content['data']['live_room']['liveStatus']
        except (KeyError, TypeError):
            logger.error('【查询动态状态】【{uid}】获取不到liveStatus'.format(uid=uid))
            return False

        return True

    def __check_live_status_is_new(self,uid,content):
        name = content['data']['name']
        live_status = content['data']['live_room']['liveStatus']
        if self.__living_status_dict.get(uid, None) is None:
            self.__living_status_dict[uid] = live_status
            logger.info('【查询直播状态】【{uname}】初始化直播状态'.format(uname=name))
            return False

        if self.__living_status_dict.get(uid, None) != live_status:
            self.__living_status_dict[uid] = live_status
            if live_status == 1:    #状态1表示开播
                room_title = content['data']['live_room']['title']
                logger.info('【查询直播状态】【{name}】开播了：{room_title}'.format(name=name, room_title=room_title))
                return True
        
        return False

    def __push_new_live_status(self,uid,msgType,content):
        dispatcher.dispatch_event(event_type.MESSAGE_PUSH,{
            'type' : msgType,
            'item' : content,
        })





            