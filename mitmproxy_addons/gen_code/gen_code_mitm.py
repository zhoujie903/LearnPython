import pathlib
import os.path
import json
import re
import time
import pprint
from urllib.parse import urlparse
import logging

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy import http

from jinja2 import Template

'''
生成接口python代码
'''

class Api(object):
    def __init__(self, url, params_as_all=False, body_as_all=False, f_p_arg: set=None, f_p_kwarg: dict=None, f_b_arg: set=None, f_b_kwarg: dict=None):
        self.url = url
        self.f_p_arg = f_p_arg
        self.f_b_arg = f_b_arg
        self.f_p_kwarg = f_p_kwarg
        self.f_b_kwarg = f_b_kwarg        
        self.params_as_all = params_as_all 
        self.body_as_all = body_as_all
        self.str_d = ''

    def __str__(self):
        return f'Api(url={self.url})'
    
    def _str_fun_params(self):
        s = ''
        if self.f_p_arg and not self.params_as_all:
            s +=", "
            s +=", ".join(self.f_p_arg)

        if self.f_b_arg and not self.body_as_all:
            s +=", "
            s +=", ".join(self.f_b_arg)

        if self.f_p_kwarg and not self.params_as_all:
            for k,v in self.f_p_kwarg.items():
                s += f', {k}={v!r}'

        if self.f_b_kwarg and not self.body_as_all:
            for k,v in self.f_b_kwarg.items():
                s += f', {k}={v!r}'

        if self.params_as_all:
            s +=', params_as_all'
        if self.body_as_all:
            s +=', body_as_all'
        return s

    def str_fun_params(self):
        if not self.str_d:
            self.str_d = self._str_fun_params()
        return self.str_d

class NamedFilter(object):
    def __init__(self, urls, name=''):
        self.name = name
        self.flts = dict()
        for u in urls:
            a = u
            if isinstance(u, str):
                a = Api(u)
            flt = flowfilter.parse(a.url)
            self.flts[flt] = a
        self.current_api = None

    def __call__(self, f):
        for flt, api in self.flts.items():
            if flt(f):
                self.current_api = api
                return True 
        return False

class GenCode(object):
    def __init__(self):
        ctx.log.info('__init__')
        

        self.re_ios = re.compile(r'iphone|ios',flags=re.IGNORECASE)
        self.re_xiao = re.compile(r'xiaomi|miui|mi\+5|miui',flags=re.IGNORECASE)
        self.re_huawei = re.compile(r'huawei',flags=re.IGNORECASE)

        self.template_dir = os.path.dirname(__file__)
        tfile = f'{self.template_dir}/api_template.j2.py'
        with open(tfile) as f:
            s = f.read()
            self.api_template = Template(s) 

        self.file_dir = '/Users/zhoujie/Desktop/api/'
        self.file_params_keys = 'data-params-keys.json'
        self.file_bodys_keys = 'data-bodys-keys.json'
        # self.file_all = 'data-all.json'
        self.file_headers = 'data-headers.json'
        self.file_params = 'data-params.json'
        self.file_bodys = 'data-bodys.json'
        self.file_cannot = 'data-xxx-data.json'
        self.file_app_hosts = 'data-app-hosts.json'
        self.file_app_fn_url = 'data-fn-url.json'

        self.headers = {}
        self.params = {}
        self.bodys = {}

        self.params_keys = {}
        self.bodys_keys = {}
        # 不能伪造但可以重放的数据
        self.can_not_create = {
            r'task/timer_submit': {},
            r'/v5/article/complete.json': {},
        }

        # app包含哪些hosts
        self.app_hosts = {}
        self.app_apis = {}
        self.app_fn_url = {}

        self.can_not_create = self.load_file(self.file_cannot, self.file_dir)

        self.params_keys = self.load_file(self.file_params_keys, self.file_dir)
        self.bodys_keys = self.load_file(self.file_bodys_keys, self.file_dir)

        self.headers = self.load_file(self.file_headers, self.file_dir)

        self.params = self.load_file(self.file_params, self.file_dir)

        self.bodys = self.load_file(self.file_bodys, self.file_dir)

        self.app_hosts = self.load_file(self.file_app_hosts, self.file_dir)

        for device, d in self.app_hosts.items():
            for app, dd in d.items():
                self.app_hosts[device][app] = set(dd)
        pprint.pprint(self.app_hosts)

        self.app_fn_url = self.load_file(self.file_app_fn_url, self.file_dir)
 
        urls = [
            'score_task/v1/task/page_data/',
            'score_task/v1/task/sign_in/',
            'score_task/v1/task/open_treasure_box/',
            Api('score_task/v1/task/new_excitation_ad/', {"score_source":None}),            
            'score_task/v1/task/get_read_bonus/',
            'score_task/v1/task/done_task/',
            'score_task/v1/landing/add_amount/',             
            'score_task/v1/user/profit_detail/',
            'score_task/v1/novel/bonus/', #读小说得金币
            'search/suggest/homepage_suggest/',
            'search/suggest/initial_page/',
            Api(r'score_task/v1/walk/count/',{"count":None}),
            r'score_task/v1/walk/',

            'score_task/v1/sleep/status/',
            'score_task/v1/sleep/start/',
            'score_task/v1/sleep/stop/',
            'score_task/v1/sleep/done_task/',#睡觉领金币

            r'ttgame/game_farm/',

            r'score_task/lite/v1/eat/eat_info/',

            'score_task/lite/v1/eat/done_eat/',
            'api/news/feed/v47/',#安卓视频tab页
            'api/news/feed/v64/',#ios视频tab页
            'api/search/content/',           
        ]
        self.toutiao = NamedFilter(urls, 'jin-ri-tou-tiao')

        # 火山极速版
        urls = [
            'luckycat/v1/task/page/',
            'luckycat/v1/task/sign_in/',
            'luckycat/v1/task/open_treasure_box/',
            'luckycat/v1/task/done_task/',
            'luckycat/v1/landing/add_amount/',
            'luckycat/v1/task/get_read_bonus/',            
        ]
        self.huoshan = NamedFilter(urls, 'huo-shan')

        # 趣头条
        urls = [
            r'sign/sign',#每日签到
            Api(r'/mission/intPointReward',params_as_all=True),#时段签到
            r'/x/game-center/user/sign-in',
            r'/newuserline/activity/signRewardNew',#挑战签到
            r'/mission/receiveTreasureBox',
            r'/content/readV2',
            Api(r'/app/re/taskCenter/info/v1/get',params_as_all=True),
            # r'taskcenter/getListV2',#旧版本 tab页：任务
            # r'api-coin-service.aiclk.com/coin/service',
            Api(r'/coin/service',params_as_all=True),
            r'readtimer/report',
            r'motivateapp/mtvcallback',
            r'x/feed/getReward',#信息流 - 惊喜红包
            r'x/v1/goldpig/bubbleWithdraw', # 金猪 - 看视频
            r'x/v1/goldpig/withdraw', #金猪 
            r'finance/piggybank/taskReward',#存钱罐

            r'x/tree-game/',
            r'x/tree-game/task-list',
            r'x/tree-game/left-plant-num',
            r'x/tree-game/plant-ok',
            r'x/tree-game/add-plant',
            r'x/tree-game/fertilizer/add',
            r'x/tree-game/fertilizer/use',
            r'x/tree-game/water-plants',
            r'x/tree-game/my-gift-box/draw-lottery',
            r'x/tree-game/my-gift-box/receive-prize',

            r'x/open/game',
            r'x/task/encourage/activity/grant',#游戏 - 瓜分
            r'/api/Login',
            r'api/loginGame',
            r'api/qttAddCoin',
            r'api/AddCoin',# 游戏 - 成语

            #游戏 - 切菜
            Api(r'/x/open/coin/add',body_as_all=True),
        ]
        self.qu_tou_tiao = NamedFilter(urls, 'qu-tou-tiao') 

        # 百度 - 好看
        urls = [
            r'activity/acusercheckin', # 每日签到
            r'signIn/new/sign', # 游戏中心签到
            r'activity/acad/rewardad', #看视频
            r'api/task/1/task/379/complete', #看视频
        ]
        self.hao_kan = NamedFilter(urls, 'hao-kan') 

        # 百度 - 全民小视频 
        urls = [
            r'mvideo/api', # 每日签到
        ]
        self.quan_ming = NamedFilter(urls, 'quan-ming') 

        # 蚂蚁看点
        urls = [
            r'article/treasure_chest',#时段签到
            r'TaskCenter/daily_sign',
            # r'WebApi/',
            r'WebApi/Stage/task_reward',
            r'WapPage/get_video_status',
            r'WebApi/RotaryTable/turn_rotary_new',
            r'WebApi/RotaryTable/turn_reward',
            r'WebApi/RotaryTable/video_double',
            r'WebApi/RotaryTable/chestReward',

            # 旧版答题
            r'WebApi/Answer/getData',
            r'WebApi/Answer/answer_question',
            r'WebApi/Answer/answer_reward',
            r'WebApi/Answer/video_double',
            r'WebApi/Answer/fill_energy',
            
            # 新版答题
            r'/v6/Answer/getData.json',
            r'/v5/answer/first_reward',
            r'/v6/Answer/answer_question.json',
            r'/v5/answer/answer_reward.json',

            r'article/haotu_video',#看视频得金币
            r'article/complete_article',#读文章得金币
            r'v5/user/rewar_video_callback',
        ]
        self.ma_yi_kd = NamedFilter(urls, 'ma-yi-kd') 

        # 中青看点
        urls = [
            r'getTimingRedReward.json',#时段签到
            r'webApi/AnswerReward/',
            r'/v5/article/complete.json',
        ]
        self.zhong_qin_kd = NamedFilter(urls, 'zhong-qin-kd')

        # 东方头条 
        urls = [
            r'sign/news_take_s',
            r'timesaward/timesaward/get_award',
            r'answer_question_new/get_question',
            r'answer_question_new/add_user_bonus',
            r'zhuanpan_v3/get_zhuanpan_new',
            r'zhuanpan_v3/get_gold',
            r'hit_susliks/hit_susliks/start_play_game',
            r'hit_susliks/hit_susliks/finish_play_game',
            r'hit_susliks/hit_susliks/set_user_video_num',
            r'hit_susliks/hit_susliks/lucky_draw',
            r'turn_over_packet/packet/add_packet_bonus',
        ]
        self.dftt = NamedFilter(urls, 'dong-fan-tt')

        # 彩蛋视频 
        urls = [
            r'task/timer_submit',
            r'/h5/task/submit',
            r'/h5/bubble/prize',
        ]
        self.cai_dan_sp = NamedFilter(urls, 'cai-dan-sp')

        urls = [
            r'/login/index',
            r'/main/index',
            r'/card/info',
            r'/card/open',
            r'/card/doublereward',
        ]
        self.kai_xin_da_ti = NamedFilter(urls, 'kai-xin-da-ti')

        # 趣键盘
        urls = [
            r'/gk/game/fanpai/basicInfo',
            r'/gk/game/fanpai/getAward',
            r'/gk/game/fanpai/awardDouble',
            r'/gk/game/fanpai/',

            r'/gk/draw/info',
            r'/gk/draw/extract',
            Api('/gk/draw/double',{"ticket":None}),
            r'/gk/draw/package',
            r'/gk/draw/pkdouble',

            Api('/gk/game/bianlidian/receiveBox',{"packageId": None}),
            Api('/gk/game/bianlidian/draw/double',{"ticket":None}),
            r'/gk/garbage/',
            r'/gk/game/dadishu/',
            r'/gk/game/bianlidian/',
            r'/qujianpan/',
            # r'',
        ]
        self.qu_jian_pan = NamedFilter(urls, 'qu-jian-pan')

        self.flowfilters = [
            self.toutiao, 
            self.huoshan, 
            self.qu_tou_tiao, 
            self.hao_kan,
            self.quan_ming,
            self.ma_yi_kd,
            self.dftt,
            self.zhong_qin_kd,
            self.cai_dan_sp,
            self.kai_xin_da_ti,
            self.qu_jian_pan,
        ]      

    def load(self, loader):
        ctx.log.info('event: load')

    def configure(self, updated):
        ctx.log.info('event: configure')

    def running(self):
        ctx.log.info('event: running')

    def done(self):
        print('event: done')
        try:
            # for _, host_headers in self.headers.items():
            #     for host, headers  in host_headers.items():
            #         self._delete_some_headers(headers)
            self._gen_file(self.headers, self.file_headers, self.file_dir)
            print(f"生成 {self.file_headers} 成功")

            self._gen_file(self.params, self.file_params, self.file_dir)
            print(f"生成 {self.file_params} 成功")

            try:
                #pprint.pprint(self.bodys)
                self._gen_file(self.bodys, self.file_bodys, self.file_dir)
                print(f"生成 {self.file_bodys} 成功")
            except Exception as e:
                print(e)                


            temp = self.can_not_create.copy()
            for body in temp.values():
                for key, value in body.items():
                    if isinstance(value, set):
                        body[key] = list(value)
            self._gen_file(temp, self.file_cannot, self.file_dir)
            print(f"生成 {self.file_cannot} 成功")


            # all_data = self.params.copy()
                
            # self._gen_file(all_data, self.file_all, self.file_dir)
            # print(f"生成 {self.file_all} 成功")

            self._gen_file(self.params_keys, self.file_params_keys, self.file_dir)
            print(f"生成 {self.file_params_keys} 成功")

            self._gen_file(self.bodys_keys, self.file_bodys_keys, self.file_dir)
            print(f"生成 {self.file_bodys_keys} 成功")

            temp = {}
            for device, d in self.app_hosts.items():
                temp[device] = d.copy()
                for app, dd in d.items():
                    temp[device][app] = list(dd)
            self._gen_file(temp, self.file_app_hosts, self.file_dir)
            print(f"生成 {self.file_app_hosts} 成功")

            self._gen_file(self.app_fn_url, self.file_app_fn_url, self.file_dir)
            # -------------------------------------------------------

            # 生成app下的 data-bodys-keys.json
            # data-bodys-keys-xxx.json
            for device, d in self.bodys_keys.items():
                for app, dd in d.items():
                    self._gen_file(dd, f'data-bodys-keys-{device}.json', f'{self.file_dir}{app}')
            print(f"生成 app - data-bodys-keys.json 成功")            

            # 生成app下的 data-params-keys.json
            # data-params-keys-xxx.json
            for device, d in self.params_keys.items():
                for app, dd in d.items():
                    self._gen_file(dd, f'data-params-keys-{device}.json', f'{self.file_dir}{app}')
            print(f"生成 app - data-params-keys.json 成功")

            # 生成app下的 data-fn-url.json
            # data-fn-url-xxx.json
            for device, d_app_fn_url in self.app_fn_url.items():
                for app, fn_url in d_app_fn_url.items():
                    self._gen_file(fn_url, f'data-fn-url-{device}.json', f'{self.file_dir}{app}')            
            print(f"生成 app - data-fn-url.json 成功")

            sessions_by_app = {}
            # sessions_jinja_data = list()
            # 生成app下的 session_xxx.py
            # app, device, data
            for device, d in self.headers.items():
                for app, dd in d.items():
                    sessions_jinja_data = sessions_by_app.setdefault(app, list())
                    sessions_jinja_data.append({ 
                        'file': f'session_{device}',
                        'session': device,
                    })

                    merge_hosts = {}
                    for host, ddd in dd.items():
                        merge_hosts.update(ddd)
                        
                    with open(f'{self.file_dir}{app}/session_{device}.py', mode='w') as f:

                        def gen_var(file_name: str, var_name: str, f):
                            with open(file_name) as ff:
                                t = json.load(ff)
                                s = f'{var_name} = ' + json.dumps(t, indent=2, sort_keys=True)
                                f.write('\n\n') 
                                f.write(s)    
                        gen_var(f'{self.file_dir}{app}/data-params-keys-{device}.json', 'params_keys', f)

                        gen_var(f'{self.file_dir}{app}/data-bodys-keys-{device}.json', 'bodys_keys', f)

                        gen_var(f'{self.file_dir}{app}/data-fn-url-{device}.json', 'fn_url', f)
                        

            self.plain_values_to_file(self.headers, 'header_values')
            self.plain_values_to_file(self.params, 'param_values')
            self.plain_values_to_file(self.bodys, 'body_values')

            # 生成app下的 code.py, sessions.py
            for app, apis in self.app_apis.items():
                seq = apis.values()

                tfile = f'{self.template_dir}/code_template.j2.py'
                gfile = f'{self.file_dir}{app}/code-{app}.py'
                self.gen_file_from_jinja2(tfile,gfile,seq=seq)

                tfile = f'{self.template_dir}/sessions.j2.py'
                gfile = f'{self.file_dir}{app}/sessions.py'
                self.gen_file_from_jinja2(tfile, gfile, seq=sessions_by_app[app])

            print('done !!!')
        except Exception as e:
            logging.error('有异常：')
            print(e)
            logging.error(e)
            

    def response(self, flow: http.HTTPFlow):
        ft = None
        for flt in self.flowfilters:
            if flt(flow):
                ft = flt
                break
        if ft:
            api: Api = ft.current_api
            ctx.log.error(f'api = {api}')
            request: http.HTTPRequest = flow.request

            parse_result = urlparse(request.url)
            url_path = parse_result.path

            function_name = re.sub(r'[/-]','_', url_path).strip('_').lower()
            api_url = f'{request.scheme}://{request.pretty_host}{url_path}' 
            headers_code = self.headers_string(flow)
            params_code = self.params_string(flow)
            data_code = self.data_string(flow) 

            path = pathlib.Path(f'{self.file_dir}{ft.name}')
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            with (path/f'{function_name}.text').open('a') as f:

                app_apis = self.app_apis.setdefault(ft.name, dict())
                if not function_name in app_apis:
                    api.name = function_name
                    api.url = api_url
                    api.method = request.method.lower()
                    api.content_type = 'json' if 'json' in request.headers.get('content-type','') else ''
                    api.fun_params = api.str_fun_params()
                    app_apis[function_name] = api

                api.time = time.strftime('%m-%d %H:%M:%S')
                api.headers_code = headers_code
                api.params_code = params_code
                api.data_code = data_code
                api.response = flow.response.text

                code = self.api_template.render(request=api)
                f.write(code)                

                device = self._guess_device(flow)

                self.gather_params_and_bodys(flow, device=device, app=ft.name)

                d = self.inner_by_list(self.app_hosts, [device])
                app_hosts = d.setdefault(ft.name, set())
                app_hosts.add(request.pretty_host)

                d_v = self.app_fn_url.setdefault(device, dict())
                fn_url = d_v.setdefault(ft.name, dict())
                fn_url[function_name] = api_url



    def headers_string(self, flow: http.HTTPFlow, indent=1):
        d = dict(flow.request.headers)
        return 'headers = {'+json.dumps(d, indent='\t'*(indent+1)).strip('{}') + '\t}'


    def params_string(self, flow: http.HTTPFlow, indent=1):
        d = dict(flow.request.query)
        return 'params = {'+json.dumps(d, indent='\t'*(indent+1)).strip('{}') + '\t}'

    def data_string(self, flow: http.HTTPFlow):
        '''
        Content-Type: application/x-www-form-urlencoded
        Content-Type: application/json; charset=utf-8
        Content-Type: text/plain;charset=utf-8
        '''
        lines = ''

        # [urlencoded_form, multipart_form, plan, json]取其一
        for key,value in flow.request.urlencoded_form.items():
            lines += f"\n\t\t'{key}': '{value}',"

        for key,value in flow.request.multipart_form.items():
            key = key.decode(encoding='utf-8')
            value = value.decode(encoding='utf-8') 
            lines += f"\n\t\t'{key}': '{value}',"

        # Todo:复杂json数据还不能代码化
        if 'application/json' in flow.request.headers.get('content-type',''):
            try:
                d = json.loads(flow.request.text)
                for key,value in d.items():
                    lines += f"\n\t\t'{key}': {value},"
            except Exception as e:
                pass
        
        s = f'''data = {{{lines}\n\t}}'''        
        return s

    def gather_params_and_bodys(self, flow: http.HTTPFlow, device='', app=''):
        '''
        request.multipart_form: Key and value are bytes. json序列化时会出错：键不能为bytes
        ''' 
        request: http.HTTPRequest = flow.request

        by_host_device = request.pretty_host
        host = request.pretty_host

        # 收集headers
        d = self.inner(self.headers, device=device, app=app, host=host)
        d.update(flow.request.headers)

        # 收集params
        d = self.inner(self.params, device=device, app=app, host=host)
        d.update(flow.request.query)

        # 收集bodys
        bodys_keys = list()
        d = self.inner(self.bodys, device=device, app=app, host=host) 
        d.update(flow.request.urlencoded_form)
        bodys_keys = list(flow.request.urlencoded_form.keys())
        # d.update(flow.request.multipart_form)
        for key,value in flow.request.multipart_form.items():
            key = key.decode(encoding='utf-8')
            value = value.decode(encoding='utf-8') 
            d[key] = value
            bodys_keys.append(key)
        try:
            o = json.loads(flow.request.text)
            d.update(o)
            bodys_keys = list(o.keys())
        except :
            pass


        parse_result = urlparse(request.url)
        fname = parse_result.path

        dd = self.inner(self.bodys_keys, device=device, app=app, host=host) 
        dd[fname] = bodys_keys#list(d.keys())
        ctx.log.error('abc--------------abc')
        ctx.log.error(str(dd))        
        ctx.log.error('abc--------------abc')
        d = self.inner(self.params_keys, device=device, app=app, host=host) 
        d[fname] = list(flow.request.query.keys())


        path = request.path
        for item in self.can_not_create.keys():
            if item in path:
                ctx.log.error(f'hit path {path}')
                d = self.can_not_create[item]
                body = json.loads(flow.request.text)
                for key, value in body.items():
                    values = d.setdefault(key, set())
                    values.add(value)



    def function_name(self, flow: http.HTTPFlow):
        request: http.HTTPRequest = flow.request

        parse_result = urlparse(request.url)
        url_path = parse_result.path

        function_name = re.sub(r'[/-]','_', url_path).strip('_').lower() 
        return function_name
    
    def _delete_some_headers(self, headers: dict):
        for key in {'Host','Connection','Content-Length','Accept-Encoding','Cache-Control','Pragma'}:
            try:
                headers.pop(key)
            except :
                pass

    def _gen_file(self, o, f, fold, mode='w'):
        path = pathlib.Path(fold)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        with (path/f).open(mode=mode) as f:
            json.dump(o, f, indent=2, sort_keys=True)

    def _guess_device(self, flow: http.HTTPFlow):
        device = ''
        request = flow.request

        guess_by_data = ''
        # ------------------------------------
        for h, v in request.headers.items():
            d = v.lower()
            if 'iphone' in d:
                device = 'ios'
                guess_by_data = v 
                break

            if self.re_xiao.search(d):
                device = 'xiaomi'
                guess_by_data = v 
                break                

            if self.re_huawei.search(d):
                device = 'huawei'
                guess_by_data = v 
                break

        for h, v in request.query.items():
            if self.re_xiao.search(v):
                device = 'xiaomi'
                guess_by_data = v 
                break            

            if self.re_huawei.search(v):
                device = 'huawei'
                guess_by_data = v 
                break

        for h, v in request.urlencoded_form.items():
            if self.re_xiao.search(v):
                device = 'xiaomi'
                guess_by_data = v 
                break            

            if self.re_huawei.search(v):
                device = 'huawei'
                guess_by_data = v 
                break
        # ------------------------------------

        ctx.log.error(f'device = {device}')
        ctx.log.error(f'guess = {guess_by_data}')
        if device == '':
            ctx.log.error(f"not guess: {request.url}")
            device = 'default'
            device = 'huawei'
        return device 

    def load_file(self, f, fold):
        try:
            with open(f'{fold}{f}', 'r') as fd:
                o = json.load(fd)
                ctx.log.info(f'load {f} success!')
                return o 
        except:
            ctx.log.error(f'load {f} fail!')
            return dict()

    def gen_file_from_jinja2(self, tfile, gfile, **kwargs):
        with open(tfile) as f:
            s = f.read()
            t = Template(s)
            ss = t.render(**kwargs)
            with open(gfile, mode='w') as ff:
                ff.write(ss)

    def inner(self, d, device='', app='', host=''):
        d = d.setdefault(device, dict())
        d = d.setdefault(app, dict())
        d = d.setdefault(host, dict())
        return d

    def inner_by_list(self, d, l: list):
        for key in l:
            d = d.setdefault(key, dict())
        return d

    def plain_values_to_file(self, data: dict, var_name):
        for device, d in data.items():
            for app, dd in d.items():
                merge_hosts = {}
                for host, ddd in dd.items():
                    merge_hosts.update(ddd)
                    
                with open(f'{self.file_dir}{app}/session_{device}.py', mode='a') as f:
                    s = f'{var_name} = ' + json.dumps(merge_hosts, indent=2, sort_keys=True)
                    f.write('\n\n')
                    f.write(s)


addons = [
    GenCode()
]


if __name__ == "__main__":
    import shlex, subprocess


    print(__file__)
    # subprocess.Popen(['mitmdump', '-s', __file__])
    
    api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=False,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',params_as_all=False, body_as_all=True,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True)#时段签到
    print(api.str_fun_params())

    api.name = 'mission_intPointReward'
    api.method = 'post'
    api.content_type = 'json'
    api.fun_params = api.str_fun_params()
    api.params_as_all = True
    api.body_as_all = True
    seq = [api]  

    template_dir = os.path.dirname(__file__)
    tfile = f'{template_dir}/code_template.j2.py'
    tfile = f'{template_dir}/api_template.j2.py'
    with open(tfile) as f:
        s = f.read()
        t = Template(s)
        # ss = t.render(seq=seq)
        ss = t.render(request=api)
        print(ss)

    print('done')
