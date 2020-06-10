
import json
import logging
import pathlib
import random
import re
import sys
import time
import traceback
from urllib.parse import urlparse

import requests

class CommonUser(object):
    def __init__(self, session_data: dict): 
        self.headers = session_data['header_values']
        self.params_keys = session_data['params_keys']
        self.bodys_keys = session_data['bodys_keys']
        self.urls = session_data['fn_url']
        self.params = session_data['param_values']
        self.bodys = session_data['body_values']
        self.params_as_all = session_data['params_as_all']
        self.bodys_as_all = session_data['bodys_as_all']
        self.params_encry = session_data['params_encry']
        self.bodys_encry = session_data['bodys_encry']
        self.session_id = session_data['session_id']
        self.api_ok = session_data['api_ok']
        self.urlparsed = dict()
        self.api_errors = dict()
        self.exc_info = []
        self.session = requests.Session()
        self.session.headers = self._header()


    def _header(self):
        return {
            'User-Agent': self.headers['User-Agent'],
            'user-agent': self.headers['user-agent'],
            # 'Cookie':self.headers['Cookie'],
        }

    def __urlparsed(self, url):
        if self.urlparsed.get(url):
            host, path = self.urlparsed[url]
        else:
            parse_result = urlparse(url)
            host = parse_result.netloc
            path = parse_result.path
            self.urlparsed[url] = host, path
        return host, path

    def __parse(self, url, res, p):
        result = res.text
        j = ""
        try:
            j = json.loads(result)
            app_ok_codes = self.api_ok['app_ok']# dict(str,list)

            response_key = 'nil'
            for k in app_ok_codes:
                if not j.get(k, 9999999) == 9999999:
                    response_key = k
                    break

            response_code = j.get(response_key, 9999999)

            codes_app = app_ok_codes.get(response_key, [])

            if response_code in codes_app:
                p(j)
                return result

            _, path = self.__urlparsed(url)
            codes_url = self.api_ok.get(path, {}).get(response_key,[])
            if response_code in codes_url:
                p(j)
                return result

            self.api_errors[path] = j
            logging.error(f"\033[1;31m {j} \033[0m")
        except json.JSONDecodeError:
            p(result)
        except :
            logging.error(f"\033[1;31m {j} \033[0m")
        finally:
            print()
        return result

    def _post(self, url, p=logging.warning, **kwargs):
        r"""Sends a POST request.

        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: str
        """
        res = self.session.post(url, **kwargs)
        return self.__parse(url, res, p)

    def _get(self, url, p=logging.warning, **kwargs):
        res = self.session.get(url, **kwargs)
        return self.__parse(url, res, p)

    def _params_from(self, url):
        host, path = self.__urlparsed(url)
        params_keys = self.params_keys[host][path]
        return { k:v for k,v in self.params.items() if k in set(params_keys) }

    def _bodys_from(self, url):
        host, path = self.__urlparsed(url)
        params_keys = self.bodys_keys[host][path]
        return { k:v for k,v in self.bodys.items() if k in set(params_keys) }


class GameUser(CommonUser):
    APP_ID_STR: str = ''
    APP_ID: int = -1 # 未设置
    def __init__(self, session_data: dict):
        super().__init__(session_data)
        self.access_token_isset = False

    def _setup_g_token(self):
        result = self.x_user_token()
        g_token = result['data']['g_token']
        self.params['g_token'] = g_token
        self.bodys['g_token'] = g_token

    def get_ticket(self, app_id: str) -> str:
        result = self.x_open_game(app_id)
        url = result['data']['url']
        m = re.search("ticket=(\\w+)", url, re.M)
        ticket = m.group(1)
        return ticket

    def _setup_ticket(self):
        ticket = self.get_ticket(self.APP_ID_STR)
        self.params['ticket'] = ticket

    def _setup_access_token(self):
        if self.APP_ID == -1:
            raise ValueError('APP_ID 未设置')

        if self.access_token_isset:
            return
        result = self.get_access_token(self.APP_ID)
        self.session.headers['access_token'] = result['payload']['access_token']
        self.access_token_isset = True


    # 登录
    def x_user_token(self):
        logging.info('/x/user/token - 获取g_token')

        url = self.urls['/x/user/token']

        params = self._params_from(url)

        data = self._bodys_from(url)

        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result   

    def x_open_game(self, app_id):
        logging.info('/x/open/game - 获取ticket')

        url = self.urls['/x/open/game']

        params = self._params_from(url)
        params['app_id'] = app_id

        data = self._bodys_from(url)

        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result


    # 中心 - 签到
    def x_game_center_gapp_sign_in(self):
        logging.info('签到')

        url = self.urls['/x/game-center/gapp/sign-in']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def x_game_center_gapp_sign_in_double(self):
        logging.info('签到 - 双倍')

        url = self.urls['/x/game-center/gapp/sign-in-double']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result


    # 上报 - 相当于完成任务
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


    # 金币-账户-提现
    def get_access_token(self, app_id):
        logging.info('获取access_token')

        url = self.urls['/qapptoken']

        params = self._params_from(url)
        params['app_id'] = app_id

        data = self._bodys_from(url)

        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def withdraw_getbindinfo(self):
        logging.info('取现 - 用户账户信息')

        url = self.urls['/withdraw/getBindInfo']

        params = self._params_from(url)

        data = self._bodys_from(url)

        result = self._get(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def withdraw_sku_list(self):
        logging.info('取现 - 可取现金额列表')

        url = self.urls['/withdraw/sku/list']

        params = self._params_from(url)

        data = self._bodys_from(url)

        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def withdraw_order_create(self, sku_id):
        logging.info('取现 - 取现')

        url = self.urls['/withdraw/order/create']

        params = self._params_from(url)

        data = self._bodys_from(url)
        data['sku_id'] = sku_id

        result = self._post(url, params=params, data=data)
    
        result = json.loads(result)
        return result

    def withdraw_order_listapp(self):
        logging.info('取现 - 提现列表')

        url = self.urls['/withdraw/order/listApp']

        params = self._params_from(url)

        data = self._bodys_from(url)

    
        result = self._get(url, params=params, data=data, p=logging.debug)
    
        result = json.loads(result)
        return result

    def withdraw_getcoinlog(self, page, page_size):
        logging.info('金币明细')

        url = self.urls['/withdraw/getCoinLog']

        params = self._params_from(url)
        params['page'] = page
        params['page_size'] = page_size

        data = self._bodys_from(url)


        result = self._get(url, params=params, data=data, p=logging.debug)

        result = json.loads(result)
        return result
class User(object):
    pass

# 提现
def ti_xian(user: GameUser):
    try:
        # result = user.get_access_token()
        # user.session.headers['access_token'] = result['payload']['access_token']
        
        user._setup_access_token()

        result = user.withdraw_order_listapp()
        for item in result['data']['list']: 
            create_time = item['create_time']#2020-03-17 19:14:24
            balance = item['balance']
            today = time.strftime('%Y-%m-%d')
            if today == create_time[0:10]:
                logging.info(f"\033[1;31m今日已提现 - {balance}元\033[0m")
                return 
            break

        result = user.withdraw_getbindinfo()
        item = result['data']
        coins = item['coins']
        wx_nickname = item['wx_nickname']
        is_bind_wx = item['is_bind_wx']
        is_bind_tel = item['is_bind_tel']

        logging.info(f"\033[1;31m{wx_nickname} {coins}\033[0m")

        if not (is_bind_tel == 1 and is_bind_wx == 1):
            logging.info(f"\033[1;31m不能提现 - 未绑定手机号或微信 {is_bind_tel=} {is_bind_wx=}\033[0m")
            return


        result = user.withdraw_sku_list()
        for item in sorted(result['data'], key=lambda item: item['price'], reverse=True):
            sku_id = item['id'] 
            name = item['name'] 
            price= item['price'] 
            withdraw_qualify= item['withdraw_qualify'] 
            view_qualify= item['view_qualify'] 
            print(f'{sku_id=} {name=} {price=}')
            if price * 10 <= coins and view_qualify == 1 and withdraw_qualify == 1:
                print(f'\033[1;31m{wx_nickname} 可以取现 {name}\033[0m')
                result = user.withdraw_order_create(sku_id)
                if result['code'] == 0:
                    print(f'\033[1;31m{wx_nickname} 成功取现 {name}\033[0m')    
                    
                if result['code'] in [-22003, -24003, -22006, 0]:
                    #-22003-作弊用户禁止提现，有疑问请联系客服！
                    #-24003-每天最多提现1次,请明天再试 
                    #-22006-Tk is required / 提现资格已用完 
                    break
                time.sleep(5)
    except :
        traceback.print_exc()


def ti_xian_history(user: GameUser):
    try:
        user._setup_access_token()
        result = user.withdraw_order_listapp()
        for item in result['data']['list']:
            balance = item['balance']
            tp_nickname = item['tp_nickname']
            status = item['status']#60:已到账
            create_time= item['create_time']
            logging.info(f'{tp_nickname} {create_time} {status} {balance}')
        return result['data']['list']
    except :
        traceback.print_exc()


# 金币详情
def income(user: GameUser):
    try:
        user._setup_access_token()
        import itertools
        import functools
        record = []
        page = 1
        page_size = 50
        coins = 0
        run = True
        today = time.strftime('%Y-%m-%d', time.localtime())
        while run:
            result = user.withdraw_getcoinlog(page, page_size)
            for item in result['data']:
                # name = item['name']
                # desc = item['desc']
                create_time = item['create_at']# "2020-02-06 08:06:30"
                amount = item['amount']
                # d = create_time[0:len(today)] 
                if not create_time[0:len(today)] == today:
                    run = False
                    break
                record.append(item)
            page += 1
            if len(result['data']) == 0:
                run = False
        print(today, len(record))
        record.sort(key=lambda item: (item['name'],str(item['desc'])))
        gy = itertools.groupby(record, key=lambda item: (item['name'],str(item['desc'])))
        for k, g in gy:
            title = f"{k[0]} - {k[1]}"
            amount = 0            
            times = 0            
            for item in g:
                amount += int(item['amount'])
                times += 1
            coins += amount if amount > 0 else 0
            print(f'{title} : {amount} : {times}')
        print(f"\033[1;31m{coins=}\033[0m")
    except Exception as e:
        print(e)

def genRunner(user: CommonUser):
    def xxx(user: User):
        pass
    r = xxx
    r = yield
    while True:
        try:
            r = yield r(user)
        except StopIteration as e:
            print('StopIteration', e)
        except Exception as e:
            user.exc_info.append(sys.exc_info())
            r = yield sys.exc_info()

def framework_main(run, users):
    '''
    run: Callable, 用户要运行的代码
    users: Iterable[CommonUser]
    '''

    import asyncio

    sessions = []
    api_errors = {}
    exc_info = {}

    done, _ = asyncio.run(asyncio.wait([_run_it(run, user) for user in users]))

    for item in done:
        user: User = item.result()
        sessions.append(user.session_id)
        api_errors[user.session_id] = user.api_errors
        exc_info[user.session_id] = user.exc_info

    for session, v in api_errors.items():
        if len(v):
            logging.info(f"\033[1;31m {session} - 有如下问题: \033[0m")
            for url, message in v.items():
                logging.info(f"\033[1;31m\t{url} - {message}\033[0m")
                print()
    print()

    for session, v in exc_info.items():
        if len(v):
            logging.info(f"\033[1;31m {session} - 有如下异常: \033[0m")
            for info in v:
                traceback.print_exception(*info, limit=None, file=None, chain=True)
                print()
    print()

    logging.info(f"共运行: \033[1;31m{sessions}\033[0m")

async def _run_it(run, user):
    try:
        logging.info(f"\033[1;31m{' '*20}\033[0m")
        logging.info(f"\033[1;31m{'-'*10} {user.session_id} {'-'*10}\033[0m")

        runner = genRunner(user)
        runner.send(None)

        await run(runner, user)
        
    except :
        traceback.print_exc()    
    finally:
        logging.info(f"\033[1;31m{'^'*10} {user.session_id} {'^'*10}\033[0m")
        logging.info(f"\033[1;31m{' '*20}\033[0m")

    return user



