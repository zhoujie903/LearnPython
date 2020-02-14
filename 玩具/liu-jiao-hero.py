#!/usr/bin/env python3
# coding=utf-8

'''
# 六角英雄App / 泡泡消消消App
# 测试时间：2019-06-01
# App版本：1.0.0(9000)
# App地址：https://itunes.apple.com/cn/app/id1462036583
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

# 接口
# ------------------------------------------------
# 接口: 每小时签到
king_daily_sign = 'king/daily_sign'

# 接口: 收集签到的金币
king_daily_luckydraw = 'king/daily_luckydraw'

# 接口: 离线金币
coin_offline_check = 'king/offline_check'

# 接口: 大转盘Go并收集金币
coin_lucky_draw = 'coin/lucky_draw'

# 接口: 大转盘达到5、10、15、20次时收集金币
api_coin_lucky_extra = 'coin/lucky_draw_extra'
# ------------------------------------------------


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
UUID_zxg = '1457654'

UUID_848 = '848678'
UUID_887 = '887887'
UUID_her = '152000'

UUID_fb6 = '2096000'

# hexgon - 六角英雄 
# ------------------------------------------------
data_919 = {
    'channel': '90000',
    'code': '',
    'gtype': 'hexgon',
    'hash': '',
    'muid': '',
    'oatype': 'dev',
    'os': 'ios',    
}
# ------------------------------------------------

# gc - 泡泡消消消
# ------------------------------------------------
data_fb6 = {
    'channel': '000001338727',
    'code': '',
    'gtype': 'gc',
    'hash': '',
    'muid': '',
    'oatype': 'dev',
    'os': 'ios',    
    'deviceid': '',    
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

    def fetch_alipay_account(self):
        '''
        获取绑定的支付宝账号
        https://king.hddgood.com/king_api/v1/user/fetch_alipay_account
        未绑定：
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"real_name":null,"alipay_account":null,"binded":false}}
        绑定：
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"real_name":"xxx","alipay_account":"xxx@yyy.com","binded":true}}
        '''
        print("获取绑定的支付宝账号 {} ".format(self.uid))

        data = self._uid_data()

        api = self._genapi('user/fetch_alipay_account')
        self.session.options(api)
        result = self._post(api, data)
        return json.loads(result) 

    def zhifubao(self, amount, account, real_name):
        '''
        提取到支付宝
        '''
        # curl -H 'Host: mapi.hddgood.com' \
        # -H 'Origin: https://wisedom.hddgood.com' \
        # -H 'Accept-Language: zh-cn' -H 'Accept: application/json, text/plain, */*' \
        # -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hddwisedom/ios1.0.0' \
        # -H 'A-Token-Header: MjNXUFZQV0FHH0INWFcPcEtVAgc=' \
        # -H 'Referer: https://wisedom.hddgood.com/my/withdraw?money=10' \
        # --data "amount=10&account=13456789876&real_name=%E5%91%A8&uid=153233" \
        # --compressed 'https://mapi.hddgood.com/api/v1/king/withdraw'
        print("提取到支付宝 {} ".format(self.uid))

        data = self._uid_data()
        data['amount'] = amount
        data['account'] = account
        data['real_name'] = real_name

        api = self._genapi('king/withdraw')
        result = self._post(api, data)
        return json.loads(result)

    def offline(self):
        '''
        离线金币
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"coin":19,"time":4665}}
        '''
        print("离线金币 {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi(coin_offline_check)
        self.session.options(api)
        return self._post(api, data) 

    def userinfo(self):
        '''
        获取用户信息
        https://mapi.hddgood.com/api/v1/king/userinfo
        '''
        print("获取用户信息 {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi('king/userinfo')
        self.session.options(api)
        result = self._post(api, data)

        result = json.loads(result)
        coin = result['result']['coin']
        acc = result['result']['acc'] 
        nick = result['result']['nick'] 
        limited = '沉迷' if result['result']['coin_limited'] else '' 
        # print('金币数量：', result['result']['coin'])
        print('\033[1;31m{} - {} - 金币数量：{} - {}\033[0m'.format(acc, nick, coin, limited))

    def fetch_captcha(self, phone):
        '''
        获取验证码
        '''
        # https://king.hddgood.com/king_api/v1/user/captcha/fetch_captcha
        print("获取验证码 {}".format(phone))

        data = {
            'acc': phone
        }

        api = self._genapi('user/captcha/fetch_captcha')
        result = self._post(api, data)



    def lucky_draw_info(self):
        '''
        获取大转盘的次数情况信息
        coin/lucky_draw_info
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"times_left":0,"times_total":50,"extra":[1,1,1,1]}}
        '''
        print("获取大转盘的次数情况信息 {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi('coin/lucky_draw_info')
        self.session.options(api)
        return self._post(api, data)

    def king_daily_info(self):
        '''
        获取签到情况信息
        king/daily_info
        '''
        print("获取签到情况信息 {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi('king/daily_info')
        self.session.options(api)
        return self._post(api, data)

    def sign(self):
        '''
        每小时签到并收集金币
        '''
        print("sign {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi(king_daily_sign)
        self.session.options(api)
        self._post(api, data)

        print("收集签到的金币 {}".format(self.uid))

        api = self._genapi(king_daily_luckydraw)
        self.session.options(api)
        return self._post(api, data)



    def coin_lucky(self):
        '''
        大转盘Go并收集金币
        '''

        print("大转盘Go {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi(coin_lucky_draw)
        return self._post(api, data)

    def coin_lucky_extra(self, index):
        '''
        大转盘Go并收集金币
        '''

        print("大转盘Go {} 额外{}".format(self.uid, index))

        data = self._uid_data()
        data['index'] = index

        api = self._genapi(api_coin_lucky_extra)
        return self._post(api, data)

    def rob_history(self):
        '''
        世界抢夺被抢夺记录
        '''
        print("世界抢夺被抢夺记录 {}".format(self.uid))

        data = self._uid_data()
        data['ps'] = '100'
        data['pn'] = '1'

        # 获取抢夺信息
        api = self._genapi('king/rob/history')
        result = self._post(api, data)
        result = json.loads(result)
        return result

    def rob_rob(self, target_id, old_id=''):
        '''
        抢夺
        '''        
        print('抢夺对象 {}'.format(target_id))
        data = self._uid_data()
        data['target'] = target_id
        data['old_id'] = old_id
        data['result'] = 'true'
        api = self._genapi('king/rob/rob')
        self._post(api, data)

    def rob(self):
        '''
        世界抢夺
        '''
        print("世界抢夺 {}".format(self.uid))

        data = self._uid_data()

        # 获取抢夺信息
        api = self._genapi('king/rob/info')
        result = self._post(api, data)

        # 判断是否还有抢夺机会
        result = json.loads(result)
        times = result['result']['times_left']
        if times > 0:
            print('还有抢夺机会 {}次'.format(result['result']['times_left']))

            # 获取抢夺对象
            api = self._genapi('king/rob/fetch_target')
            result = self._post(api, data)

            result = json.loads(result)
            if result['success'] == False:
                return

            targets = []
            for person in result['result']:
                if person['result'] != 1 and int(person['balance']) > 150:
                    targets.append(person['uid'])

            print(targets)

            c = min(times, len(targets))
            for i in range(c):
                self.rob_rob(targets[i])


    def rest_super_brain(self):
        '''
        最强大脑
        '''
        print("最强大脑 {} ".format(self.uid))

        data = {}

        api = self._genapi("king/rest/game_report2?uid=" +
                           self.uid + r'&param={"type":"M","result":true}')
        return self._post(api, data)

    def rest_pingtu(self, gameid):
        '''
        六边形拼图
        /api/v1/king/rest/game_report2?uid=145696&param={"type":"H","mode":"endless","gameid":"H1367","data":"ST_Hex_Blocks_Puzzle_FFIGZ_ls_=0,ST_Hex_Blocks_Puzzle_FHPRG_RST_ls_=1559378352.566,ST_Hex_Blocks_Puzzle_FHPRG_ls_=0,ST_Hex_Blocks_Puzzle_HUSD_ls_=0,ST_Hex_Blocks_Puzzle_LC_ls_=1,ST_Hex_Blocks_Puzzle_NM_HNT_ls_=5,ST_Hex_Blocks_Puzzle_TDIFF_ls_=0,ST_Hex_Blocks_Puzzle_THUSD_ls_=0,ST_Hex_Blocks_Puzzle_TLE_ls_=2,ST_Hex_Blocks_Puzzle_TLH_ls_=1,ST_Hex_Blocks_Puzzle_TLM_ls_=1,ST_Hex_Blocks_Puzzle_aUorI_ls_=1,ST_Hex_Blocks_Puzzle_lang_ls_=1,ST_Hex_Blocks_Puzzle_music_is_on_ls_=1,ST_Hex_Blocks_Puzzle_sound_is_on_ls_=1"}
        '''
        print("六边形拼图 {} ".format(self.uid))

        data = {}

        b = "king/rest/game_report2?uid=" + self.uid
        c1 = r'&param={"type":"H","mode":"endless","gameid":'
        gid = r'"{}"'.format(gameid)
        c2 = r',"data":"ST_Hex_Blocks_Puzzle_FFIGZ_ls_=0,ST_Hex_Blocks_Puzzle_FHPRG_RST_ls_=1559378352.566,ST_Hex_Blocks_Puzzle_FHPRG_ls_=0,ST_Hex_Blocks_Puzzle_HUSD_ls_=0,ST_Hex_Blocks_Puzzle_LC_ls_=1,ST_Hex_Blocks_Puzzle_NM_HNT_ls_=5,ST_Hex_Blocks_Puzzle_TDIFF_ls_=0,ST_Hex_Blocks_Puzzle_THUSD_ls_=0,ST_Hex_Blocks_Puzzle_TLE_ls_=2,ST_Hex_Blocks_Puzzle_TLH_ls_=1,ST_Hex_Blocks_Puzzle_TLM_ls_=1,ST_Hex_Blocks_Puzzle_aUorI_ls_=1,ST_Hex_Blocks_Puzzle_lang_ls_=1,ST_Hex_Blocks_Puzzle_music_is_on_ls_=1,ST_Hex_Blocks_Puzzle_sound_is_on_ls_=1"}' 
        
        api = self._genapi(b + c1 + gid + c2)
        self.session.options(api)
        return self._post(api, data)

    def rest_xiaopaoer(self, level):
        '''
        小炮儿
        '''
        print("小炮儿 {} ".format(self.uid))

        data = {}

        api = self._genapi("king/rest/game_report2?uid=" + str(self.uid) +
                           r'&param={"type":"S","mode":"upgrade","level":' + str(level) + r',"score":200,"result":true}')

        return self._post(api, data)

    def rest_guodong(self, level):
        '''
        果冻
        '''
        # https://king.hddgood.com/king_api/v1/rest/game_report2?uid=453689&param={"type":"J","level":2,"score":7080,"result":true}

        print("果冻 {} ".format(self.uid))

        data = {}

        api = self._genapi("rest/game_report2?uid=" + self.uid +
                           r'&param={"type":"J","level":' + str(level) + r',"score":100000,"result":true}')

        return self._post(api, data)

    def rest_archery(self, level):
        # https://king.hddgood.com/king_api/v1/rest/game_report2?uid=472251&param={"type":"A","mode":"upgrade","level":2,"score":17,"result":true,"data":"1,4,10,4,15,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"}
        '''
        拇指射箭
        19965412404 done
        '''
        print("拇指射箭 - 共50关 {} ".format(self.uid))

        data = {}

        api = self._genapi("rest/game_report2?uid=" + self.uid +
                           r'&param={"type":"A","mode":"upgrade","level":' + str(level) + r',"score":17,"result":true' + r',"data":"1,4,10,4,15,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"}')

        return self._post(api, data)

    def rest_get_gameid(self, game_type):
        '''
        获取游戏ID - 消灭病毒/伪装者
        V:消灭病毒
        F:伪装者
        '''

        t = {
            'V':'消灭病毒',
            'F':'伪装者',
            'H':'六边形拼图',
        }
        print("获取游戏ID - {} - {}".format(t[game_type], self.uid))
        headers = self.headers
        start = int(time.time() * 1000)
        headers['Referer'] = 'https://king.hddgood.com/static/wzz/game.html?uid={}&token={}&hideAd=false&webPlugin=false&appchannel=&nick=%E4%B8%80%E5%90%BB%E6%B1%9F%E5%B1%B1&time={}'.format(self.uid, self.token_header, start)

        data = {}

        url = 'king/rest/start?uid={}&type={}'.format(self.uid, game_type)
        api = self._genapi(url)

        self.session.options(api)
        return self._post(api, data)

    def rest_win_game(self, gameid, score, query=''):
        '''
        得分
        '''
        print("得分 {} ".format(self.uid))

        data = {}

        a = '/king/rest/game_report?uid={}&gameid={}&score={}'.format(self.uid, gameid, score)
        url = a + query
        api = self._genapi(url)

        return self._post(api, data)

    def rest_board(self):
        '''
        排行榜
        '''
        day = time.strftime("%Y%m%d", time.localtime())
        data = {
            'uid': self.uid,
            'ps': '10',
            'pn': '1',
            'type': 'V',
            'dayid': day,
        }

        api = self._genapi('/king/rest/board')

        return self._post(api, data)

    def math_join_math(self):
        '''
        高斯速算 - 开题
        {"success":false,"msg":"操作失败","code":"365","codemsg":"异常用户不允许参与"}
        '''
        print("高斯速算 - 开题 - {} ".format(self.uid))
        headers = self.headers
        headers['Referer'] = 'https://wisedom.hddgood.com/math/speed'

        data = {
            'uid': self.uid
        }

        url = 'wisedom/math/join_math'
        api = self._genapi(url)

        self.session.options(api)
        result = self._post(api, data)
        return json.loads(result)

    def math_answer(self, mid, seq, answer):
        '''
        高斯速算 - 回答
        '''
        print("高斯速算 - 回答 - {} ".format(self.uid))
        headers = self.headers
        headers['Referer'] = 'https://wisedom.hddgood.com/math/speed'

        data = {
            'uid': self.uid,
            'mid': mid,
            'seq': seq,
            'answer': answer,
            # 'hash': '35bb56d304284c1333f4f33b1f2bc34e',
        }

        url = 'wisedom/math/answer'
        api = self._genapi(url)

        if seq == '1':
            self.session.options(api)
        result = self._post(api, data)
        return json.loads(result) 

    def fomo_daily_bonus(self):
        '''
        薛定谔的钥匙 - 是否今日投入最多
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"tool_key":false,"most_key":false,"keys":31}}
        '''
        print("薛定谔的钥匙 - 是否今日投入最多 - {} ".format(self.uid))
        headers = self.headers
        headers['Referer'] = 'https://wisedom.hddgood.com/math/fomo'

        data = {
            'uid': self.uid,
        }

        url = 'wisedom/fomo/daily_bonus'
        api = self._genapi(url)
        
        self.session.options(api)
        result = self._post(api, data)
        return json.loads(result)        

    def fomo_buy2(self):
        '''
        薛定谔的钥匙 - 买
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"succeed":true,"ad":true}}
        {"success":false,"msg":"操作失败","code":"324","codemsg":"余额不足"}
        '''
        print("薛定谔的钥匙 - 买 - {} ".format(self.uid))
        headers = self.headers
        headers['Referer'] = 'https://wisedom.hddgood.com/math/fomo'

        data = {
            'uid': self.uid,
            'fid': '176',
            'keys': '1',
            'bouns_balance': 'true',
            'hash': '0f9bf38323849c4124548dfbd0179b73',
            'tm': '1560657170192',
        }

        url = 'wisedom/fomo/buy2'
        api = self._genapi(url)
        
        self.session.options(api)
        result = self._post(api, data)
        return json.loads(result)       

    def _uid_data(self):
        return {'uid': self.uid}

    @staticmethod
    def _genapi(path):
        return 'https://mapi.hddgood.com/api/v1/' + path


    def _post(self, api, data, p=logging.warning):
        time.sleep(QuXiaoChuUser.SLEEP)

        res = self.session.post(api, data=data)
        print(res.url)
        result = res.text
        print(result)
        print('')
        return result

    @staticmethod
    def _need_sign(j):
        '''
        这个时段是否已签到过？
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"sign":"111111111111111111111000","luckydraw":"111111111111111111111000","hour_index":20}}
        '''

        import json
        d = json.loads(j)
        if d["code"] == "200":
            result = d["result"]

            sign = result["sign"]
            index = result["hour_index"]
            return sign[index] == '0'
        else:
            return True

    @staticmethod
    def _need_go(j):
        '''
        是否还有大转盘的抽奖机会？
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"times_left":0,"times_total":50,"extra":[1,1,1,1]}}
        '''

        import json
        d = json.loads(j)
        if d["code"] == "200":
            result = d["result"]

            total = result["times_total"]
            left = result["times_left"]
            extra = result["extra"]

            need = [i for i, v in enumerate(
                extra) if v != 1 and (total - left) > (i+1)*5]

            return (left != 0, need)
        else:
            return (True, [0, 1, 2, 3])


def rob_back(user: QuXiaoChuUser):
    '''
    世界抢夺-反击
    '''
    result = user.rob_history()
    for item in result['result']:
        print(item['robber'], item['id'])
        if item['strike_back'] == None:
            user.rob_rob(item['robber'], item['id'])

def hourly_sign(user: QuXiaoChuUser):
    # 签到
    result = user.king_daily_info()
    if user._need_sign(result):
        print('需要签到')
        user.sign()
    else:
        print('不需要签到')

def rank(user: QuXiaoChuUser):
    '''
    获取排名
    排行榜：https://king.hddgood.com/king_api/v1/rest/board
    '''
    users = [UUID_275, UUID_zxg]
    ranks = [0,1,2,3]
    count = len(users) 

    weekday = datetime.datetime.now().weekday()
    first =  weekday % count

    result = user.rest_board()
    result = json.loads(result)
    board = result['result']['list']

    for i, item in enumerate(board):
        print(i, ' - ', item['score'], ' - ', item['nick'])


    for i, r in enumerate(ranks):
        uid = users[(i + first)%count]
        if uid == user.uid and str(board[r]['uid']) != user.uid:
            score = board[r]['score'] 
            if i == 0:
                score += random.randint(1,4)
            print('用户 {} 以 {} 分争第{}名'.format(uid, score, r+1))
            mine_clearance(user,score)

def mine_clearance(user: QuXiaoChuUser, score=860):
    result = user.rest_get_gameid('V')
    result = json.loads(result)

    gameid = result['result']['gameid']
    print(gameid)
    time.sleep(7)

    seconds = random.randint(1, 30) 
    q = '&userScores=81&difSelected=3&currentLives=1&currentShots=2&minutes=1&seconds={}&kScores=2'.format(seconds)
    user.rest_win_game(gameid, score, q)

def disguiser(user: QuXiaoChuUser):
    result = user.rest_get_gameid('F')
    result = json.loads(result)

    gameid = result['result']['gameid']
    print(gameid)
    time.sleep(20)
    user.rest_win_game(gameid, 61)


def rest_pingtu(user: QuXiaoChuUser):
    result = user.rest_get_gameid('H')
    result = json.loads(result)

    gameid = result['result']['gameid']
    print(gameid)
    time.sleep(5)
    user.rest_pingtu(gameid)

def math_rank(user: QuXiaoChuUser):
    result = user.math_join_math()
    mid = result['mid']
    seq = str(result['seq'])
    question = result['question']
    answer = str(eval(question))
    user.math_answer(mid, seq, answer)

def fomo(user: QuXiaoChuUser):
    '''
    有50次观看视频得key的机会
    '''
    for _ in range(20):
        result = user.fomo_buy2()
        if result['code'] != '200':
            break
        time.sleep(28)

def rest_games(user: QuXiaoChuUser):
    # Todo:
    # 六边形拼图、我飞刀玩的賊溜


    # 最强大脑 - 共100关
    for i in range(1, 101):
        print('---', i)
        user.rest_super_brain()
        time.sleep(1.1)

    # 小炮儿大作战 - 共50关
    for level in range(1, 51):
        user.rest_xiaopaoer(level)
        time.sleep(1)

    # 拇指射箭 - 共50关
    for level in range(1, 51):
        user.rest_archery(level)
        time.sleep(1)

    # 果冻消消消 - 共150关
    for level in range(1, 151):
        user.rest_guodong(level)
        time.sleep(1)

def auto_fetch_money(user: QuXiaoChuUser):
    '''
    自动提现
    '''
    result = user.fetch_alipay_account()

    real_name = result['result']['real_name']
    alipay_account = result['result']['alipay_account']
    binded = result['result']['binded'] 

    if binded:
        result = user.zhifubao('10', alipay_account, real_name)
        if result['success']:
            print('\033[0;31m {} 提现成功 \033[0m'.format(alipay_account))

def genUsers():
    # yield QuXiaoChuUser(data_919)

    yield QuXiaoChuUser(data_fb6)


if __name__ == "__main__":

    # 趣消除2App自动签到
    for user in genUsers(): 
        print('\033[1;31m---------------------------\033[0m')
       
        user.sessions_create_oauth2() 

        # 离线金币      
        user.offline()

        # 签到
        hourly_sign(user)

        # 世界抢夺
        user.rob()
        rob_back(user)

        # 作战休息区
        rest_games(user)

        # fomo(user)
        # continue

        # auto_fetch_money(user)

        user.userinfo()

        
