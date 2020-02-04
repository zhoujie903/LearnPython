#!/usr/bin/env python3
# coding=utf-8

'''
# 趣消除App-成语消消乐全自动化；
# App版本：1.1.2
# App地址：https://itunes.apple.com/cn/app/id1449545954
提现非常迅速
'''

import re
import time
import datetime
import random
import json
import sys
import logging
import collections
import pathlib

import requests

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)


Red = '\033[0;31m'
Green = '\033[0;32m'
Yellow = '\033[0;33m' 
Blue = '\033[0;34m'
Purple = '\033[0;35m' 
Cyan = '\033[0;36m'  
White = '\033[0;37m' 

colors = {
    0:Red,
    1:Purple,
    2:Yellow,
    3:Blue,
    4:White,
}


# 这些变量的值可以通过像Charles抓包软件获得
# 账号变量
# ------------------------------------------------
# A_Token_Header的一些结论：
# 1.由接口api/v1/sessions/create_oauth2返回


# Cookie的一些结论：
# 1.同一个账号，退出或再登录，都不用修改，一直有效
# 2.值为空也可以

# UUID的一些结论：
# 1.固定不变
UUID_her = '152095'

# wisedom - 扶我起来学数学
# ------------------------------------------------
# ------------------------------------------------


# hexgon - 六角英雄 
# ------------------------------------------------
data_her = {
    'channel': '90000',
    'code': '9FB3B4B7-75A2-4A5D-9004-C59EEF09931F',
    'gtype': 'hexgon',
    'hash': 'ece00508057a6de77c62390242f34650',
    'muid': 'C5AE84F2-18D0-4BB8-B11F-5D962C555543',
    'oatype': 'dev',
    'os': 'ios',    
}
# ------------------------------------------------



class QuXiaoChuUser():
    headers = {
        'Host': 'mapi.hddgood.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'Origin': 'http://hexgoncdn.hddgood.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hddhexgon/ios1.0.0',
        'Referer': 'https://mapi.hddgood.com/'
    }

    SLEEP = 0.5

    def __init__(self, data):
        self.headers = dict(QuXiaoChuUser.headers)
        self.data = data

        self.session = requests.Session()
        self.session.headers = dict(QuXiaoChuUser.headers)

    def sessions_create_oauth2(self):
        '''
        获取atoken: A-Token-Header	Oi9KUFdWU0pFH0INWlQMdRlVVVU=
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"id":145696,"unionid":"wisedom-AF202DCF-F89A-4812-9A9F-A05A171477D2","nick":"新人77D2","acc":"","atoken":"MipcUFdWU0pFH0INWlQNIRcFAAY=","rtoken":"Z3cbRFxQFQQb","accesskey":null,"gift":null}}
        '''
        print("获取atoken: A-Token-Header")

        # api = self._genapi('sessions/create_oauth2')
        api = 'https://mapi.hddgood.com/api/v1/sessions/create_oauth2'
        result = self._post(api, self.data) 

        result = json.loads(result)
        atoken = result['result']['atoken']
        self.token_header = atoken
        self.session.headers['A-Token-Header'] = self.token_header

        uid = result['result']['id']
        self.uid = uid
        
        nick = result['result']['nick']
        self.nick = nick
        print(f'uid = {uid} nick = {nick} atoken = {atoken}')


    def game_chengyu_join_game(self, rank):
        '''
        成语消消乐-获取游戏id
        https://king.hddgood.com/king_api/v1/game/join_game
        六角英雄：https://mapi.hddgood.com/api/v1/king/game/join_game
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"gameid":"G15-3232777","dup":0,"starter":531492}}
        '''
        print("成语消消乐-获取游戏id {}".format(self.uid))

        data = self._uid_data()
        # 1:书童；2:儒生；15:殿阁大学士
        data['rank'] = str(rank) 
        data['type'] = 'G'

        api = self._genapi('game/join_game')
        result = self._post(api, data) 
        return json.loads(result)       

    def _uid_data(self):
        return {'uid': self.uid}

    @staticmethod
    def _genapi(path):
        return 'https://mapi.hddgood.com/api/v1/king/' + path

    def _post(self, api, data, p=logging.warning):
        time.sleep(QuXiaoChuUser.SLEEP)

        res = self.session.post(api, data=data)
        print(res.url)
        result = res.text
        print(result)
        print('')
        return result


class Chengyu(object):
    def __init__(self):
        self.dictpath = '/Users/zhoujie/chengyu.text'
        self.chengyu = set()
        with open(self.dictpath, 'rt') as f:
            for line in f.readlines():
                self.chengyu.add(line.strip())

        self.answers = list()
        self.ask_string = ''

        # {'和':[1,8], '我':[11]}
        self.char_indexs_dict = dict()

        # {1:'和', 8:'和', 11:'我'}
        self.index_char_dict = dict()

        self.count = 0

        # 自动提交答案的网络发送次数
        self.auto_send_count = 0

        # 自动发送的成语
        self.auto_send_list = list()

        # 服务器确定正确的成语
        self.ack_true_list = list()

        # {'中流砥柱':[1,9,21,25]}
        self.answer_indexs_dict = dict()

        # 查找到的错误答案
        self.error_answers = []

        # 玩了多少局
        self.play_times = 0

        self.firt_auto_answer = True
    # ---------------------------------------------
    def find_answers_v2(self, ask_string):
        '''
            在内存成语字典查找答案
        '''
        ask_set = set(ask_string)
        for i, c in enumerate(ask_string):
            self.char_indexs_dict.setdefault(c, []).append(i)
        self.index_char_dict = dict( zip(range(len(ask_string)), ask_string))

        used_chars = set()
        # 找到的的成语中各异字符为2个的答案数量：如 [真真假假]
        answer_2chars_count = 0
        max_count = len(ask_string) / 4
        for item in self.chengyu:
            item_set = set(item)
            if not (item_set - ask_set):
                self.answers.append(item)
                used_chars.update(item_set)
                if len(item_set)<4:
                    answer_2chars_count += 1
                if len(self.answers) - answer_2chars_count >= max_count and used_chars >= ask_set:
                    self.count = len(self.answers)
                    return
        self.count = len(self.answers)

    async def auto_answer(self, flow):
        while len(self.answers) > 0:
            item = self.answers[0]
            answer_index = []
            counter = collections.Counter(item)

            b_continue = False
            for char, count in counter.items():
                if len(self.char_indexs_dict[char]) < count:
                    self.error_answers.append(item)
                    self.answers.remove(item)
                    b_continue = True
                    break # break for

            if b_continue:
                continue

            char_index = {}
            for c in item:                
                x = char_index.get(c, 0)
                index = self.char_indexs_dict[c][x]
                answer_index.append( str(index) )
                char_index[c] = x+1

            if len(set(answer_index)) < 4:
                print(f'?算法有错误：{answer_index} 小于4')
                continue

            send_message = {
                'answer': item,
                'answer_index': answer_index,
                'type': 'answer'
            }
            mm = json.dumps(send_message)
            # -----------------------
            print(mm)
            # -----------------------
            self.answer_indexs_dict[item] = answer_index
            # 向服务器发送消息
            self.firt_auto_answer = False
            self.auto_send_count += 1
            self.auto_send_list.append(item)
            self.answers.remove(item)
            time.sleep(1.5)
            await flow.send(mm)
            break


    def add_new_worlds_to_memory(self, m):
        '''
            把答案增加到内存字典中
        '''
        for answer in m['all_answer']:
            self.chengyu.add(answer['phrase'])

        print('\033[1;31m 共收录{}个成语 \033[0m'.format(len(self.chengyu)))
        print(f'\033[1;31m 共玩了 {self.play_times} 局\033[0m')

    def add_new_worlds_to_file(self, m):
        '''
            把答案增加到文件中
        '''
        if len(self.ack_true_answers) < len(m['all_answer']) and self.play_times % 5 == 0:
            with open(self.dictpath, 'wt') as f:
                l = list(self.chengyu)
                l.sort()
                for item in l:
                    f.write(item)
                    f.write('\n')

    def print_answers(self):
        '''
            图形化、色彩化显示答案
        '''
        logging.info('')
        self.print_color(self.ask_string)
        self.print_color('共找到 {}/{} 个成语'.format(self.count, len(self.ask_string)//4))
        self.print_color('错误成语 {}'.format(self.error_answers))
        self.print_color('共自动 {} 次提交'.format(self.auto_send_count))
        self.print_color('自动{:2}个：{}'.format(len(self.auto_send_list),self.auto_send_list))
        self.print_color('确认{:2}个：{}'.format(len(self.ack_true_list),self.ack_true_list))
        # for item in self.answers:
        #     self.print_color(item)
        #     self.print_matrix(item)

        # if (not self.answers) and self.index_char_dict:
        #     self.print_matrix()

    def print_matrix(self, item = []):
        '''
        item: '腊尽春回' or []
        '''
        chars_in_line = 6
        length = len(self.ask_string)

        lines = (length + chars_in_line - 1) // chars_in_line
        PADDING = ' '*(lines * chars_in_line - length)
        is_need_padding = len(PADDING) != 0

        global colors, White
        
        self.print_color('--'*chars_in_line)

        for i, c in self.index_char_dict.items():
            end = ''
            if (i+1) % chars_in_line == 0 or (i+1) == length:
                end = '\n'

            color = White
            if c in item:
                color = colors[item.index(c)]

            line, first = divmod(i, chars_in_line)
            if is_need_padding and first == 0 and (line + 1 == lines):
                c = PADDING + c

            self.print_color(c, end=end, front_color=color)

        self.print_color('--'*chars_in_line)

    def print_color(self, message, end='\n', front_color=Red):
        print(f'{front_color}{message}\033[0m', end=end)


    def reset_data_to_init(self):
        self.ask_string = ''
        self.answers.clear()
        self.index_char_dict.clear()

        self.count = 0
        self.auto_send_count = 0

        self.answer_indexs_dict.clear()
        self.char_indexs_dict.clear()
        self.error_answers.clear()
        self.ack_true_list.clear()
        self.auto_send_list.clear()
        self.firt_auto_answer = True

def chengyu_auto_answer(user: QuXiaoChuUser):
    '''
    成语消消乐自动答题
    wss://king.hddgood.com/websock_m/websock_message?uid=472251&gameid=G15-3232777&token=JSdLVVRRV0ZCH0INUlYNchcDUlc=
    wss://mapi.hddgood.com/websock_m/websock_message?uid=152095&gameid=G15-13129506&token=PjdDUFZRVUpGH0NfWwRbdh1SUgI=
    '''
    result = user.game_chengyu_join_game(g_rank)
    if result['success']:
        gameid = result['result']['gameid']
        url = 'wss://mapi.hddgood.com/websock_m/websock_message?uid={}&gameid={}&token={}'
        url = url.format(user.uid, gameid, user.token_header)
        print(url)

        import asyncio
        import websockets

        async def chengyu():
            coins = 0
            async with websockets.connect(url) as websocket:
                print('连接成功')
                global chengyu
                live = True
                count = 0
                while live:

                    if count % 10 == 0:
                        keeplive = json.dumps({"type":"keepalive"})
                        await websocket.send(keeplive)
                        print('send keeplive')

                    # await asyncio.sleep(0.5)                    
                    count += 1

                    m = await websocket.recv()
                    print(f"\n{m}\n")

                    m = json.loads(m)
                    message_type = m['type']
                    if m.get('ask_string'):
                        chengyu.ask_string = m['ask_string']        
                        # 计算答案
                        chengyu.find_answers_v2(chengyu.ask_string)
                        chengyu.play_times += 1

                    if message_type == 'answer':
                        chengyu.answer_indexs_dict[m['answer']] = m['answer_index']


                    # 删除已回答正确的答案
                    ack = False

                    # {"answer":"长驱直入","type":"answer_ack","seq":0,"ack":1}
                    if m.get('ack') == 1:

                        answer = m['answer']
                        chengyu.ack_true_list.append(answer)
                        answer_index = chengyu.answer_indexs_dict.get(answer,[])
                        for i in answer_index:
                            chengyu.index_char_dict[int(i)] = '  '

                        for c,i in zip(answer,answer_index):                
                            indexs = chengyu.char_indexs_dict[c]
                            indexs.remove(int(i))

                        try:
                            ack = True
                            chengyu.answers.remove(m['answer'])
                        except:
                            pass


                    # 自动答题
                    if message_type == 'answer_ack' or chengyu.firt_auto_answer:
                        await chengyu.auto_answer(websocket)

                    # 显示答案
                    if len(chengyu.ask_string):
                        chengyu.print_answers()

                    
                    if message_type == 'game_result':
                        live = False
                        # 把答案增加到内存字典中
                        chengyu.add_new_worlds_to_memory(m)

                        chengyu.reset_data_to_init()


                        # 其它解析
                        for item in m['scores']:
                            if str(item['uid']) == user.uid:
                                global g_rank
                                g_rank = item['rank'] 
                        coins = m['coin']
                        print('\033[1;31m 获得金币: {} Rank: {}\033[0m'.format(m['coin'], g_rank))

                print('\033[1;31m 游戏结束 \033[0m')
            return coins            
            

        # asyncio.get_event_loop().run_until_complete(chengyu())
        loop = asyncio.get_event_loop()
        tasks = chengyu()  
        coins = loop.run_until_complete(asyncio.gather(tasks))
        return coins[0]


def genUsers():
    yield QuXiaoChuUser(data_her)

g_rank = 15
chengyu = Chengyu()

if __name__ == "__main__":

    for user in genUsers():

        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 登录获取 token
        result = user.sessions_create_oauth2()

        for _ in range(10):   
            coins = chengyu_auto_answer(user)
            time.sleep(1)
            if coins == 10:
                break

        print('开始时间 ', start_time)
        print('结束时间 ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



        
