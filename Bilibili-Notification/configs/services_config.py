#!/usr/bin/python
#coding:utf-8

# up主uid列表
#UID_LIST_MEMBER = [672328094,672346917,672353429,672342685,351609538]
UID_LIST_MEMBER = [672328094,672346917,672353429,672342685]
UID_LIST_OFFICIAL = [703007996]

#需要处理的动态类型
HANDLE_DYNAMIC_TYPES = [2,4,6,8,64]

# 扫描间隔秒数，不建议设置太频繁
INTERVALS_SECOND = 60
# 扫描起止时间，24小时制(目前不支持跨日期)，例：07:00、23:59
BEGIN_TIME = "07:00"
END_TIME = "23:59"

#[proxy_pool]
# 是否启用 true/false
PROXY_ENABLE = False
# ip池地址，参考 https://github.com/jhao104/proxy_pool
PROXY_POOL_URL = "http://ip:port"