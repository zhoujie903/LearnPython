#!/usr/bin/env python3
# coding=utf-8

'''
王者大脑
'''
import asyncio
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
from same_hard import ti_xian_history, ti_xian, GameUser, framework_main

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)

logging.info(sys.stdout.encoding)

class User(GameUser):
    APP_ID_STR = 'a3NqP2sbHEzE' 
    APP_ID = 46 
    def __init__(self, session_data: dict):
        super().__init__(session_data) 

    def _header(self):
        return {
            # 'User-Agent': self.headers['User-Agent'],
            'user-agent': self.headers['user-agent'],
            # 'Cookie':self.headers['Cookie'],
        }

    def x_game_center_gapp_sign_in(self):
        logging.info('签到')

        url = self.urls['/x/game-center/gapp/sign-in']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_game_center_gapp_sign_in_double(self):
        logging.info('x_game_center_gapp_sign_in_double')

        url = self.urls['/x/game-center/gapp/sign-in-double']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def game_special_report(self, app_id, report_type='round'):
        logging.info('special_report')

        url = self.urls['/x/game-report/special_report']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['app_id'] = app_id
        data['report_type'] = report_type

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def game_duration_report(self, start_ts, duration, report_type='duration_addition'):
        logging.info('duration_report')

        url = self.urls['/x/game-report/duration_report']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['start_ts'] = start_ts
        data['duration'] = duration
        data['report_type'] = report_type

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_gapp_task_list(self, app, app_id):
        logging.info('游戏 - 任务列表')

        url = self.urls['/x/gapp/task/list']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['app'] = app
        data['app_id'] = app_id

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result


    def api_v1_z6qtt_sign(self):
        logging.info('王者大脑 - 签到')

        url = self.urls['/api/v1/z6qtt/sign']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_login(self, ticket):
        logging.info('王者大脑 - 获取open_id')

        url = self.urls['/api/v1/z6qtt/login']

        params = self._params_from(url)
        params['ticket'] = ticket

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_user_coin(self):
        logging.info('api_v1_z6qtt_user_coin')

        url = self.urls['/api/v1/z6qtt/user_coin']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_get_reward(self, activity_id=3, word='',key={}):
        '''
        activity_id: 3-时段签到 4-{'mission':11} 7-任务完成{'task':1,7}和不传task 6-福袋
        12-通过关卡{'level':4}  
        '''
        logging.info(f'王者大脑 - 任务完成 - {activity_id} - {key}')

        url = self.urls['/api/v1/z6qtt/get_reward']

        params = self._params_from(url)
        params['activity_id'] = activity_id
        params['word'] = word
        params['relive'] = 0
        for k,v in key.items():
            params[k] = v

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_updateinfo(self, info):
        '''
        "activeNum": 20-每日所有任务完成进度 20/120
        dayTaskList: "state": 0-去完成 2-可领取 1-已领取
        '''
        logging.info('api_v1_z6qtt_updateinfo')

        url = self.urls['/api/v1/z6qtt/updateInfo']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['data'] = json.dumps(info)

    
        result = self._get(url, params=params, data=data)
    
        # result = json.loads(result)
        return result

    def api_v1_z6qtt_round_report(self):
        logging.info('api_v1_z6qtt_round_report')

        url = self.urls['/api/v1/z6qtt/round_report']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_lottery(self):
        logging.info('王者大脑 - lottery')

        url = self.urls['/api/v1/z6qtt/lottery']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_add_coin(self):
        logging.info('王者大脑 - add_coin')

        url = self.urls['/api/v1/z6qtt/add_coin']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_open_redpacket(self):
        logging.info('王者大脑 - 红包')

        url = self.urls['/api/v1/z6qtt/open_redpacket']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result


    # 红包挑战
    def api_v1_z6qtt_get_rank(self):
        logging.info('王者大脑 - 判案比赛-排行')

        url = self.urls['/api/v1/z6qtt/get_rank']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_get_rank_reward(self):
        logging.info('王者大脑 - 判案比赛-领奖')

        url = self.urls['/api/v1/z6qtt/get_rank_reward']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.info)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_upload_rank(self, score):
        logging.info('王者大脑 - 判案比赛')

        url = self.urls['/api/v1/z6qtt/upload_rank']

        params = self._params_from(url)
        params['score'] = score

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_z6qtt_exchange(self):
        logging.info('api_v1_z6qtt_exchange')

        url = self.urls['/api/v1/z6qtt/exchange']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

def dayly_sign(user: User):
    user.x_game_center_gapp_sign_in()
    user.x_game_center_gapp_sign_in_double()


# Tudo
def task(user: User, info):
    # info['brainTodayCount'] += 1 
    # info['dailyPoints'] = [120003, 120005, 120007]
    dayTaskList = info['dayTaskList']
    for task in dayTaskList:
        dayTaskList[task]['state'] = 2
        dayTaskList[task]['process'] = 3

    # user.api_v1_z6qtt_updateinfo(info)
    # 不用updateinfo,get_reward获取金币成功，但102，104，109失败 
    # 1-签到 2-通关5个关卡[红包] 5-开启3个红包[红包] 3-使用2次提示；6-领取3次趣金币；4-观看3个视频；7-完成1次挑战赛[红包]；
    for task in dayTaskList:
        task_id = dayTaskList[task]['id']
        state = dayTaskList[task]['state']
        if not state == 1:
            user.api_v1_z6qtt_get_reward(activity_id=7, key={'task': task_id})
            
def lottery(user: User):
    '''
    每天最多开启10个红包
    '''
    for _ in range(30):
        result = user.api_v1_z6qtt_lottery()
        if not result['code'] == 1:
            break

def open_redpacket(user: User):
    for _ in range(6):
        result = user.api_v1_z6qtt_open_redpacket()
        if result['code'] == 0:
            break

def add_coin(user: User):
    for _ in range(10):
        result = user.api_v1_z6qtt_add_coin()
        if result['code'] == 0:
            break

def rank(user: User):
    result = user.api_v1_z6qtt_get_rank()
    userData = result['data']['userData']
    rank = userData['rank']
    if rank > 9 or rank == 0:
        new_rank = random.randint(1, 9) - 1
        rankList = result['data']['rankList']
        person = rankList[new_rank]
        new_score = float(person['score']) - 0.2
        logging.info(f'以 {new_score} 排名 {new_rank}')
        user.api_v1_z6qtt_upload_rank(new_score)

def activity_id_6(user: User):
    logging.info('''6-判案结束后的福袋''')
    for i in range(1, 32):
        logging.info(i)
        result = user.api_v1_z6qtt_get_reward(activity_id=6)
        if not result['code'] == 1:
            break
        time.sleep(1)

def activity_id_12(user: User):
    logging.info('''12-通过关卡{'level':4}''')
    # [4,7, 10, 13, 20, 26]
    for level in [4,7, 10, 13, 20, 26]:
        result = user.api_v1_z6qtt_get_reward(activity_id=12, key={'level':level})
        if not result['code'] == 1:
            break
        time.sleep(1)

async def run(runner, user: User):
    # 获取g_token 
    user._setup_g_token()

    # 获取ticket
    ticket = user.get_ticket(User.APP_ID_STR)

    result = user.api_v1_z6qtt_login(ticket)
    puid = result['data']['puid']
    open_id = result['data']['open_id']
    nickname = result['data']['nickname']
    cash = result['data']['cash']
    data = result['data']['data']
    data = json.loads(data)

    logging.info(f'\033[1;31m{nickname} {cash=}, {open_id=} {puid=} \033[0m')
    if cash >= 20 * 100:
        user.api_v1_z6qtt_exchange()

    user.params['puid'] = puid
    user.params['open_id'] = open_id


    tasks = [
        User.api_v1_z6qtt_sign,
        partial(task, info=data),
        rank,
        User.api_v1_z6qtt_get_rank_reward,
        lottery,

        User.api_v1_z6qtt_get_reward,

        activity_id_6,
        User.api_v1_z6qtt_user_coin,

        # ti_xian,
        # # activity_id_12,#failed
    ]
    for t in tasks:
        runner.send(t)



def genUsers():
    for session_data in users:
        yield User(session_data)

if __name__ == "__main__":
    framework_main(run, genUsers())