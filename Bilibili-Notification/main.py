#!/usr/bin/python
#coding:utf-8

from managers.service_manager import service_manager
from servers import notification_poll_service
from servers import pushing_poll_service

def main():
    service_manager.register_service(notification_poll_service.NotificationPollService())
    service_manager.register_service(pushing_poll_service.PushingPollService())
    return service_manager.execute()

if __name__ == "__main__":
    main()
