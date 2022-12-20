#!/usr/bin/python
#coding:utf-8
import os
from managers.service_manager import service_manager
from servers import notification_poll_service
from servers import dingding_push_service
from servers import sleep_cpu_service
from utils.logger import logger

def main():
    pid = os.getpid()
    logger.info('【进程服务】: 当前进程pid:{pid}'.format(pid=pid))

    service_manager.register_service(notification_poll_service.NotificationPollService())
    service_manager.register_service(dingding_push_service.DingdingPushService())
    service_manager.register_service(sleep_cpu_service.SleepCpuService())
    
    return service_manager.execute()

if __name__ == "__main__":
    main()
