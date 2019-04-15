#!/usr/bin/env python3
# coding=utf-8

'''
# 趣消除App的签到和大装盘地自动化；东方头条App的签到、金币成熟收集地自动化；
# 测试时间：2019-04-08
# App版本：1.1.2
# App地址：https://itunes.apple.com/cn/app/id1449545954
# App地址：https://itunes.apple.com/cn/app/id1030220577
'''

import requests
import re
import time
import json
import sys
print(sys.stdout.encoding)

# 解决编码问题
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


# 这些变量的值可以通过像Charles抓包软件获得
# 账号变量
# ------------------------------------------------
# 每个账号不同；同一个账号每次登录时也是不一样的
# 同一个账号，退出时，只要不登录，上次的A-Token-Header的值还有效，只有再登录时，上次的token值才失败
A_Token_Header_13456774460 = 'ICxfVVRRV0ZCH0IOWgNdIhpTVlM='
A_Token_Header_19965412404 = 'NDpMV1BQV0RLH0IOWVVaJk1TAlI='

# 这里的Cookie好像很奇怪
# CNZZDATA1276022107的值：同一个账号每次登录时，值不同；但好像也不影响接口请求的成功
# 同一个账号，退出或再登录，都不用修改，一直有效
Cookie_13456774460 = 'UM_distinctid=16947f46ccd79-0e531e04caae4e8-73275048-4a640-16947f46cce2e2; cn_1276022107_dplus=%7B%22distinct_id%22%3A%20%2216947f46ccd79-0e531e04caae4e8-73275048-4a640-16947f46cce2e2%22%2C%22sp%22%3A%20%7B%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221551686237%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24_sessionid%22%3A%20402%2C%22%24_sessionTime%22%3A%201554368804%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201554368804%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D; CNZZDATA1276022107=1035459509-1551686237-%7C1554367164; _ga=GA1.2.1747575593.1553400628'
Cookie_19965412404 = 'UM_distinctid=16947f46ccd79-0e531e04caae4e8-73275048-4a640-16947f46cce2e2; cn_1276022107_dplus=%7B%22distinct_id%22%3A%20%2216947f46ccd79-0e531e04caae4e8-73275048-4a640-16947f46cce2e2%22%2C%22sp%22%3A%20%7B%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221551686237%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24_sessionid%22%3A%20402%2C%22%24_sessionTime%22%3A%201554368804%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201554368804%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D; CNZZDATA1276022107=1035459509-1551686237-%7C1554367164; _ga=GA1.2.1747575593.1553400628'

UUID_13456774460 = '472251'
UUID_19965412404 = '633278'
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

class User:
    pass

class QuXiaoChuUser(User):
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

    SLEEP = 1

    def __init__(self, uid, token_header, cookie):
        self.uid = uid
        self.headers = dict(QuXiaoChuUser.headers)
        self.headers['A-Token-Header'] = token_header
        self.headers['Cookie'] = cookie


    def userinfo(self):
        '''
        获取用户信息
        https://king.hddgood.com/king_api/v1/king/userinfo
        ''' 

        print("获取大转盘的次数情况信息 {}".format(self.uid))

        data = self.data
        data['uid'] = self.uid

        api = self._genapi('king/userinfo')
        result = self._post(api, self.headers, data) 

        result = json.loads(result)
        print('金币数量：', result['result']['coin'])  


    def lucky_draw_info(self):
        '''
        获取大转盘的次数情况信息
        coin/lucky_draw_info
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
            targets = []
            for person in result['result']:
                if person['result'] != 1:
                    targets.append(person['uid']) 

            
            print(targets)

            c = min(times, len(targets))
            for i in range(c):
                # 抢夺
                print('抢夺对象 {}'.format(targets[i]))
                data = self._uid_data()
                data['target'] = targets[i]
                data['old_id'] = '' 
                data['result'] = 'true'
                api = self._genapi('rob/rob')
                self._post(api, self.headers, data)


    def super_brain(self):
        '''
        最强大脑
        '''
        # rest/game_report2?uid=633278&param=%7B%22type%22:%22M%22,%22result%22:true%7D
        # rest/game_report2?uid=633278&param={"type":"M","result":true}

        print("最强大脑 {} ".format(self.uid))

        data = {}

        api = self._genapi("rest/game_report2?uid=" + self.uid + r'&param={"type":"M","result":true}')
        return self._post(api, self.headers, data)


    def pingtu(self):
        '''
        六边形拼图
        '''

        print("六边形拼图 {} ".format(self.uid))

        data = {}

        gameid = {
            "472251":"H5579905",
            "633278":"H5584802",
        }

        api = self._genapi("rest/game_report2?uid=" + self.uid + r'&param={"type":"H","mode":"endless","gameid":"' + gameid[self.uid] + r'","data":"ST_Hex_Blocks_Puzzle_FFIGZ_ls_=0,ST_Hex_Blocks_Puzzle_FHPRG_RST_ls_=1555320439.099,ST_Hex_Blocks_Puzzle_FHPRG_ls_=0,ST_Hex_Blocks_Puzzle_HUSD_ls_=0,ST_Hex_Blocks_Puzzle_LC_ls_=5,ST_Hex_Blocks_Puzzle_NM_HNT_ls_=5,ST_Hex_Blocks_Puzzle_TDIFF_ls_=2,ST_Hex_Blocks_Puzzle_THUSD_ls_=0,ST_Hex_Blocks_Puzzle_TLE_ls_=6,ST_Hex_Blocks_Puzzle_TLH_ls_=1,ST_Hex_Blocks_Puzzle_TLM_ls_=2,ST_Hex_Blocks_Puzzle_aUorI_ls_=1,ST_Hex_Blocks_Puzzle_lang_ls_=1,ST_Hex_Blocks_Puzzle_music_is_on_ls_=1,ST_Hex_Blocks_Puzzle_sound_is_on_ls_=1"}')
        return self._post(api, self.headers, data)


    def _uid_data(self):
        return {'uid': self.uid}

    
    @staticmethod
    def _genapi(path):
        return 'https://king.hddgood.com/king_api/v1/' + path 

    @staticmethod
    def _post(api, headers, data):
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

            need = [i for i, v in enumerate(extra) if v != 1 and (total - left) > (i+1)*5]

            return (left != 0, need)
        else:
            return (True, [0, 1, 2, 3])


class DFTouTiaoUser(User):
    def sign(self):
        # 东方头条时段签到
        # 无参数
        # body[--data]有几个字段：
        # city=杭州市
        # cqid=AppStore
        # device=iPhone 6s Plus (A1634/A1687)
        # idfa=DBAEC254-D9C9-4CB7-BB49-E5B5FD4FB0A5
        # ime=F2B14555-E2EB-4556-B757-2C55799C92C2
        # it=d2RlWExGb015UjRqSkxMZk0rRkYwaW9sTFp3Y0VrMXhOcUtxZm9Ub0VId2NXS0NoZmpvZzRSeXdmWXZIVGs2TmZRb1pDRW1hUVlZWEhVQ1IrSldQdXc0V1JoWTlPU0hES2NKOTF1cjIzZlNHTndyNHp3WFhLeE5yUm1FTzhTdDA=
        # os=iOS
        # position=浙江
        # ver=2.4.5

        print("东方头条时段签到")

        headers = self._header()
        headers['Host'] = 'timesaward.dftoutiao.com'

        data = {
            'city': '杭州市',
            'cqid': 'AppStore',
            'device': 'iPhone 6s Plus (A1634/A1687)',
            'idfa': 'DBAEC254-D9C9-4CB7-BB49-E5B5FD4FB0A5',
            'ime': 'F2B14555-E2EB-4556-B757-2C55799C92C2',
            'lt': 'd2RlWExGb015UjRqSkxMZk0rRkYwaW9sTFp3Y0VrMXhOcUtxZm9Ub0VId2NXS0NoZmpvZzRSeXdmWXZIVGs2TmZRb1pDRW1hUVlZWEhVQ1IrSldQdXc0V1JoWTlPU0hES2NKOTF1cjIzZlNHTndyNHp3WFhLeE5yUm1FTzhTdDA%3D',
            'os': 'ios',
            'position': '浙江',
            'ver': '2.4.5',
        }

        api_timesaward = 'https://timesaward.dftoutiao.com/timesaward/timesaward/get_award'
        result = requests.post(api_timesaward, headers=headers, data=data).text
        print(result)


    def harvest_tree(self):
        # 东方头条时段签到
        # 无参数

        print("东方头条金币成熟")

        headers = self._header()
        headers['Host'] = 'tree.dftoutiao.com' 

        data = {
            'accid': '834536089',
            'appqid': 'AppStore190330',
            'apptypeid': 'DFTT',
            'appver': '2.4.5',
            'device': 'iPhone 6s Plus (A1634/A1687)',
            'deviceid': 'DBAEC254-D9C9-4CB7-BB49-E5B5FD4FB0A5',
            'ime': 'F2B14555-E2EB-4556-B757-2C55799C92C2',
            'network': 'wifi',
            'number': '2',
            'os': 'iOS12.1.4',
            'platform':	'2',
            'position': '浙江',
            'region':	"%E6%B5%99%E6%B1%9F",
            'sign':	'6bff6ce07b55fdc09c8be7b4c058d616',
            'softname':	'DFTTIOS',
            'softtype':	'TouTiao',
            'ts':	'1554591451',
            'ver': '2.4.5',
            'version':	'2.4.5'
        }

        api_timesaward = 'https://tree.dftoutiao.com/tree/money_tree_config/harvest_tree'
        result = requests.post(api_timesaward, headers=headers, data=data).text
        print(result)

    @staticmethod
    def _header():
        return {
            'Host': '',
            'Accept': '*/*',
            'User-Agent': 'DFTT/2.4.5 (iPhone; iOS 12.1.4; Scale/3.00)',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-CN;q=0.8'
        } 


def genUsers():
    yield QuXiaoChuUser(UUID_13456774460, A_Token_Header_13456774460, Cookie_13456774460)
    yield QuXiaoChuUser(UUID_19965412404, A_Token_Header_19965412404, Cookie_19965412404) 


if __name__ == "__main__":

    # 趣消除App自动签到和大转盘
    for user in genUsers():

        # 离线金币
        user.offline()

        user.super_brain()
        user.pingtu()

        # 签到
        result = user.king_daily_info()            
        if user._need_sign(result):
            print('需要签到')
            user.sign()
        else:
            print('不需要签到')
            

        # 大转盘
        result = user.lucky_draw_info()
        result = user._need_go(result)
        if result[0]:
            user.coin_lucky()
        else:
            print('没有转盘抽奖机会了')
            

        for index in result[1]:
            user.coin_lucky_extra(index)


        # 世界抢夺
        user.rob()


    # 东方头条App自动签到和金币成熟收集
    toutiao = DFTouTiaoUser()
    toutiao.sign()
    toutiao.harvest_tree()
