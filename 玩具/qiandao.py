#!/usr/bin/env python3
# coding=utf-8

'''
# 趣消除App地自动化；
# 测试时间：2019-04-08
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

import requests

print(sys.stdout.encoding)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 解决编码问题
import codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


# 这些变量的值可以通过像Charles抓包软件获得
# 账号变量
# ------------------------------------------------
# A_Token_Header的一些结论：
# 1.每个账号不同；
# 2.同一个账号每次登录时也是不一样的
# 3.同一个账号，退出时，只要不登录，上次的A-Token-Header的值还有效，只有再登录时，上次的token值才失败
A_Token_Header_13400004460 = 'MCBKVVRRV0ZCH0INXVdaIRZSVFM='
A_Token_Header_19965412404 = 'JS9bV1BQV0RLH0INWFUNIUgFVwc='
A_Token_Header_17157725704 = 'JiZAVVZQU0tKH0INWlBdck1UBlA='
A_Token_Header_zxg = 'PTtWUFdWUkBFHEVZCVcNdUtVWwdc'


# Cookie的一些结论：
# 1.同一个账号，退出或再登录，都不用修改，一直有效
# 2.值为空也可以
# CNZZDATA1276022107的值：同一个账号每次登录时，值不同；但好像也不影响接口请求的成功
Cookie_13400004460 = 'UM_distinctid=16947f46ccd79-0e531e04caae4e8-73275048-4a640-16947f46cce2e2; cn_1276022107_dplus=%7B%22distinct_id%22%3A%20%2216947f46ccd79-0e531e04caae4e8-73275048-4a640-16947f46cce2e2%22%2C%22sp%22%3A%20%7B%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221551686237%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24_sessionid%22%3A%20402%2C%22%24_sessionTime%22%3A%201554368804%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201554368804%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D; CNZZDATA1276022107=1035459509-1551686237-%7C1554367164; _ga=GA1.2.1747575593.1553400628'
Cookie_19965412404 = 'UM_distinctid=16a10c4e1e8f2-0c66e08b0b85348-7229504a-4a640-16a10c4e1ebee; cn_1276022107_dplus=%7B%22distinct_id%22%3A%20%2216a10c4e1e8f2-0c66e08b0b85348-7229504a-4a640-16a10c4e1ebee%22%2C%22%24_sessionid%22%3A%20121%2C%22%24_sessionTime%22%3A%201555477452%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201555477452%2C%22initial_view_time%22%3A%20%221555058837%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D; CNZZDATA1276022107=808150895-1555058837-%7C1555475042; _ga=GA1.2.1602188260.1555309467; _gid=GA1.2.58736974.1555309467'
Cookie_17157725704 = 'UM_distinctid=16a10c4e1e8f2-0c66e08b0b85348-7229504a-4a640-16a10c4e1ebee; cn_1276022107_dplus=%7B%22distinct_id%22%3A%20%2216a10c4e1e8f2-0c66e08b0b85348-7229504a-4a640-16a10c4e1ebee%22%2C%22%24_sessionid%22%3A%20667%2C%22%24_sessionTime%22%3A%201557585874%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201557585874%2C%22initial_view_time%22%3A%20%221555058837%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D; CNZZDATA1276022107=808150895-1555058837-%7C1557583689; _ga=GA1.2.1602188260.1555309467; _gid=GA1.2.1233231256.1557556594'
Cookie_zxg = ''

# UUID的一些结论：
# 1.固定不变
UUID_13400004460 = '472251'
UUID_19965412404 = '633278' # https://www.pdflibr.com/SMSContent/1
UUID_17157725704 = '453689' # https://www.pdflibr.com/SMSContent/21
UUID_zxg = '1457362'
# ------------------------------------------------


# 接口
# ------------------------------------------------
api_ = 'https://king.hddgood.com/king_api/v1/'
# 接口: 每小时签到
king_daily_sign = 'king/daily_sign'

# 接口: 收集签到的金币
king_daily_luckydraw = 'king/daily_luckydraw'

# 接口: 离线金币
coin_offline_check = 'coin/offline_check'

# 接口: 大转盘Go并收集金币
coin_lucky_draw = 'coin/lucky_draw'

# 接口: 大转盘达到5、10、15、20次时收集金币
api_coin_lucky_extra = 'coin/lucky_draw_extra'
# ------------------------------------------------


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

    
    def zhifubao(self):
        '''
        提现到支付宝
        https://king.hddgood.com/king_api/v1/user/fetch_alipay_account
        {"success":false,"msg":"操作失败","code":"327","codemsg":"余额不足"}
        {"success":false,"msg":"操作失败","code":"380","codemsg":"该帐号已被其他用户使用"}
        '''
        print("提取到支付宝 {} ".format(self.uid))

        data = self._uid_data()
        data['amount'] = '10'
        data['account'] = '13400004460'
        data['real_name'] = 'xxx'

        api = self._genapi('king/withdraw')
        return self._post(api, self.headers, data)


    def fetch_captcha(self, phone):
        '''
        获取验证码
        https://king.hddgood.com/king_api/v1/user/captcha/fetch_captcha
        '''
        print("获取验证码 {}".format(phone))

        data = {
            'acc': phone
        }

        api = self._genapi('user/captcha/fetch_captcha')
        result = self._post(api, self.headers, data)


    def userinfo(self):
        '''
        获取用户信息
        https://king.hddgood.com/king_api/v1/king/userinfo
        '''
        print("获取用户信息 {}".format(self.uid))

        data = self.data
        data['uid'] = self.uid

        api = self._genapi('king/userinfo')
        result = self._post(api, self.headers, data)

        result = json.loads(result)
        coin = result['result']['coin']
        acc = result['result']['acc'] 
        nick = result['result']['nick']  
        print('{} - {} - 金币数量：{}'.format(acc, nick, coin))


    def lucky_draw_info(self):
        '''
        获取大转盘的次数情况信息
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"times_left":0,"times_total":50,"extra":[1,1,1,1]}}
        '''
        print("获取大转盘的次数情况信息 {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi('coin/lucky_draw_info')
        return self._post(api, self.headers, data)


    def king_daily_info(self):
        '''
        获取签到情况信息
        king/daily_info
        '''
        print("获取签到情况信息 {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi('king/daily_info')
        return self._post(api, self.headers, data)


    def sign(self):
        '''
        每小时签到并收集金币
        '''
        print("sign {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi(king_daily_sign)
        self._post(api, self.headers, data)

        print("收集签到的金币 {}".format(self.uid))

        api = self._genapi(king_daily_luckydraw)
        return self._post(api, self.headers, data)


    def offline(self):
        '''
        离线金币
        {"success":true,"msg":"操作成功","code":"200","codemsg":"操作成功","result":{"coin":19,"time":4665}}
        '''
        print("离线金币 {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi(coin_offline_check)
        return self._post(api, self.headers, data)


    def coin_lucky(self):
        '''
        大转盘Go并收集金币
        '''
        print("大转盘Go {}".format(self.uid))

        data = self._uid_data()

        api = self._genapi(coin_lucky_draw)
        return self._post(api, self.headers, data)


    def coin_lucky_extra(self, index):
        '''
        大转盘Go并收集金币
        '''
        print("大转盘Go {} 额外{}".format(self.uid, index))

        data = self._uid_data()
        data['index'] = index

        api = self._genapi(api_coin_lucky_extra)
        return self._post(api, self.headers, data)
        

    def rob_history(self):
        '''
        世界抢夺被抢夺记录
        '''
        print("世界抢夺被抢夺记录 {}".format(self.uid))

        data = self._uid_data()
        data['ps'] = '100'
        data['pn'] = '1'

        # 获取抢夺信息
        api = self._genapi('rob/history')
        result = self._post(api, self.headers, data)
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

        api = self._genapi('rob/rob')
        self._post(api, self.headers, data)


    def rob(self):
        '''
        世界抢夺
        '''
        print("世界抢夺 {}".format(self.uid))

        data = self._uid_data()

        # 获取抢夺信息
        api = self._genapi('rob/info')
        result = self._post(api, self.headers, data)

        # 判断是否还有抢夺机会
        result = json.loads(result)
        times = result['result']['times_left']
        if times > 0:
            print('还有抢夺机会 {}次'.format(result['result']['times_left']))

            # 获取抢夺对象
            api = self._genapi('rob/fetch_target')
            result = self._post(api, self.headers, data)

            result = json.loads(result)
            if result['success'] == False:
                return

            targets = []
            for person in result['result']:
                if person['result'] != 1 and person['balance'] > 150:
                    targets.append(person['uid'])

            print(targets)

            c = min(times, len(targets))
            for i in range(c):
                self.rob_rob(targets[i])


    def rest_super_brain(self):
        '''
        最强大脑 - 共100关
        rest/game_report2?uid=633278&param={"type":"M","result":true}
        '''
        print("最强大脑 - 共100关 {} ".format(self.uid))

        data = {}

        api = self._genapi("rest/game_report2?uid=" +
                           self.uid + r'&param={"type":"M","result":true}')
        return self._post(api, self.headers, data)


    def rest_pingtu(self):
        '''
        六边形拼图
        '''
        print("六边形拼图 {} ".format(self.uid))

        data = {}

        # 每个用户的gameid都不同
        gameid = {
            "472251": "H5579905",
            "633278": "H5584802",
            "453689": "H6273236",
        }

        api = self._genapi("rest/game_report2?uid=" + self.uid + r'&param={"type":"H","mode":"endless","gameid":"' +
                           gameid[self.uid] + r'","data":"ST_Hex_Blocks_Puzzle_FFIGZ_ls_=0,ST_Hex_Blocks_Puzzle_FHPRG_RST_ls_=1555320439.099,ST_Hex_Blocks_Puzzle_FHPRG_ls_=0,ST_Hex_Blocks_Puzzle_HUSD_ls_=0,ST_Hex_Blocks_Puzzle_LC_ls_=5,ST_Hex_Blocks_Puzzle_NM_HNT_ls_=5,ST_Hex_Blocks_Puzzle_TDIFF_ls_=2,ST_Hex_Blocks_Puzzle_THUSD_ls_=0,ST_Hex_Blocks_Puzzle_TLE_ls_=6,ST_Hex_Blocks_Puzzle_TLH_ls_=1,ST_Hex_Blocks_Puzzle_TLM_ls_=2,ST_Hex_Blocks_Puzzle_aUorI_ls_=1,ST_Hex_Blocks_Puzzle_lang_ls_=1,ST_Hex_Blocks_Puzzle_music_is_on_ls_=1,ST_Hex_Blocks_Puzzle_sound_is_on_ls_=1"}')
        return self._post(api, self.headers, data)


    def rest_xiaopaoer(self, level):
        '''
        小炮儿大作战 - 共50关
        # https://king.hddgood.com/king_api/v1/rest/game_report2?uid=633278&param={"type":"S","mode":"upgrade","level":13,"score":1984,"result":true}
        '''
        print("小炮儿大作战 - 共50关 {} ".format(self.uid))

        data = {}

        api = self._genapi("rest/game_report2?uid=" + self.uid +
                           r'&param={"type":"S","mode":"upgrade","level":' + str(level) + r',"score":4000,"result":true}')

        return self._post(api, self.headers, data)


    def rest_guodong(self, level):
        '''
        果冻消消消
        # https://king.hddgood.com/king_api/v1/rest/game_report2?uid=453689&param={"type":"J","level":2,"score":7080,"result":true}
        '''
        print("果冻消消消 - 共150关 {} ".format(self.uid))

        data = {}

        api = self._genapi("rest/game_report2?uid=" + self.uid +
                           r'&param={"type":"J","level":' + str(level) + r',"score":100000,"result":true}')

        return self._post(api, self.headers, data)


    def rest_archery(self, level):
        '''
        拇指射箭
        # https://king.hddgood.com/king_api/v1/rest/game_report2?uid=472251&param={"type":"A","mode":"upgrade","level":2,"score":17,"result":true,"data":"1,4,10,4,15,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"}
        19965412404 done
        17157725704 done
        zxg done
        '''
        print("拇指射箭 - 共50关 {} ".format(self.uid))

        data = {}

        api = self._genapi("rest/game_report2?uid=" + self.uid +
                           r'&param={"type":"A","mode":"upgrade","level":' + str(level) + r',"score":17,"result":true' + r',"data":"1,4,10,4,15,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"}')

        return self._post(api, self.headers, data)
      

    def _uid_data(self):
        return {'uid': self.uid}

    @staticmethod
    def _genapi(path):
        return 'https://king.hddgood.com/king_api/v1/' + path

    @staticmethod
    def _post(api, headers, data, p=logging.warning):
        time.sleep(QuXiaoChuUser.SLEEP)
        res = requests.post(api, headers=headers, data=data)
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


def is_phone_ok():
    '''
    趣消除App以前可以手机号登录，现在不再手机号注册登录了
    用来自动测试网上公开的手机号是否可以已注册趣消除App
    '''
    fake = QuXiaoChuUser(UUID_17157725704, A_Token_Header_17157725704, Cookie_17157725704)
    with open('/Users/zhoujie/Desktop/phone.text') as f:
        for line in f:        
            if len(line) == 12:
                fake.fetch_captcha(line)
                time.sleep(3)

def hourly_sign(user: QuXiaoChuUser):
    '''
    每小时签到
    '''
    result = user.king_daily_info()
    if user._need_sign(result):
        print('需要签到')
        user.sign()
    else:
        print('不需要签到')


def lucky(user: QuXiaoChuUser):
    '''
    大转盘
    '''
    result = user.lucky_draw_info()
    result = user._need_go(result)
    if result[0]:
        user.coin_lucky()
    else:
        print('没有转盘抽奖机会了')

    for index in result[1]:
        user.coin_lucky_extra(index) 

def rest_games(user: QuXiaoChuUser):
    pass
    return
    # Todo:
    # 六边形拼图、我飞刀玩的賊溜


    # 最强大脑 - 共100关
    for i in range(1, 101):
        print('---', i)
        user.rest_super_brain()

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
    pass

def genUsers():
    yield QuXiaoChuUser(UUID_13400004460, A_Token_Header_13400004460, Cookie_13400004460)
    yield QuXiaoChuUser(UUID_19965412404, A_Token_Header_19965412404, Cookie_19965412404)
    yield QuXiaoChuUser(UUID_17157725704, A_Token_Header_17157725704, Cookie_17157725704)
    yield QuXiaoChuUser(UUID_zxg, A_Token_Header_zxg, Cookie_zxg)


if __name__ == "__main__":

    # 趣消除App自动签到和大转盘
    for user in genUsers():
        print('\033[1;31m---------------------------\033[0m')
        # 离线金币    
        user.offline()

        # 签到
        hourly_sign(user)

        # 大转盘
        lucky(user)

        # 世界抢夺
        user.rob()

        # 世界抢夺-反击
        rob_back(user)

        # 作战休息区
        rest_games(user)

        # 自动取现到已绑定的支付宝账号
        auto_fetch_money(user)

        
