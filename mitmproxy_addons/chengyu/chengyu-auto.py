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
# 1.每个账号不同；
# 2.同一个账号每次登录时也是不一样的
# 3.同一个账号，退出时，只要不登录，上次的A-Token-Header的值还有效，只有再登录时，上次的token值才失败
A_Token_Header_zxg = 'PTtWUFdWUkBFHEVZCVcNdUtVWwdc'


# Cookie的一些结论：
# 1.同一个账号，退出或再登录，都不用修改，一直有效
# 2.值为空也可以
Cookie_zxg = ''

# UUID的一些结论：
# 1.固定不变
UUID_zxg = '1457362'
# ------------------------------------------------

api_ = 'https://king.hddgood.com/king_api/v1/'


class QuXiaoChuUser():
    headers = {
        'Host': 'king.hddgood.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'Origin': 'https://king.hddgood.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57/; quxiaochu/ios v1.1.2',
        'Referer': 'https://king.hddgood.com/'
    }

    data = {
        'uid': '',
        'channel': '',
        'version': '1.1.2',
        'os': 'ios',
        'web_ver': '20190261'
    }

    SLEEP = 0.5

    def __init__(self, uid, token_header, cookie):
        self.uid = uid
        self.headers = dict(QuXiaoChuUser.headers)
        self.headers['A-Token-Header'] = token_header
        self.token_header = token_header
        self.headers['Cookie'] = cookie

    def game_chengyu_join_game(self, rank):
        '''
        成语消消乐-获取游戏id
        https://king.hddgood.com/king_api/v1/game/join_game
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"gameid":"G15-3232777","dup":0,"starter":531492}}
        '''
        print("成语消消乐-获取游戏id {}".format(self.uid))

        data = self._uid_data()
        # 1:书童；2:儒生；15:殿阁大学士
        data['rank'] = str(rank) 
        data['type'] = 'G'

        api = self._genapi('game/join_game')
        result = self._post(api, self.headers, data) 
        return json.loads(result)       

    def _uid_data(self):
        return {'uid': self.uid}

    @staticmethod
    def _genapi(path):
        return 'https://king.hddgood.com/king_api/v1/' + path

    @staticmethod
    def _post(api, headers, data, p=logging.warning):
        time.sleep(QuXiaoChuUser.SLEEP)

        res = requests.post(api, headers=headers, data=data, verify=False)
        print(res.url)
        result = res.text
        print(result)
        print('')
        return result


class Chengyu(object):
    def __init__(self):
        path = pathlib.PurePath(__file__)
        path = path.parent.joinpath('chengyu.text')
        self.dictpath = str(path) 
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
        self.auto_send_answers = list()
        self.ack_true_answers = list()

        # 找到的的成语中各异字符为2个的答案数量：如 [真真假假] 
        self.answer_2chars_count = 0

        # {'中流砥柱':[1,9,21,25]}
        self.answer_indexs_dict = dict()

        # {'中流砥柱':set('中流砥柱')}
        self.answer_charset_dict = dict()

        # 查找到的错误答案
        self.error_answers = []

    # ---------------------------------------------
    def find_answers_v2(self, ask_string):
        '''
            在内存成语字典查找答案
        '''      
        ask_set = set(ask_string)        
        for i, c in enumerate(ask_string):
            self.char_indexs_dict.setdefault(c, []).append(i)
        self.index_char_dict = dict( zip(range(len(ask_string)), ask_string)) 

        max_count = (len(ask_string) / 4 ) * 1.5         
        for item in self.chengyu:
            item_set = self.answer_charset_dict.setdefault(item, set(item))
            if not (item_set - ask_set):
                self.answers.append(item)
                if len(item_set)<4:
                    self.answer_2chars_count += 1
                if len(self.answers) - self.answer_2chars_count >= max_count :
                    self.count = len(self.answers)
                    return
        self.count = len(self.answers)

    async def auto_answer(self, flow):
        if len(self.answers):
            item = self.answers[0]
            answer_index = []
            counter = collections.Counter(item)

            for char, count in counter.items():
                if self.char_indexs_dict[char]:
                    if len(self.char_indexs_dict[char]) < count:
                        self.error_answers.append(item)
                        self.answers.remove(item)
                        return
                else:
                    pass

            for c in item:
                if self.char_indexs_dict[c]:
                    index = self.char_indexs_dict[c][0]  
                    answer_index.append( str(index) )
                    del self.char_indexs_dict[c][0]
                else:
                    pass
              

            if len(set(answer_index)) < 4:
                print('算法有错误：{} 小于4'.format(answer_index))

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
            self.auto_send_answers.append(item)
            self.answers.remove(item)
            await flow.send(mm)
            # time.sleep(0.5)


    def add_new_worlds_to_memory(self, m):
        '''
            把答案增加到内存字典中
        '''
        if len(self.ack_true_answers) < len(m['all_answer']):
            for answer in m['all_answer']:
                self.chengyu.add(answer['phrase'])

        print('\033[1;31m 共收录{}个成语 \033[0m'.format(len(self.chengyu)))

    def add_new_worlds_to_file(self, m):
        '''
            把答案增加到文件中
        '''
        if len(self.ack_true_answers) < len(m['all_answer']):
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
        self.print_color('共找到 {}/{} 个成语'.format(self.count, len(self.ask_string)//4))
        self.print_color('错误成语 {}'.format(self.error_answers))
        self.print_color('共自动 {} 次提交：{}'.format(len(self.auto_send_answers),self.auto_send_answers))
        self.print_color('已确认 {} 个提交：{}'.format(len(self.ack_true_answers),self.ack_true_answers))
        self.print_color('问题 {}'.format(self.ask_string))
        for item in self.answers:
            self.print_color(item)
            # self.print_matrix(item)

        if (not self.answers) and self.index_char_dict:
            self.print_matrix()


    def print_matrix(self, item = []):
        chars_in_line = 6
        length = len(self.ask_string)        

        lines = (length + chars_in_line - 1) // chars_in_line
        PADDING = ' '*(lines * chars_in_line - length) 
        is_need_padding = len(PADDING) != 0

        self.print_color('--'*chars_in_line)

        global colors, White
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

            self.print_color(c, end=end, color=color)

        self.print_color('--'*chars_in_line)

    def print_color(self, message, end='\n', color=Red):
        print('{}{}\033[0m'.format(color, message), end=end)


    def reset_data_to_init(self):
        self.ask_string = ''
        self.answers.clear()
        self.index_char_dict.clear()

        self.count = 0        
        self.answer_2chars_count = 0

        self.answer_indexs_dict.clear()
        self.char_indexs_dict.clear()
        self.error_answers.clear()
        self.ack_true_answers.clear()
        self.auto_send_answers.clear()


def chengyu_auto_answer(user: QuXiaoChuUser):
    '''
    成语消消乐自动答题
    wss://king.hddgood.com/websock_m/websock_message?uid=472251&gameid=G15-3232777&token=JSdLVVRRV0ZCH0INUlYNchcDUlc=
    '''

    result = user.game_chengyu_join_game(g_rank)
    if result['success']:
        gameid = result['result']['gameid']
        url = 'wss://king.hddgood.com/websock_m/websock_message?uid={}&gameid={}&token={}'
        url = url.format(user.uid, gameid, user.token_header)
        print(url)

        import asyncio
        import websockets

        async def chengyu():
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

                    if message_type == 'answer':
                        chengyu.answer_indexs_dict[m['answer']] = m['answer_index']


                    # 删除已回答正确的答案
                    if m.get('ack') == 1:

                        answer = m['answer']
                        chengyu.ack_true_answers.append(answer)
                        answer_index = chengyu.answer_indexs_dict.get(answer,[])
                        for i in answer_index:
                            chengyu.index_char_dict[int(i)] = '  '
                        try:
                            chengyu.answers.remove(m['answer'])
                        except:
                            pass

                    # 自动答题
                    await chengyu.auto_answer(websocket)

                    # 显示答案
                    if len(chengyu.ask_string):
                        chengyu.print_answers()

                    
                    if message_type == 'game_result':
                        live = False
                        # 把答案增加到内存字典中
                        chengyu.add_new_worlds_to_memory(m)

                        chengyu.add_new_worlds_to_file(m) 

                        chengyu.reset_data_to_init()


                        # 其它解析
                        for item in m['scores']:
                            if str(item['uid']) == user.uid:
                                global g_rank
                                g_rank = item['rank'] 

                        print('\033[1;31m 获得金币: {} Rank: {}\033[0m'.format(m['coin'], g_rank))

                print('\033[1;31m 游戏结束 \033[0m')            

        asyncio.get_event_loop().run_until_complete(chengyu())


def genUsers():
    yield QuXiaoChuUser(UUID_zxg, A_Token_Header_zxg, Cookie_zxg)

g_rank = 15
chengyu = Chengyu()

if __name__ == "__main__":

    for user in genUsers():

        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for _ in range(20):   
            chengyu_auto_answer(user)
            time.sleep(1)
        print('开始时间 ', start_time)
        print('结束时间 ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



        
