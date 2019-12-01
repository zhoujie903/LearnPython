import pathlib
import json
import re
import pprint
from urllib.parse import urlparse

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy import http

from jinja2 import Template

'''
生成接口python代码
'''

class NamedFilter(object):
    def __init__(self, urls, name=''):
        self.name = name
        self.flt = flowfilter.parse('|'.join(urls))

    def __call__(self, f):
        return self.flt(f)

class GenCode(object):
    def __init__(self):
        ctx.log.info('__init__')
        # self._test_jinja2()

        self.file_dir = '/Users/zhoujie/Desktop/api/'
        self.file_params_keys = 'api_params_keys.text'
        self.file_all = 'api_all_data.text'
        self.file_headers = 'headers.text'
        self.file_params = 'params.text'
        self.file_bodys = 'bodys.text'
        self.file_cannot = 'can_not_create_data.text'

        self.headers = {}
        self.params = {}
        self.bodys = {}

        self.params_keys = {}
        # 不能伪造但可以重放的数据
        self.can_not_create = {
            r'task/timer_submit': {},
        }

        # app包含哪些hosts
        self.app_hosts = {}
        self.app_apis = {}
        try:
            with open(f'{self.file_dir}{self.file_cannot}', 'r') as f:
                self.can_not_create = json.load(f)
                ctx.log.info(f'load {self.file_cannot} success!') 
        except:
            pass

        try:
            with open(f'{self.file_dir}{self.file_params_keys}', 'r') as f:
                self.params_keys = json.load(f) 
                ctx.log.info(f'load {self.file_params_keys} success!') 
        except:
            pass

        try:
            with open(f'{self.file_dir}{self.file_headers}', 'r') as f:
                self.headers = json.load(f) 
                ctx.log.info(f'load {self.file_headers} success!') 
        except:
            pass

        try:
            with open(f'{self.file_dir}{self.file_params}', 'r') as f:
                self.params = json.load(f) 
                ctx.log.info(f'load {self.file_params} success!') 
        except:
            pass

        try:
            with open(f'{self.file_dir}{self.file_bodys}', 'r') as f:
                self.bodys = json.load(f)
                ctx.log.info(f'load {self.file_bodys} success!') 
        except:
            pass

 
        urls = [
            'score_task/v1/task/page_data/',
            'score_task/v1/task/sign_in/',
            'score_task/v1/task/open_treasure_box/',
            'score_task/v1/task/new_excitation_ad/',            
            'score_task/v1/task/get_read_bonus/',
            'score_task/v1/task/done_task/',
            'score_task/v1/landing/add_amount/',             
            'score_task/v1/user/profit_detail/',
            'score_task/v1/novel/bonus/', #读小说得金币
            'search/suggest/homepage_suggest/',
            'search/suggest/initial_page/',
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
            r'api/loginGame',
            r'api/qttAddCoin',
            r'api/AddCoin',# 成语
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

        self.flowfilters = [
            self.toutiao, 
            self.huoshan, 
            # self.qu_tou_tiao, 
            # self.hao_kan,
            # self.quan_ming,
            # self.ma_yi_kd,
            # self.dftt,
            # self.zhong_qin_kd,
            # self.cai_dan_sp,
            self.kai_xin_da_ti,
        ]      

    def load(self, loader):
        ctx.log.info('event: load')

    def configure(self, updated):
        ctx.log.info('event: configure')

    def running(self):
        ctx.log.info('event: running')

    def done(self):
        print('event: done')

        self._gen_file(self.params, self.file_params, self.file_dir)
        print(f"生成 {self.file_params} 成功")


        for host, headers  in self.headers.items():
            self._delete_some_headers(headers)
        self._gen_file(self.headers, self.file_headers, self.file_dir)
        print(f"生成 {self.file_headers} 成功")


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
        for host, dict_value in all_data.items():
            all_data[host].update(self.headers.get(host, {}))
            all_data[host].update(self.bodys.get(host, {}))
            
        self._gen_file(all_data, self.file_all, self.file_dir)
        print(f"生成 {self.file_all} 成功")

        print(self.app_hosts)
        for app, hosts in self.app_hosts.items():
            p_k = dict(); app_all_data = dict()
            for h in hosts:
                p_k[h] = self.params_keys.get(h, dict())
                # app_all_data[h] = all_data.get(h, dict())
                app_all_data.update(all_data.get(h, dict()))

            self._gen_file(p_k, self.file_params_keys, f'{self.file_dir}{app}')
            self._gen_file(app_all_data, self.file_all, f'{self.file_dir}{app}')


        self._gen_file(self.params_keys, self.file_params_keys, self.file_dir)
        print(f"生成 {self.file_params_keys} 成功")
    
        pprint.pprint(self.app_apis)
        for app, apis in self.app_apis.items():
            seq = apis.values()
            print(seq)
            self._test_jinja2(seq,app=app)

            tfile = f'{self.file_dir}users.j2.py'
            gfile = f'{self.file_dir}{app}/users.py'
            self.gen_file_from_jinja2(tfile,gfile)

            path = f'{self.file_dir}{app}/{self.file_all}'
            with open(path) as f:
                s = 'q_dict = ' + f.read()
                with open(f'{self.file_dir}{app}/ios.py', mode='w') as ff:
                    ff.write(s)

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

    url = '{request.scheme}://{request.pretty_host}{url_path}'

    params = self._params_from(url)

    {data_code}

    result = self._{request.method.lower()}(url, params=params, data=data)
    result = json.loads(result)
    return result
                

'''
                f.write(code)                
                # 

                print(f'''Response:''',file=f)
                print(f'''{flow.response.text}''',file=f)
                print(f'''# ---------------------\n\n''',file=f)

                self.gather_params_and_bodys(flow)
                self.gather_keys(flow)

                app_hosts = self.app_hosts.setdefault(ft.name,set())
                app_hosts.add(request.pretty_host)

                app_apis = self.app_apis.setdefault(ft.name, dict())
                app_apis[function_name] = {
                    'name': function_name,
                    'url': f'{request.scheme}://{request.pretty_host}{url_path}',
                    'method': request.method.lower(),
                    'content_type': 'json' if 'json' in request.headers.get('content-type','') else '',
                }


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

    def gather_params_and_bodys(self, flow: http.HTTPFlow): 
        request: http.HTTPRequest = flow.request

        # 收集params
        host_key = self.params.setdefault(request.pretty_host,dict())
        host_key.update(flow.request.query)

        # 收集headers
        host_key = self.headers.setdefault(request.pretty_host,dict())
        host_key.update(flow.request.headers)

        host_key = self.bodys.setdefault(request.pretty_host,dict())
        host_key.update(flow.request.urlencoded_form)
        host_key.update(flow.request.multipart_form)
        try:
            d = json.loads(flow.request.text)
            host_key.updated(d)
        except :
            pass

        # pprint.pprint(self.params)

        # pprint.pprint(self.headers)

        path = request.path
        for item in self.can_not_create.keys():
            if item in path:
                ctx.log.error(f'hit path {path}')
                d = self.can_not_create[item]
                body = json.loads(flow.request.text)
                for key, value in body.items():
                    values = d.setdefault(key, set())
                    values.add(value)
                # pprint.pprint(self.can_not_create)



    def gather_keys(self, flow: http.HTTPFlow): 
        request: http.HTTPRequest = flow.request
        host_key = self.params_keys.setdefault(request.pretty_host,dict())
        parse_result = urlparse(request.url)
        url_path = parse_result.path
        fname = url_path
        host_key[fname] = list(flow.request.query.keys())
        # pprint.pprint(self.params_keys)


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

    def _test_jinja2(self, seq, app=''):
        with open(f'{self.file_dir}code_template.j2.py') as f:
            s = f.read()
            t = Template(s)
            # seq = [
            #     {
            #         'name': 'login',
            #         'url': 'https://baidu.com',
            #         'method': 'post',
            #         'content_type': 'json',

            #     },
            #     {
            #         'name': 'main',
            #         'url': 'https://tent.com',
            #         'method': 'get',
            #         'content_type': 'form',

            #     }
            # ]
            ss = t.render(seq=seq)
            path = f'{self.file_dir}{app}/code-{app}.py'
            with open(path, mode='w') as ff:
                ff.write(ss)

    def gen_file_from_jinja2(self, tfile, gfile, **kwargs):
        print(tfile)
        print(gfile)
        with open(tfile) as f:
            s = f.read()
            t = Template(s)
            ss = t.render(**kwargs)
            print('xxxxxxxxxx')
            with open(gfile, mode='w') as ff:
                ff.write(ss)

addons = [
    GenCode()
]


if __name__ == "__main__":
    import shlex, subprocess


    print(__file__)
    # subprocess.Popen(['mitmdump', '-s', __file__])


    print('done')
