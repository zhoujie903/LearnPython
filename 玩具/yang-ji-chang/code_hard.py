#!/usr/bin/env python3
# coding=utf-8

'''
欢乐养鸡场
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
from same_hard import ti_xian, ti_xian_history, income, GameUser, framework_main

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)

class User(GameUser):
    APP_ID_STR: str = 'a3MddYAXrTjG'
    APP_ID: int = 20

    def __init__(self, session_data: dict):
        super().__init__(session_data) 

    def _header(self):
        return {
            # 'User-Agent': self.headers['User-Agent'],
            'user-agent': self.headers['user-agent'],
            # 'Cookie':self.headers['Cookie'],
        }

    def x_middle_open_user_ticket(self):
        logging.info('欢乐养鸡场 - 获取s_token')

        url = self.urls['/x/middle/open/user/ticket']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_chicken_task_get_list(self):
        logging.info('x_chicken_task_get_list')

        url = self.urls['/x/chicken/task/get-list']

        params = self._params_from(url)

        data = self._bodys_from(url)


        result = self._post(url, params=params, data=data)

        result = json.loads(result)
        return result

    def x_chicken_info(self):
        logging.info('欢乐养鸡场 - 信息')

        url = self.urls['/x/chicken/info']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result
        
    # Todo:失败
    def x_chicken_feed(self):
        logging.info('喂饲料')

        url = self.urls['/x/chicken/feed']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_chicken_get_fodder(self, again, id, pos):
        logging.info(f'领饲料 - {id} - {pos} - {again}')

        url = self.urls['/x/chicken/get-fodder']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['again'] = again
        data['id'] = id
        data['pos'] = pos


        result = self._post(url, params=params, data=data)

        result = json.loads(result)
        return result

    def x_chicken_video_accomplish(self):
        logging.info('x_chicken_video_accomplish')

        url = self.urls['/x/chicken/video/accomplish']

        params = self._params_from(url)

        data = self._bodys_from(url)
    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_chicken_task_take_award(self, task_id):
        logging.info('达标领奖励')

        url = self.urls['/x/chicken/task/take-award']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['task_id'] = task_id 

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_chicken_speed_up(self):
        logging.info('x_chicken_speed_up')

        url = self.urls['/x/chicken/speed-up']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result


    # 翻翻乐
    def x_middle_flop_take_reward(self):
        logging.info('x_middle_flop_take_reward')

        url = self.urls['/x/middle/flop/take-reward']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_middle_flop_info(self):
        logging.info('欢乐养鸡场 - 翻翻乐 - 信息')

        url = self.urls['/x/middle/flop/info']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_middle_flop_start(self):
        logging.info('欢乐养鸡场 - 翻翻乐 - 开始')

        url = self.urls['/x/middle/flop/start']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def x_middle_flop_video(self):
        logging.info('x_middle_flop_video')

        url = self.urls['/x/middle/flop/video']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    # 砸蛋
    def x_chicken_add_hit_count(self):
        logging.info('欢乐养鸡场 - 增加砸蛋机会')

        url = self.urls['/x/chicken/add-hit-count']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_chicken_hit_egg_award(self, again):
        logging.info('x_chicken_hit_egg_award')

        url = self.urls['/x/chicken/hit-egg/award']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['again'] = again

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result



def setup(user: User):
    # result = user.x_user_token()
    # g_token = result['data']['g_token']
    # user.params['g_token'] = g_token
    user._setup_g_token()

    result = user.x_open_game(app_id=User.APP_ID_STR)
    url = result['data']['url']
    a = urlparse(url)
    d = dict()
    for item in a.query.split('&'):
        q = item.split('=')
        d[q[0]] = q[1]
        user.params[q[0]] = q[1]
        user.bodys[q[0]] = q[1]
    # logging.info(d)
    m = re.search("ticket=(\\w+)", url, re.M)
    ticket = m.group(1)
    user.params['ticket'] = ticket


    result = user.x_middle_open_user_ticket()
    s_token = result['data']['s_token']
    open_id = result['data']['open_id']
    nickname = result['data']['nickname']
    user.params['s_token'] = s_token
    user.bodys['s_token'] = s_token
    # logging.info(f'{nickname=}, {open_id=}, {s_token=}')

def task(user: User):
    try:
        result = user.x_chicken_task_get_list()
        task_list = result['data']['task_list']
        for item in task_list:
            cur_num = item['cur_num']
            all_num = item['all_num']
            task_id = item['task_id']
            award_state = item['award_state']
            if cur_num >= all_num and award_state == 1:
                user.x_chicken_task_take_award(task_id)

    except Exception:
        traceback.print_exc()

def hit_egg(user: User):
    try:
        have_hit_count = user.have_hit_count
        hit_egg_day_can_count = user.hit_egg_day_can_count # 初始值为2
        video_award_count = user.video_award_count # 初始值为0 

        if have_hit_count == 0 and hit_egg_day_can_count > video_award_count:
            result = user.x_chicken_add_hit_count()            
            have_hit_count = result['data']['have_hit_count']
            hit_egg_day_can_count = result['data']['hit_egg_day_can_count']

        # 砸蛋
        for _ in range(have_hit_count):
            result = user.x_chicken_hit_egg_award(0)
            can_again = result['data']['can_again']
            if can_again:
                user.x_chicken_hit_egg_award(1)
        

    except Exception:
        traceback.print_exc()
    pass
    
def flop(user: User):
    try:
        result = user.x_middle_flop_info()
        physical = result['data']['physical']
        logging.info(f'翻翻乐 - {physical} 次')
        # if physical:
        for _ in range(physical):
            user.x_middle_flop_start()
            user.x_middle_flop_video()
            user.x_middle_flop_take_reward()
            time.sleep(1)
    except Exception as e:
        traceback.print_exc()

def get_fodder(user: User, fodder_item: list):
    #   {
    #     "id": 1,
    #     "pos": 1,
    #     "is_need_ad": 0,
    #     "mature_time": 1578033228,
    #     "day_fodder_count": 2,
    #     "day_can_count": 4,
    #     "again_fodder": 15
    #   },
    logging.info(' - 饲料信息 - ')
    for item in fodder_item:
        i = item['id']
        pos = item['pos']
        mature_time = item['mature_time']
        day_fodder_count = item['day_fodder_count']
        day_can_count = item['day_can_count']
        logging.info(f"{i} - {pos} - {time.strftime('%X',time.localtime(mature_time))}")
        if int(time.time()) >= mature_time and day_fodder_count < day_can_count:
            result = user.x_chicken_get_fodder(0,i,pos)
            if result['code'] == 0 and result['data']['can_again'] == 1:
                user.x_chicken_get_fodder(1,i,pos)

async def run(runner, user: User):
    localtime = time.localtime(time.time())
    # if localtime.tm_hour in range(0, 6):
    #     return

    setup(user)
    
    result = user.x_chicken_info()
    cur_fodder = result['data']['cur_fodder']
    cur_fodder = result['data']['cur_fodder']
    fodder_item = result['data']['fodder_item']
    day_max_feed_num = result['data']['day_max_feed_num']
    day_feed_num = result['data']['day_feed_num']
    left_can_speed_up = result['data']['left_can_speed_up']
    have_hit_count = result['data']['have_hit_count']
    hit_egg_day_can_count = result['data']['hit_egg_day_can_count']
    video_award_count = result['data']['video_award_count']

    user.have_hit_count = have_hit_count
    user.hit_egg_day_can_count = hit_egg_day_can_count
    user.video_award_count = video_award_count

    # 加速
    if left_can_speed_up:
        user.x_chicken_speed_up()

    # 砸蛋
    hit_egg(user)

    get_fodder(user, fodder_item)
    
    need_run = localtime.tm_hour % 8 == 0
    need_run = True
    if need_run == True:
        task(user)

    logging.info(f' 饲料 = {cur_fodder}')
    if cur_fodder and day_feed_num < day_max_feed_num:
        for _ in range(3):
            result = user.x_chicken_feed()
            if result['code'] == 10000:
                break
            if result['code'] == 10005:
                # 'code': 10005, 'message': '您没有完成激励任务哦'
                user.x_chicken_video_accomplish()
            if result['code'] == 0:
                cur_fodder = result['data']['cur_fodder']
            time.sleep(4)

    flop(user)


    # ti_xian(user)
    # ti_xian_history(user)
    # # income(user) 


def genUsers():
    for session_data in users:
        yield User(session_data)

if __name__ == "__main__":
    framework_main(run, genUsers())