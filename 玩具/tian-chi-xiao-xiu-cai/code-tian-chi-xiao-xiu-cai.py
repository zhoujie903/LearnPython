#!/usr/bin/env python3
# coding=utf-8

'''
填词小秀才app - 自动化
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
from same_hard import ti_xian_history, ti_xian, GameUser, framework_main

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)

logging.info(sys.stdout.encoding)

class User(GameUser):
    APP_ID_STR = "a3NqMwuuoZCC"
    APP_ID = 40
    def __init__(self, session_data: dict): 
        super().__init__(session_data)

    def _header(self):
        return {
            # 'User-Agent': self.headers['User-Agent'],
            'user-agent': self.headers['user-agent'],
            # 'Cookie':self.headers['Cookie'],
        }


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


    def api_v1_tczyapp_sign(self):
        logging.info('填词小秀才 - 签到')

        url = self.urls['/api/v1/tczyapp/sign']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_event(self,event):
        logging.info('api_v1_tczyapp_event')

        url = self.urls['/api/v1/tczyapp/event']

        params = self._params_from(url)
        params['event'] = event

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        # result = json.loads(result)
        return result

    def api_v1_tczyapp_login(self, ticket):
        logging.info('填词小秀才 - 获取open_id')

        url = self.urls['/api/v1/tczyapp/login']

        params = self._params_from(url)
        params['ticket'] = ticket

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_user_coin(self):
        logging.info('api_v1_tczyapp_user_coin')

        url = self.urls['/api/v1/tczyapp/user_coin']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_get_reward(self, activity_id=3, word='',key={}):
        '''
        activity_id: 3-时段签到 5-任务完成 6-判案结束后的福袋
        12-通过关卡{'level':4} 11-抽字凑齐成语{'word':'一帆风顺'} 
        '''
        logging.info(f'填词小秀才 - 任务完成 - {activity_id} - {key}')

        url = self.urls['/api/v1/tczyapp/get_reward']

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

    def api_v1_tczyapp_updateinfo(self, info):
        '''
        "activeNum": 20-每日所有任务完成进度 20/120
        dayTaskList: "state": 0-去完成 2-可领取 1-已领取
        '''
        logging.info('api_v1_tczyapp_updateinfo')

        url = self.urls['/api/v1/tczyapp/updateInfo']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['data'] = json.dumps(info)

    
        result = self._get(url, params=params, data=data)
    
        # result = json.loads(result)
        return result

    def api_v1_tczyapp_get_words_info(self):
        logging.info('api_v1_tczyapp_get_words_info')

        url = self.urls['/api/v1/tczyapp/get_words_info']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_draw_a_char(self):
        logging.info('填词小秀才 - 抽字')

        url = self.urls['/api/v1/tczyapp/draw_a_char']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_round_report(self):
        logging.info('api_v1_tczyapp_round_report')

        url = self.urls['/api/v1/tczyapp/round_report']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_lottery(self):
        logging.info('填词小秀才 - lottery')

        url = self.urls['/api/v1/tczyapp/lottery']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_add_coin(self):
        logging.info('填词小秀才 - add_coin')

        url = self.urls['/api/v1/tczyapp/add_coin']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_open_redpacket(self):
        logging.info('填词小秀才 - 红包')

        url = self.urls['/api/v1/tczyapp/open_redpacket']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result


    # 红包挑战
    def api_v1_tczyapp_get_rank(self):
        logging.info('填词小秀才 - 判案比赛-排行')

        url = self.urls['/api/v1/tczyapp/get_rank']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_get_rank_reward(self):
        logging.info('填词小秀才 - 判案比赛-领奖')

        url = self.urls['/api/v1/tczyapp/get_rank_reward']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.info)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_upload_rank(self, score):
        logging.info('填词小秀才 - 判案比赛')

        url = self.urls['/api/v1/tczyapp/upload_rank']

        params = self._params_from(url)
        params['score'] = score

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def api_v1_tczyapp_exchange(self):
        logging.info('填词小秀才 - 红包满20元兑换成金币')

        url = self.urls['/api/v1/tczyapp/exchange']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

def dayly_sign(user: User):
    user.x_game_center_gapp_sign_in()
    user.x_game_center_gapp_sign_in_double()

def draw_a_char(user: User):
    for _ in range(4):
        # {'code': 1, 'data': {'word': '一团和气', 'char': '气', 'chars': [['一', 10], ['千', 1], ['团', 3], ['字', 1], ['帆', 5], ['气', 3], ['言', 2], ['顺', 4], ['风', 3], ['鼎', 1]]}}
        result = user.api_v1_tczyapp_draw_a_char()
        word = result['data']['word']
        # char = result['data']['char']
        chars = dict(result['data']['chars'])
        missing = set(word) - set(k for k, v in chars.items() if v>0)
        if len(missing) == 0:
            result = user.api_v1_tczyapp_get_reward(activity_id=11, word=word)
            if result['code'] == 0:
                break

# Tudo
def task(user: User, info):
    info['cmpCount'] += 1 
    info['dailyPoints'] = [120003, 120005, 120007]
    dayTaskList = info['dayTaskList']
    for task in dayTaskList:
        dayTaskList[task]['state'] = 2
        dayTaskList[task]['process'] = 3

    # user.api_v1_tczyapp_updateinfo(info)
    # 不用updateinfo,get_reward获取金币成功，但102，104，109失败 
    # 102-通关5个关卡[红包] 104-开启3个红包[红包] 103-使用3次提示；105-领取3次趣金币；107-观看5个视频；109-参与1次判案玩法[红包]；
    # 102\104\109是红包奖励，get_reward是得金币的，没有这些任务；应该用tczyapp_lottery
    for task in dayTaskList:
        task_id = dayTaskList[task]['id']
        state = dayTaskList[task]['state']
        if not state == 1:
            user.api_v1_tczyapp_get_reward(activity_id=5, key={'task': task_id})
            
def lottery(user: User):
    '''
    每天最多开启10个红包
    '''
    for _ in range(30):
        result = user.api_v1_tczyapp_lottery()
        if not result['code'] == 1:
            break

def open_redpacket(user: User):
    for _ in range(6):
        result = user.api_v1_tczyapp_open_redpacket()
        if result['code'] == 0:
            break

def add_coin(user: User):
    for _ in range(10):
        result = user.api_v1_tczyapp_add_coin()
        if result['code'] == 0:
            break

def rank(user: User):
    result = user.api_v1_tczyapp_get_rank()
    userData = result['data']['userData']
    rank = userData['rank']
    # score = userData['score']
    if rank > 9 or rank == 0:
        new_rank = random.randint(1, 9) - 1
        rankList = result['data']['rankList']
        person = rankList[new_rank]
        new_score = float(person['score']) - 0.2
        logging.info(f'以 {new_score} 排名 {new_rank}')
        user.api_v1_tczyapp_upload_rank(new_score)

def activity_id_6(user: User):
    logging.info('''6-判案结束后的福袋''')
    for _ in range(6):
        result = user.api_v1_tczyapp_get_reward(activity_id=6)
        if not result['code'] == 1:
            break

def activity_id_12(user: User):
    logging.info('''12-通过关卡{'level':4}''')
    # [4,7, 10, 13, 20, 26]
    for level in [4,7, 10, 13, 20, 26]:
        result = user.api_v1_tczyapp_get_reward(activity_id=12, key={'level':level})
        # if not result['code'] == 1:
        #     break
        time.sleep(1)



def genUsers():
    for session_data in users:
        yield User(session_data)


def run(runner, user: User):
    # 获取g_token 
    user._setup_g_token()

    # 获取ticket
    ticket = user.get_ticket(User.APP_ID_STR)

    result = user.api_v1_tczyapp_login(ticket)
    puid = result['data']['puid']
    open_id = result['data']['open_id']
    nickname = result['data']['nickname']
    cash = result['data']['cash']
    new_cash = result['data']['new_cash']
    utag = result['data']['utag']
    data = result['data']['data']
    data = json.loads(data)

    logging.info(f'\033[1;31m{nickname} {cash=}, {new_cash=}, {open_id=} {puid=} {utag=}\033[0m')
    if cash >= 20:
        user.api_v1_tczyapp_exchange()

    user.params['puid'] = puid
    user.params['open_id'] = open_id
    user.params['utag'] = utag


    # user.game_special_report(User.APP_ID_STR)


    tasks = [
        dayly_sign,
        User.api_v1_tczyapp_sign,
        partial(task, info=data),
        activity_id_6,
        rank,
        User.api_v1_tczyapp_get_rank_reward,
        lottery,

        draw_a_char,
        add_coin,
        User.api_v1_tczyapp_get_reward,

        User.api_v1_tczyapp_user_coin,
        
        # ti_xian
        # ti_xian_history
        # activity_id_12,
    ]
    for t in tasks:
        runner.send(t)

if __name__ == "__main__":
    framework_main(run, genUsers())