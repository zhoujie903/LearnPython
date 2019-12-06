import pathlib
import os.path
import json
import re
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
    def __init__(self, url, d=dict()):
        self.url = url
        self.d = d
        self.str_d = self._str_fun_params()

    def __str__(self):
        return f'Api(url={self.url}, d={self.d})'
    
    def _str_fun_params(self):
        s = ''
        for k,v in self.d.items():
            if v:
                s += f', {k}={v!r}'
            else:
                s += f', {k}'
        return s

    def str_fun_params(self):
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

        self.sep = '--'
        self.q_dict = 'q_dict'
        self.template_dir = os.path.dirname(__file__)
        self.file_dir = '/Users/zhoujie/Desktop/api/'
        self.file_params_keys = 'data-params-keys.json'
        self.file_bodys_keys = 'data-bodys-keys.json'
        self.file_all = 'data-all.json'
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
            r'sign/sign',
            r'/mission/intPointReward',#时段签到
            r'/content/readV2',
            r'/app/re/taskCenter/info/v1/get',
            # r'taskcenter/getListV2',#旧版本 tab页：任务
            r'api-coin-service.aiclk.com/coin/service',
            r'readtimer/report',
            r'motivateapp/mtvcallback',
            r'x/feed/getReward',#信息流 - 惊喜红包

            r'x/tree-game/',
            r'x/tree-game/left-plant-num',
            r'x/tree-game/plant-ok',
            r'x/tree-game/add-plant',
            r'x/tree-game/fertilizer/add',
            r'x/tree-game/fertilizer/use',
            r'x/tree-game/water-plants',
            r'x/tree-game/my-gift-box/draw-lottery',
            r'x/tree-game/my-gift-box/receive-prize',

            r'x/open/game',
            r'/api/Login',
            r'api/loginGame',
            r'api/qttAddCoin',
            r'api/AddCoin',# 成语

            r'/x/open/coin/add',#切菜
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
            r'article/treasure_chest',
            r'TaskCenter/daily_sign',
            # r'WebApi/',
            r'WebApi/Stage/task_reward',
            r'WapPage/get_video_status',
            r'article/complete_article',
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

            self._gen_file(self.bodys, self.file_bodys, self.file_dir)
            print(f"生成 {self.file_bodys} 成功")


            temp = self.can_not_create.copy()
            for body in temp.values():
                for key, value in body.items():
                    if isinstance(value, set):
                        body[key] = list(value)
            self._gen_file(temp, self.file_cannot, self.file_dir)
            print(f"生成 {self.file_cannot} 成功")


            all_data = self.params.copy()
            for device, d in all_data.items():
                for app, dd in d.items():
                    for host, ddd in dd.items():
                        ddd.update( self.inner(self.headers, device=device, app=app, host=host) )
                        ddd.update( self.inner(self.bodys, device=device, app=app, host=host) )
                
            self._gen_file(all_data, self.file_all, self.file_dir)
            print(f"生成 {self.file_all} 成功")

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
            for device, d in all_data.items():
                for app, dd in d.items():
                    merge_hosts = {}
                    for host, ddd in dd.items():
                        merge_hosts.update(ddd)
                    with open(f'{self.file_dir}{app}/session_{device}.py', mode='w') as f:
                        s = f'{self.q_dict} = ' + json.dumps(merge_hosts, indent=2, sort_keys=True)
                        f.write(s)
                        sessions_jinja_data = sessions_by_app.setdefault(app, list())
                        sessions_jinja_data.append({ 
                            'file': f'session_{device}',
                            'var': self.q_dict,
                            'session': device,
                        })

                        with open(f'{self.file_dir}{app}/data-params-keys-{device}.json') as ff:
                            t = json.load(ff)
                            s = f'params_keys = ' + json.dumps(t, indent=2, sort_keys=True)
                            f.write('\n\n') 
                            f.write(s)

                        with open(f'{self.file_dir}{app}/data-bodys-keys-{device}.json') as ff:
                            t = json.load(ff)
                            s = f'bodys_keys = ' + json.dumps(t, indent=2, sort_keys=True)
                            f.write('\n\n') 
                            f.write(s)

                        with open(f'{self.file_dir}{app}/data-fn-url-{device}.json') as ff:
                            t = json.load(ff)
                            s = f'fn_url = ' + json.dumps(t, indent=2, sort_keys=True)
                            f.write('\n\n') 
                            f.write(s)

                        # s = '\n\nq_dict.update(params_keys)\n\nq_dict.update(bodys_keys)\n\nq_dict.update(fn_url)'
                        # f.write(s)

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
                print(f'''# ---------------------''',file=f)

                code = f'''
def {function_name}(self):

    {headers_code}

    {params_code}

    {data_code}

    url = '{request.scheme}://{request.pretty_host}{url_path}'
    result = self._{request.method.lower()}(url, headers=headers, params=params, data=data)
    return result
                
'''
                f.write(code)

                # 
                code = f'''
def {function_name}(self):
    logging.info('')

    url = '{api_url}'

    params = self._params_from(url)

    {data_code}

    result = self._{request.method.lower()}(url, params=params, data=data)
    result = json.loads(result)
    return result
                

'''
                # f.write(code)                
                # 

                print(f'''Response:''',file=f)
                print(f'''{flow.response.text}''',file=f)
                print(f'''# ---------------------\n\n''',file=f)

                api: Api = ft.current_api
                ctx.log.error(f'api = {api}')
                device = self._guess_device(flow)

                self.gather_params_and_bodys(flow, device=device, app=ft.name)

                d = self.inner_by_list(self.app_hosts, [device])
                app_hosts = d.setdefault(ft.name, set())
                app_hosts.add(request.pretty_host)
                # ctx.log.error(str(self.app_hosts))

                app_apis = self.app_apis.setdefault(ft.name, dict())
                app_apis[function_name] = {
                    'name': function_name,
                    'url': api_url,
                    'method': request.method.lower(),
                    'content_type': 'json' if 'json' in request.headers.get('content-type','') else '',
                    'fun_params':api.str_fun_params(),
                }

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
        d = self.inner(self.bodys, device=device, app=app, host=host) 
        d.update(flow.request.urlencoded_form)
        d.update(flow.request.multipart_form)
        try:
            o = json.loads(flow.request.text)
            d.update(o)
        except :
            pass


        parse_result = urlparse(request.url)
        fname = parse_result.path

        d = self.inner(self.bodys_keys, device=device, app=app, host=host) 
        d[fname] = list(d.keys())        

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
        # print(tfile)
        # print(gfile)
        with open(tfile) as f:
            s = f.read()
            t = Template(s)
            ss = t.render(**kwargs)
            # print('xxxxxxxxxx')
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


addons = [
    GenCode()
]


if __name__ == "__main__":
    import shlex, subprocess


    print(__file__)
    # subprocess.Popen(['mitmdump', '-s', __file__])


    print('done')
