#!/usr/bin/python
#coding:utf-8

from managers.service_manager import service_manager
from servers import notification_poll_service

if __name__ == "__main__":
    service_manager.register_service(notification_poll_service.NotificationPollService())

    service_manager.execute()
