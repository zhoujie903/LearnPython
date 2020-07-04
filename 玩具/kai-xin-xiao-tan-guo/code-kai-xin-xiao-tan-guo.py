#!/usr/bin/env python3
# coding=utf-8

'''
代码模板
'''

import json
import logging
import pathlib
import random
import re
import sys
import time
import traceback
from functools import partial
from urllib.parse import urlparse

import requests

from sessions import users
from same_hard import ti_xian, ti_xian_history, income, GameUser, framework_main

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)

logging.info(sys.stdout.encoding)

class User(GameUser):
    def __init__(self, session_data: dict):
        super().__init__(session_data) 

    def _header(self):
        return {
            'User-Agent': self.headers['User-Agent'],
            'user-agent': self.headers['user-agent'],
            # 'Cookie':self.headers['Cookie'],
        }

    def x_cocos_gapp_game_init(self, params_as_all):
        logging.info('x_cocos_gapp_game_init')

        url = self.urls['/x/cocos/gapp-game-init']

        params = self._params_from(url)
        params = params_as_all

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def x_user_token(self):
        logging.info('/x/user/token - 获取g_token')

        url = self.urls['/x/user/token']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def happy_qtt_apkuserinfo(self, ticket):
        logging.info('游戏 - 糖果 - 获取open_id')

        url = self.urls['/happy/qtt/apkuserinfo']

        params = self._params_from(url)
        params['ticket'] = ticket

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def happy_protocol(self, vv=None):
        logging.info(f"happy_protocol - {vv['data'][1][0]['method']}")

        url = self.urls['/happy/protocol']

        params = self._params_from(url)
        params['uid'] = 1

        data = self._bodys_from(url)
        data['data'] = json.dumps(vv)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result




def common_data(user: User):

    # 一般不变量
    appVersion = '1.0.1'
    deviceModel = 'test'
    apkVersion = '1.0.1'
    data = {
        "openId": user.open_id,
        "gender": 0,
        "province": "",
        "appVersion": appVersion,
        "deviceModel": deviceModel,
        "apkVersion": apkVersion
    } 
    return data

def doLogin(user: User):
    # 获取uk, uid
    data = dict()
    method = [
        {
            "method": "doLogin",
            "openId": user.open_id,
            "nickName": user.nickname,
            "avatarUrl": user.avatar,
        }
    ] 
    data['data'] = [common_data(user), method]
    return user.happy_protocol(vv=data)

def addQttCoin(user: User):
    m = {
        "method": "addQttCoin",
        "addQttCoin": 90
    }

    for _ in range(20):
        result = common_method(user, m)
        if result['addQttCoin']['qttCoinDayLimit']:
            break
        time.sleep(1)

def receiveDailyLoginReward(user: User):
    m = {
        "method": "receiveDailyLoginReward",
        "doubleReward": True,
        "receiveType": 0
    }
    return common_method(user, m)

def receiveTaskReward(user: User):
    m = {
        "method": "receiveTaskReward",
        "propId": 1000,
        "num": 10000,
        "taskId": "task0"
    }
    return common_method(user, m)

def user_info(user: User):
    m = {
        "method": "user",
        "nickName": user.nickname
    } 
    result = common_method(user, m)
    qttCoin = result['user']['qttCoin']
    logging.info(f"\033[1;31m{user.nickname} {qttCoin}\033[0m")

def common_method(user: User, m: dict):
    data = dict()
    xxx = common_data(user)
    xxx['uid'] = user.uid
    xxx['uk'] = user.uk

    method = [
        m
    ]
    data['data'] = [xxx, method]

    return user.happy_protocol(vv=data)

def genUsers():
    for session_data in users:
        yield User(session_data)

def run(runner, user: User):
    '''
    用户代码
    '''
    user._setup_g_token()

    # 设置g_token

    # 获取ticket 
    item = user.params_as_all['/x/cocos/gapp-game-init'][0]
    result = user.x_cocos_gapp_game_init(item)
    url = result['data']['h5_game_info']['url']
    m = re.search("ticket=(\\w+)", url, re.M)
    ticket = m.group(1)

    # 获取open_id
    result = user.happy_qtt_apkuserinfo(ticket)
    open_id = result['data']['open_id']
    nickname = result['data']['nickname']
    avatar = result['data']['avatar']

    logging.info(f'{open_id}, {nickname}')
    user.open_id = open_id
    user.nickname = nickname
    user.avatar = avatar

    # 用户登录 
    result = doLogin(user)
    uk = result['doLogin']['uk']
    uid = result['doLogin']['uid']
    user.uk = uk
    user.uid = uid



    addQttCoin(user)

    receiveDailyLoginReward(user)

    user_info(user)

if __name__ == "__main__":
    framework_main(run, genUsers())