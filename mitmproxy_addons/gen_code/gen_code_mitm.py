import pathlib
import os.path
import json
import re
import time
import pprint
from urllib.parse import urlparse
import logging
import itertools

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy import http

from jinja2 import Template

'''
生成接口python代码
mitmdump --flow-detail 0 --set session='huawei' -s "/Users/zhoujie/Documents/zhoujie903/LearnScrapy/mitmproxy_addons/gen_code/gen_code_mitm.py" 
'''

class Api(object):
    def __init__(self, url, f_name='', log='', params_as_all=False, body_as_all=False, f_p_enc: set=None, f_b_enc: set=None, f_p_arg: set=None, f_p_kwarg: dict=None, f_b_arg: set=None, f_b_kwarg: dict=None, content_type=''):
        self.url = url
        self.url_path = ''
        self.f_name = f_name
        self._name = ''
        self.log = log

        self.f_p_arg = f_p_arg
        self.f_p_enc = f_p_enc
        if f_p_enc:
            if self.f_p_arg == None:
                self.f_p_arg = set()
            self.f_p_arg.update(f_p_enc)

        self.f_b_arg = f_b_arg
        self.f_b_enc = f_b_enc
        if f_b_enc:
            if self.f_b_arg == None:
                self.f_b_arg = set()
            self.f_b_arg.update(f_b_enc)

        self.f_p_kwarg = f_p_kwarg
        self.f_b_kwarg = f_b_kwarg        
        self.params_as_all = params_as_all 
        self.body_as_all = body_as_all
        self.str_d = ''
        # content_type取值'json', 'multipart_form', 'urlencoded_form', 'get'
        self.content_type = content_type 

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

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
        if not self.f_name:
            self.f_name = name

class NamedFilter(object):
    def __init__(self, urls, name=''):
        self.app_name = name
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

    def add(self, api: Api):
        flt = flowfilter.parse(api.url)
        self.flts[flt] = api

class GenCode(object):
    def __init__(self):
        ctx.log.info('__init__')
        

        self.re_ios = re.compile(r'iphone|ios', flags=re.IGNORECASE)
        self.re_xiao = re.compile(r'xiaomi|mi\+5|miui', flags=re.IGNORECASE)
        self.re_huawei = re.compile(r'huawei', flags=re.IGNORECASE)

        self.template_dir = os.path.dirname(__file__)
        tfile = f'{self.template_dir}/api_template.j2.py'
        with open(tfile) as f:
            s = f.read()
            self.api_template = Template(s) 

        self.file_dir = '/Users/zhoujie/Desktop/api/'
        self.file_params_keys = 'data-params-keys.json'
        self.file_bodys_keys = 'data-bodys-keys.json'
        self.file_headers = 'data-headers.json'
        self.file_params = 'data-params.json'
        self.file_bodys = 'data-bodys.json'
        self.file_app_hosts = 'data-app-hosts.json'
        self.file_app_fn_url = 'data-fn-url.json'

        self.headers = {}
        self.params = {}
        self.bodys = {}

        self.params_keys = {}
        self.params_encry = {}
        self.bodys_keys = {}
        self.bodys_encry = {}
        self.params_as_all = {}
        self.bodys_as_all = {}

        # app包含哪些hosts
        self.app_hosts = {}
        self.app_apis = {}
        self.app_fn_url = {}
        self.session_hit = set()


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

        # 趣头条小视频
        urls = [
            Api(r'seafood-api.1sapp.com/v1/readtimer/report',log='看视频得金币', f_b_enc={'qdata'}, f_b_arg={'qdata'})
        ]

        self.qtt_video = NamedFilter(urls, 'qtt-video')

        # 趣头条
        urls = [
            r'sign/sign',#每日签到
            Api(r'/mission/intPointReward', log='时段签到', params_as_all=True),
            r'/x/game-center/user/sign-in',
            r'/newuserline/activity/signRewardNew',#挑战签到
            r'/mission/receiveTreasureBox',
            Api(r'/content/readV2',params_as_all=True),
            Api(r'/app/re/taskCenter/info/v1/get',params_as_all=True),
            # r'taskcenter/getListV2',#旧版本 tab页：任务
            # r'api-coin-service.aiclk.com/coin/service',
            Api(r'/coin/service', body_as_all=True),
            r'readtimer/report',
            Api(r'motivateapp/mtvcallback',params_as_all=True),
            Api(r'x/feed/getReward',log='信息流-惊喜红包', params_as_all=True),
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

            # 金猪
            Api(r'/actcenter/piggy/videoConfirm',log='合成金猪 - 气泡', f_p_arg={'tag'}),
            r'/actcenter/piggy/',
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
            Api(r'article/treasure_chest', log='时段签到', f_b_enc={'p'}, content_type='multipart_form'),
            r'TaskCenter/daily_sign',
            # r'WebApi/',
            r'WebApi/Stage/task_reward',
            r'WapPage/get_video_status',
            r'WebApi/RotaryTable/turn_rotary_new',
            r'WebApi/RotaryTable/turn_reward',
            r'WebApi/RotaryTable/video_double',
            r'WebApi/RotaryTable/chestReward',
            
            # 新版答题
            r'/v6/Answer/getData.json',
            r'/v5/answer/first_reward',
            r'/v6/Answer/answer_question.json',
            r'/v5/answer/answer_reward.json',

            Api(r'article/haotu_video',log='看视频得金币', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'article/complete_article',log='读文章得金币', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'/v5/user/rewar_video_callback', log='视频广告 - 得金币', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'/v5/user/adlickstart.json',log='点击广告领金币 - 开始', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'/v5/user/adlickend.json',log='点击广告领金币 - 结束', f_b_enc={'p'}, content_type='multipart_form'),

            # 旧版答题
            r'WebApi/Answer/getData',
            r'WebApi/Answer/answer_question',
            r'WebApi/Answer/answer_reward',
            r'WebApi/Answer/video_double',
            r'WebApi/Answer/fill_energy',
        ]
        self.ma_yi_kd = NamedFilter(urls, 'ma-yi-kd') 

        # 中青看点
        urls = [
            Api(r'getTimingRedReward.json', f_name='hourly_sign',log='时段签到'),
            r'webApi/AnswerReward/',
            Api(r'/v5/Game/GameVideoReward.json'),
            Api(r'/taskCenter/getAdVideoReward',log='任务中心 - 看视频'),
            Api(r'/WebApi/invite/openHourRed',log='开宝箱'),
            Api(r'/v5/article/complete.json',log='看视频得金币', f_b_enc={'p'}, f_b_arg={'p'}, content_type='urlencoded_form'),
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
            self.qtt_video,
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
        loader.add_option(
            name = 'session',
            typespec = str,
            default = 'default',
            help = '若接口不能推断出session,则用这值来设定默认值', 
        )

    def configure(self, updated):
        ctx.log.info('event: configure')
        if 'session' in updated:
            self.default_session = ctx.options.session

    def running(self):
        ctx.log.info('event: running')
        ctx.log.info('default session = ' + ctx.options.session)

    def done(self):
        print('event: done')
        try:
            # for _, host_headers in self.headers.items():
            #     for host, headers  in host_headers.items():
            #         self._delete_some_headers(headers)
            self._gen_file(self.headers, self.file_headers, self.file_dir)

            self._gen_file(self.params, self.file_params, self.file_dir)

            self._gen_file(self.bodys, self.file_bodys, self.file_dir)

            self._gen_file(self.params_keys, self.file_params_keys, self.file_dir)

            self._gen_file(self.bodys_keys, self.file_bodys_keys, self.file_dir)

            temp = {}
            for device, d in self.app_hosts.items():
                temp[device] = d.copy()
                for app, dd in d.items():
                    temp[device][app] = list(dd)
            self._gen_file(temp, self.file_app_hosts, self.file_dir)

            self._gen_file(self.app_fn_url, self.file_app_fn_url, self.file_dir)
            # -------------------------------------------------------

            print('session_hit')
            print(str(self.session_hit))
            def gen_app_data_to_file(data: dict, file_name):
                for device, app in self.session_hit:
                    try:
                        dd = data[device][app]
                        print(f"生成 App", end='\t')
                        self._gen_file(dd, f'{file_name}-{device}.json', f'{self.file_dir}{app}')
                    except:
                        pass

            # 生成app下的 data-bodys-keys.json, data-params-keys.json, data-fn-url.json 
            gen_app_data_to_file(self.bodys_keys, 'data-bodys-keys')
            gen_app_data_to_file(self.params_keys, 'data-params-keys')
            gen_app_data_to_file(self.app_fn_url, 'data-fn-url')
            gen_app_data_to_file(self.params_as_all, 'data-params_as_all')
            gen_app_data_to_file(self.bodys_as_all, 'data-bodys_as_all')

            sessions_by_app = {}
            # sessions_jinja_data = list()
            # 生成app下的 session_xxx.py
            for device, app in self.session_hit:
                sessions_jinja_data = sessions_by_app.setdefault(app, list())
                sessions_jinja_data.append({ 
                    'file': f'session_{device}',
                    'session': device,
                })


                var_dict = dict()

                def abc(data: dict, var_name, var_dict: dict, mergehost=True):
                    try:
                        dd = data[device][app]
                        merge_hosts = {}
                        try:
                            if mergehost:                            
                                for host, ddd in dd.items():
                                    merge_hosts.update(ddd)
                            else:
                                merge_hosts = dd
                        except:
                            merge_hosts = dd                            
                        var_dict[var_name] = json.dumps(merge_hosts, indent=2, sort_keys=True)
                        print(f"生成 App - {app:20} - session_{device}.py {var_name} 成功")
                    except Exception as e:
                        print(e)
                        var_dict[var_name] = '{}'

                abc(self.headers, 'header_values', var_dict)
                abc(self.app_fn_url, 'fn_url', var_dict)
                abc(self.params_keys, 'params_keys', var_dict, mergehost=False)
                abc(self.bodys_keys, 'bodys_keys', var_dict, mergehost=False)
                abc(self.params, 'param_values', var_dict)
                abc(self.bodys, 'body_values', var_dict)
                abc(self.params_as_all, 'params_as_all', var_dict)
                abc(self.bodys_as_all, 'bodys_as_all', var_dict)
                abc(self.params_encry, 'params_encry', var_dict)
                abc(self.bodys_encry, 'bodys_encry', var_dict)

                tfile = f'{self.template_dir}/session_xxx.j2.py'
                gfile = f'{self.file_dir}{app}/session_{device}.py'
                self.gen_file_from_jinja2(tfile, gfile, seq=var_dict)

            # 生成app下的 code.py, sessions.py
            for app, apis in self.app_apis.items():
                print(f'生成code - {app}')
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
            request: http.HTTPRequest = flow.request

            parse_result = urlparse(request.url)
            url_path = parse_result.path
            if api.url_path and (not api.url_path == url_path):
                api = Api(url_path)
                ft.add(api)

            ctx.log.error(f'api = {api}')

            function_name = re.sub(r'[./-]','_', url_path).strip('_').lower()
            api_url = f'{request.scheme}://{request.pretty_host}{url_path}' 
            headers_code = self.headers_string(flow)
            params_code = self.params_string(flow)
            data_code = self.data_string(flow, api) 

            path = pathlib.Path(f'{self.file_dir}{ft.app_name}')
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            with (path/f'{function_name}.text').open('a') as f:

                app_apis = self.app_apis.setdefault(ft.app_name, dict())
                if not function_name in app_apis:
                    api.name = function_name
                    api.url = api_url
                    api.url_path = url_path
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

                device = self._guess_device(flow, api)

                self.gather_params_and_bodys(flow, api, device=device, app=ft.app_name)
                self.session_hit.add((device, ft.app_name))

                d = self.inner_by_list(self.app_hosts, [device])
                app_hosts = d.setdefault(ft.app_name, set())
                app_hosts.add(request.pretty_host)

                d_v = self.app_fn_url.setdefault(device, dict())
                fn_url = d_v.setdefault(ft.app_name, dict())
                fn_url[url_path] = api_url



    def headers_string(self, flow: http.HTTPFlow, indent=1):
        d = dict(flow.request.headers)
        return 'headers = {'+json.dumps(d, indent='\t'*(indent+1)).strip('{}') + '\t}'


    def params_string(self, flow: http.HTTPFlow, indent=1):
        d = dict(flow.request.query)
        return 'params = {'+json.dumps(d, indent='\t'*(indent+1)).strip('{}') + '\t}'

    def data_string(self, flow: http.HTTPFlow, api: Api):
        lines = ''

        d = self.dict_from_request_body(flow, api)
        if d:
            for key, value in d.items():
                lines += f"\n\t\t'{key}': {value!r},"    
        
        s = f'''data = {{{lines}\n\t}}'''        
        return s

    def gather_params_and_bodys(self, flow: http.HTTPFlow, api: Api, device='', app=''):
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
        body_dict = self.dict_from_request_body(flow, api)
        if body_dict:
            d.update(body_dict)
            bodys_keys = list(body_dict.keys())

        parse_result = urlparse(request.url)
        fname = parse_result.path

        dd = self.inner(self.bodys_keys, device=device, app=app, host=host) 
        dd[fname] = bodys_keys

        d = self.inner(self.params_keys, device=device, app=app, host=host) 
        d[fname] = list(flow.request.query.keys())


        path = request.path

        d = self.inner(self.params_as_all, device=device, app=app, host=host)
        if api.params_as_all:
            if not api.name in d:
                d[api.name] = []
            d[api.name].append(dict(flow.request.query))

        d = self.inner(self.bodys_as_all, device=device, app=app, host=host)
        if api.body_as_all:
            if not api.name in d:
                d[api.name] = []
            d[api.name].append(dict(body_dict))
            ctx.log.error('self.bodys_as_all:')

        if api.f_p_enc and not api.params_as_all:
            d = self.inner_by_list(self.params_encry,[device, app, host, api.url_path])
            for k in api.f_p_enc:
                l = d.setdefault(k, list())
                l.append(flow.request.query[k])

        if api.f_b_enc and not api.body_as_all:
            d = self.inner_by_list(self.bodys_encry,[device, app, host, api.url_path])
            for k in api.f_b_enc:
                l = d.setdefault(k, list())
                l.append(body_dict[k])

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

        with (path/f).open(mode=mode) as fd:
            json.dump(o, fd, indent=2, sort_keys=True)
            print(f"生成 {f} 成功")

    def _guess_device(self, flow: http.HTTPFlow, api: Api):
        device = ''
        guess_by_data = ''
        request = flow.request

        def gass(data):
            nonlocal guess_by_data, device
            for k, v in data:
                if self.re_ios.search(v):
                    device = 'ios'
                    guess_by_data = v 
                    break

                if self.re_xiao.search(v):
                    device = 'xiaomi'
                    guess_by_data = v 
                    break            

                if self.re_huawei.search(v):
                    device = 'huawei'
                    guess_by_data = v 
                    break

        gass( itertools.chain(request.headers.items(), request.query.items()) )
        if not device:
            d = self.dict_from_request_body(flow, api)
            if d: 
                gass(d.items())
        
        ctx.log.error(f'device = {device}')
        ctx.log.error(f'guess = {guess_by_data}')
        if device == '':
            ctx.log.error(f"not guess: {request.url}")
            device = ctx.options.session
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

    def dict_from_request_body(self, flow: http.HTTPFlow, api: Api):
        d = None
        if api.content_type == 'json':
            try:
                d = json.loads(flow.request.text)
            except :
                pass

        elif api.content_type == 'urlencoded_form' or flow.request.urlencoded_form:
            # 返回的类型是 multidict.MultiDictView
            d = flow.request.urlencoded_form
            api.content_type = 'urlencoded_form'

        elif api.content_type == 'multipart_form' or flow.request.multipart_form:
            ctx.log.error('是multipart_form')
            d = dict()
            for key,value in flow.request.multipart_form.items():                
                key = key.decode(encoding='utf-8')
                value = value.decode(encoding='utf-8')
                d[key] = value
            api.content_type = 'multipart_form'

        elif api.content_type == 'get':
            pass

        else:
            # api.content_type没有决定出来：1,没有设置且第1次击中api；2,body没有内容也无法决定content_type；3,get请求一般没有body 

            if flow.request.text:
                ctx.log.error('有请求内容')
            else:
                ctx.log.error('没有请求内容')
                if flow.request.method == 'GET':
                    api.content_type = 'get'
                    return d

            try:
                d = json.loads(flow.request.text)
                api.content_type = 'json'
            except:
                pass

        return d        


addons = [
    GenCode()
]


if __name__ == "__main__":
    import shlex, subprocess


    print(__file__)
    # subprocess.Popen(['mitmdump', '-s', __file__])
    
    api =Api(r'/mission/intPointReward',params_as_all=False, body_as_all=False,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',f_name='hourly_sign', log='时段签到', params_as_all=False, body_as_all=False,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    # api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True)#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',f_p_enc={'p_enc'})
    print(api.str_fun_params())

    api.name = 'mission_intPointReward'
    api.method = 'post'
    api.content_type = 'json'
    api.fun_params = api.str_fun_params()
    # api.params_as_all = True
    # api.body_as_all = True
    seq = [api]  

    template_dir = os.path.dirname(__file__)
    tfile = f'{template_dir}/code_template.j2.py'
    # tfile = f'{template_dir}/api_template.j2.py'
    with open(tfile) as f:
        s = f.read()
        t = Template(s)
        ss = t.render(seq=seq)
        # ss = t.render(request=api)
        print(ss)

    print('done')
