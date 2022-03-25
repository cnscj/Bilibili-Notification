#!/usr/bin/python
#coding:utf-8

from commons import dinging_robot
from configs import dingding_config
from defines import event_type

if __name__ == "__main__":
    robot = dinging_robot.DingDingRobot(dingding_config.DINGDING_PUSH_ROBOT_TOKEN_1,dingding_config.DINGDING_PUSH_ROBOT_SEC_1)
    #robot.send_text(event_type.MESSAGE_PUSH)
    robot.send_markdown()
 
 