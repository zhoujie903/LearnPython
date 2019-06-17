#!/usr/bin/env python3
# coding=utf-8

'''
# 今日头条极速版App地自动化；
# 测试时间：2019-05-08
# App地址：https://itunes.apple.com/cn/app/id1410120498
'''

import requests
import re
import time
import json
import sys
import logging

logging.basicConfig(format='%(message)s')

print(sys.stdout.encoding)

# ToDo
# * [ ] 输出显示账号




# headers待研究
# Host	is.snssdk.com
# tt-request-time	1557820167455
# X-SS-STUB	22E67CC3AE278CB47BCA0058382D3330
# X-Khronos	1557820167
# X-Pods
# X-Gorgon	830000000000e3ad942491c627ace9a3ea0a85d18bc9f7a61890

# 用户变量
#
'''
headers['X-SS-Cookie']、headers['Cookie'] 这2个值相同:
134账号：
    UM_distinctid=16aa95d0306637-04af03430e1256-624c1540-4a640-16aa95d0307768; 
    CNZZDATA1264561316=1124511948-1557523913-%7C1557725024;  
    install_id=71980003246; 
    ttreq=1$f240c437305183835b3ad155dbef90f4332ffe03; 
    odin_tt=790d74b6df6b9fc63bab7e7e9999d3c00635bfbc7a03f99ddb431ce513bde6400590ba32c982b577943ead724d1c5106; 
    sid_guard=71d8b9612f76d55adffb263ce5ad2546%7C1557819990%7C5184000%7CSat%2C+13-Jul-2019+07%3A46%3A30+GMT; 
    uid_tt=6b020a09aa2c6f416cf86bf425253adf; 
    sid_tt=71d8b9612f76d55adffb263ce5ad2546; 
    sessionid=71d8b9612f76d55adffb263ce5ad2546;
    SLARDAR_WEB_ID=bb965c9e-9094-4fde-8b35-fe35220aae65;
'''

'''
UM_distinctid, CNZZDATA1264561316, install_id, ttreq, SLARDAR_WEB_ID: 同一手机上不同账号的值相同
odin_tt, sessionid, sid_guard, sid_tt, uid_tt：不同账号不相同
sessionid == sid_tt
sid_guard=71e52b49cde9b2717df1461469904bab%7C1557856571%7C5184000%7CSat%2C+13-Jul-2019+17%3A56%3A11+GMT
sid_guard=sessionid|1557856571|5184000|Sat,+13-Jul-2019+17:56:11+GMT
%7C=|
%3A=:
%2C=,
5184000 = 60 * 60 * 24 * 60 = 60天 sessionid有效时长
'''

'''
结论：
1. 退出登入后，cookie就失效了
2. xss_cookie，Cookie这2个字段，只要Cookie字段设置正确就可以了
'''
u134_xss_cookie='odin_tt=c9b152c7105c9b68dc486c593691d637190dd0d3452c5a2c35d927ed511239a5618ccb3dd5888bed019bb986fa228578; sessionid=736945d57d224c7ef21f2da8fc2058a9; sid_guard=736945d57d224c7ef21f2da8fc2058a9%7C1559318410%7C5184000%7CTue%2C+30-Jul-2019+16%3A00%3A10+GMT; sid_tt=736945d57d224c7ef21f2da8fc2058a9; uid_tt=49cab3713e8f97b5c39d583ed315b1f3; install_id=71980003246; ttreq=1$f240c437305183835b3ad155dbef90f4332ffe03; SLARDAR_WEB_ID=bb965c9e-9094-4fde-8b35-fe35220aae65; CNZZDATA1264561316=1124511948-1557523913-%7C1557725024; UM_distinctid=16aa95d0306637-04af03430e1256-624c1540-4a640-16aa95d0307768'
u134_Cookie='UM_distinctid=16aa95d0306637-04af03430e1256-624c1540-4a640-16aa95d0307768; CNZZDATA1264561316=1124511948-1557523913-%7C1557725024; SLARDAR_WEB_ID=bb965c9e-9094-4fde-8b35-fe35220aae65; install_id=71980003246; ttreq=1$f240c437305183835b3ad155dbef90f4332ffe03; odin_tt=c9b152c7105c9b68dc486c593691d637190dd0d3452c5a2c35d927ed511239a5618ccb3dd5888bed019bb986fa228578; sid_guard=736945d57d224c7ef21f2da8fc2058a9%7C1559318410%7C5184000%7CTue%2C+30-Jul-2019+16%3A00%3A10+GMT; uid_tt=49cab3713e8f97b5c39d583ed315b1f3; sid_tt=736945d57d224c7ef21f2da8fc2058a9; sessionid=736945d57d224c7ef21f2da8fc2058a9'


u165_xss_cookie='install_id=71980003246; ttreq=1$f240c437305183835b3ad155dbef90f4332ffe03; odin_tt=af797d4e0114caea449c831e9b19e7931c7608341b5a94819ff80cdcde65bebe25041dc6e9932fcf9af375bcde2c8da0f457f551c97b4a3627378a69e25c2936; sessionid=57bcc38e94a4b672aea311efe463167f; sid_guard=57bcc38e94a4b672aea311efe463167f%7C1559053779%7C5184000%7CSat%2C+27-Jul-2019+14%3A29%3A39+GMT; sid_tt=57bcc38e94a4b672aea311efe463167f; uid_tt=991da58fd71adbef2ed26a22dfb7b893; SLARDAR_WEB_ID=bb965c9e-9094-4fde-8b35-fe35220aae65; CNZZDATA1264561316=1124511948-1557523913-%7C1557725024; UM_distinctid=16aa95d0306637-04af03430e1256-624c1540-4a640-16aa95d0307768'
u165_Cookie='UM_distinctid=16aa95d0306637-04af03430e1256-624c1540-4a640-16aa95d0307768; CNZZDATA1264561316=1124511948-1557523913-%7C1557725024; SLARDAR_WEB_ID=bb965c9e-9094-4fde-8b35-fe35220aae65; uid_tt=991da58fd71adbef2ed26a22dfb7b893; sid_guard=57bcc38e94a4b672aea311efe463167f%7C1559053779%7C5184000%7CSat%2C+27-Jul-2019+14%3A29%3A39+GMT; sid_tt=57bcc38e94a4b672aea311efe463167f; odin_tt=af797d4e0114caea449c831e9b19e7931c7608341b5a94819ff80cdcde65bebe25041dc6e9932fcf9af375bcde2c8da0f457f551c97b4a3627378a69e25c2936; sessionid=57bcc38e94a4b672aea311efe463167f; install_id=71980003246; ttreq=1$f240c437305183835b3ad155dbef90f4332ffe03'


u152_xss_cookie=''
u152_Cookie='odin_tt=0e2070eff1aed467ad35db79123e0db0864de40792596b684643a0e490fc2e76dc0815f11d1c7f881a67d7589bab4de6; sid_guard=6a9181e7d1fa588d6521c0531a01f62f%7C1558914676%7C5184000%7CThu%2C+25-Jul-2019+23%3A51%3A16+GMT; uid_tt=c48c52bf604943764a01a109a75ee8d1; sid_tt=6a9181e7d1fa588d6521c0531a01f62f; sessionid=6a9181e7d1fa588d6521c0531a01f62f; UM_distinctid=16b2f22c27c1c-0834c5417cbfd-28480850-38400-16b2f22c27d5d; tt_diamond_env=prod; SLARDAR_WEB_ID=c21b6e31-eb3e-4e3f-ac43-275742149826; install_id=75249396282; ttreq=1$038b06c2dbda4627d889ddf10d6d27479d10da30; qh[360]=1'

# 重要
# aid:app_id
q_aid = 'aid=35'

# 其它
q_fp = 'fp=JlTrL2x1FWFuFlcbPrU1F2FePlcb'
q_version_code = 'version_code=6.7.5'
# vid:vendor_id,idfv
q_vid = 'vid=A9EA23F1-848B-4730-A847-89B988EB7A3B'
q_openudid = 'openudid=503c73bce41529a8e28bb7fe9f98f7fbc37fd45c'
# iid:install_id
q_iid = 'iid=71980003246'
q_device_id = '35038288092'

query_dict = {
    'fp': q_fp,
    'aid': q_aid,
    'vid': q_vid,
    'openudid': q_openudid,
    'iid': q_iid,
    'version_code': q_version_code,
}


class TouTiaoSpeedUser():
    def __init__(self, xss_cookie, cookie):
        self.xxs_cookie = xss_cookie
        self.cookie = cookie

    @staticmethod
    def _header():
        return {
            'Host': 'is.snssdk.com',
            'Accept': 'application/json',
            'User-Agent': 'NewsLite 6.7.5 rv:6.7.5.3 (iPhone; iOS 12.3; zh_CN)',
        }

    @staticmethod
    def _post(api, headers, data, p=logging.warning):
        # time.sleep(QuXiaoChuUser.SLEEP)
        res = requests.post(api, headers=headers, data=data)
        result = res.text
        p(res.json())
        print('')
        return result

    @staticmethod
    def _get(api, headers):
        # time.sleep(QuXiaoChuUser.SLEEP)
        res = requests.get(api, headers=headers)
        result = res.text
        print(json.loads(result))
        print('')
        return result

    def print_log(self, msg):
            print(self,msg)
            def decorator(func):
                def wapper(*args, **kwargs):
                    return func(*args, **kwargs)
                return wapper
            return decorator


    def open_treasure_box(self):
        '''
        开宝箱
        {'err_no': 5, 'err_tips': '请求参数中需要携带aid'}
        '''
        print("头条-开宝箱")
        headers = self._header()
        headers['X-SS-Cookie'] = self.xxs_cookie
        headers['Cookie'] = self.cookie

        # 不是必要的headers
        t = time.time()
        headers['tt-request-time'] = str(int(t * 1000))
        headers['X-Khronos'] = str(int(t))
        headers['X-Pods'] = ''

        data = {
        }

        url = 'http://is.snssdk.com/score_task/v1/task/open_treasure_box/?'
        query = '&_request_from=web&{fp}&{version_code}&app_name=news_article_lite&{vid}&device_id=35038288092&channel=App%20Store&resolution=1242*2208&{aid}&ab_version=472113,374098,758003,770507,887347,644001,661931,785656,800193,668907,808414,821460,772542,844798,846821,861726,668904,668906,877353,812272,865204,770317,668903,679106,763639,775316,770573,668905,851392&ab_feature=201616,z1&review_flag=0&ab_group=201616&update_version_code=6753&{openudid}&pos=5pe9vb%252F%252B9Onkv72nvb97ADB4KgO%252FsZe9vb%252Fx8vP69Ono%252Bfi%252Fvae9rK%252Bts62krKyvrq%252BvqKWrqKSqsZe9vb%252Fx%252FOn06ej5%252BL%252B9p72urbOvqqSpq6qvpaqqqKSkqqyX4A%253D%253D&idfv=A9EA23F1-848B-4730-A847-89B988EB7A3B&ac=WIFI&os_version=12.2&ssmix=a&device_platform=iphone&iid=71980003246&ab_client=a1,f2,f7,e1&device_type=iPhone%206S%20Plus&idfa=00000000-0000-0000-0000-000000000000'
        query = query.format(**query_dict)
        api = url + query
        result = self._post(api, headers=headers, data=data)


    def feed(self):
        print("头条-feed")

        headers = self._header()
        headers['X-SS-Cookie'] = self.xxs_cookie
        headers['Cookie'] = self.cookie

        data = {
        }

        url = 'https://iu.snssdk.com/api/news/feed/v64/?'
        query = '{fp}&{version_code}&app_name=news_article_lite&{vid}&device_id=35038288092&channel=App%20Store&resolution=1242*2208&{aid}&ab_version=472113,374098,758003,770507,887347,644001,661931,785656,800193,668907,808414,821460,772542,844798,846821,861726,668904,668906,877353,812272,865204,770317,668903,679106,763639,775316,770573,668905,851392&ab_feature=201616,z1&review_flag=0&ab_group=201616&update_version_code=6753&{openudid}&pos=5pe9vb%252F%252B9Onkv72nvb97ADB4KgO%252FsZe9vb%252Fx8vP69Ono%252Bfi%252Fvae9rK%252Bts62krKqsqa%252Bupa2pqKmlsZe9vb%252Fx%252FOn06ej5%252BL%252B9p72urbOvpa2kr6yupa%252BopK2tqKWX4A%253D%253D&idfv=A9EA23F1-848B-4730-A847-89B988EB7A3B&ac=WIFI&os_version=12.2&ssmix=a&device_platform=iphone&iid=71980003246&ab_client=a1,f2,f7,e1&device_type=iPhone%206S%20Plus&idfa=00000000-0000-0000-0000-000000000000&detail=1&category=video&last_refresh_sub_entrance_interval=1729&list_entrance=main_tab&tt_from=tab&count=20&loc_mode=1&LBS_status=authroize&cp=54C6DbA57d919q1&min_behot_time=1557819990&image=1&strict=0&language=zh-Hans-CN&refer=1'
        query = query.format(**query_dict)
        api = url + query
        result = self._post(api, headers=headers, data=data, p=logging.debug)
        result = json.loads(result)

        ids = []
        for item in result['data']:
            d = json.loads(item['content'])            
            ids.append(d.get('group_id'))

        return ids

    def get_read_bonus(self, group_id, is_push=True):
        '''
        推送：{'err_no': 0, 'data': {'content': '奖励认真阅读的你', 'score_amount': 100}, 'err_tips': 'success'}
        "err_no": 1028 "这篇文章已经阅读过了哦"
        普通：{'err_no': 0, 'data': {'content': '奖励认真阅读的你', 'score_amount': 100, 'have_score_amount': 100, 'score_limit': 1000}, 'err_tips': 'success'}

        {'err_no': 1, 'err_tips': '请登录后再开始任务'}
        推送/普通：{'err_no': 4, 'data': {'content': '奖励认真阅读的你', 'score_amount': 0}, 'err_tips': '已经到达任务限制次数'}
        '''
        print("头条-阅读文章-奖励")

        headers = self._header()
        headers['X-SS-Cookie'] = self.xxs_cookie
        headers['Cookie'] = self.cookie

        data = {
        }

        push = 'push' if is_push else ''
        item = 'group_id={}&impression_type={}&'.format(group_id, push)
        url = 'https://is.snssdk.com/score_task/v1/task/get_read_bonus/?'
        query = item + '{fp}&{version_code}&app_name=news_article_lite&vid=A9EA23F1-848B-4730-A847-89B988EB7A3B&device_id=35038288092&channel=App%20Store&resolution=1242*2208&aid=35&ab_version=472113%2C374098%2C758003%2C770507%2C887347%2C644001%2C661931%2C785656%2C800193%2C668907%2C808414%2C821460%2C772542%2C844798%2C846821%2C861726%2C668904%2C668906%2C877353%2C812272%2C865204%2C770317%2C668903%2C679106%2C763639%2C775316%2C770573%2C668905%2C851392&ab_feature=201616%2Cz1&review_flag=0&ab_group=201616&update_version_code=6753&openudid=503c73bce41529a8e28bb7fe9f98f7fbc37fd45c&pos=5pe9vb%252F%252B9Onkv72nvb97ADB4KgO%252FsZe9vb%252Fx8vP69Ono%252Bfi%252Fvae9rK%252Bts62krKqsqa%252Bupa2pqKmlsZe9vb%252Fx%252FOn06ej5%252BL%252B9p72urbOvpa2kr6yupa%252BopK2tqKWX4A%253D%253D&idfv=A9EA23F1-848B-4730-A847-89B988EB7A3B&ac=WIFI&os_version=12.2&ssmix=a&device_platform=iphone&iid=71980003246&ab_client=a1%2Cf2%2Cf7%2Ce1&device_type=iPhone%206S%20Plus&idfa=00000000-0000-0000-0000-000000000000'
        query = query.format(**query_dict)
        api = url + query
        result = self._get(api, headers)

        result = json.loads(result)
        return result['err_no'] == 4 or result['err_no'] == 1 


def _read(user: TouTiaoSpeedUser):
    # {'err_no': 9, 'data': {'content': '奖励认真阅读的你', 'score_amount': 0}, 'err_tips': '反作弊失败'}
    sleep_duration = 40

    read_limit_push = False
    read_limit_normal = False
    for group_id in user.feed():

        if read_limit_push == False:
            read_limit_push = user.get_read_bonus(group_id)

        if read_limit_push == True:
            break

        time.sleep(sleep_duration)

    time.sleep(5)

    for group_id in user.feed():

        if read_limit_normal == False:
            read_limit_normal = user.get_read_bonus(group_id, False)

        if read_limit_normal == True:
            break

        time.sleep(sleep_duration)


def genUsers():
    yield TouTiaoSpeedUser(u134_xss_cookie, u134_Cookie)
    # yield TouTiaoSpeedUser(u165_xss_cookie, u165_Cookie)
    yield TouTiaoSpeedUser(u152_xss_cookie, u152_Cookie)


if __name__ == "__main__":
    for user in genUsers():
        print('\033[1;31m---------------------------\033[0m')
        user.open_treasure_box()
        _read(user)
