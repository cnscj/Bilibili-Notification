# Bilibili-Notification

## 声明:

- 本仓库发布的`Bilibili-Notification`项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途
- `cnscj` 对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害
- 以任何方式查看此项目的人或直接或间接使用`Bilibili-Notification`项目的任何脚本的使用者都应仔细阅读此声明
- `Bilibili-Notification` 保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或`Bilibili-Notification`项目，则视为已接受此免责声明
- 本项目遵循`MIT LICENSE`协议，如果本声明与`MIT LICENSE`协议有冲突之处，以本声明为准

## 简介

开启服务并定时检测指定up发布的动态,直播状态,如有更新则进行推送

## 运行环境

- [Python 3](https://www.python.org/)

## 使用教程

#### 1. 填写configs配置信息

(1)`services_config`下的参数
- `UID_LIST_MEMBER`为需要扫描的up主uid列表，使用英文逗号分隔，必填
- `HANDLE_DYNAMIC_TYPES`为需要处理的动态类型,目前支持文字动态,图文动态,投稿动态

(1)`dingding_config`下的参数
- `DINGDING_PUSH_ROBOT_TOKEN`为需要推送的钉钉Webhook机器人token
- `DINGDING_PUSH_ROBOT_SEC`为需要推送的钉钉Webhook机器人sec,选择加签模式则必填

#### 2. 填写defines配置信息
(1)`description`下的参数
- 多语言下的描述文件,可根据自己需要修改,支持makedown格式
  
#### 3.安装第三方库

`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

#### 4.启动脚本

`nohup python3 -u main.py >& Bilibili-Notification.log &`

## 感谢

- 特别感谢项目`bili_dynamic_push`的作者`nfe-w`提供的项目作为参考
