import pathlib
import os.path
import json
import re
import time
import pprint
from urllib.parse import urlparse
import logging
import itertools
import collections
import importlib
import traceback

from mitmproxy import ctx, flowfilter, http

from jinja2 import Template, Environment, FileSystemLoader
from merge import *
from api_app import Api, App
from data_api_app import apps

'''
生成接口python代码
mitmdump -q --flow-detail 0 --set session='huawei' -s "/Users/zhoujie/Documents/zhoujie903/LearnScrapy/mitmproxy_addons/gen_code/gen_code_mitm.py" 
'''

class GenCode(object):
    def __init__(self):
        ctx.log.info('__init__')
        # 设置代码文件生成的目录\文件夹
        self.api_dir = pathlib.Path('/Users/zhoujie/Desktop/api/')
        self.guess_session = collections.OrderedDict(
            ios=re.compile(r'iphone|ios', flags=re.IGNORECASE),
            xiaomi=re.compile(r'xiaomi|mi\+5|miui', flags=re.IGNORECASE),
            huawei=re.compile(r'huawei', flags=re.IGNORECASE),
        )

        self.env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
        self.api_template = self.env.get_template('api_template.j2.py')

        self.headers = {}
        self.params = {}
        self.bodys = {}

        self.params_keys = {}
        self.params_encry = {}
        self.bodys_keys = {}
        self.bodys_encry = {}
        self.params_as_all = dict()
        self.params_as_all_limit = dict()
        self.bodys_as_all = {}

        self.app_apis = {}
        self.app_fn_url = {}
        self.session_hit = set()

        self.appfilters = apps()
        

    def load(self, loader):
        ctx.log.info('event: load')
        loader.add_option(
            name='guess_as_session',
            typespec=str,
            default='default',
            help='若接口不能推断出session,则用这值来设定默认值',
        )

        loader.add_option(
            name='session',
            typespec=str,
            default='',
            help='指定session的值, 不用代码推断',
        )

        loader.add_option(
            "mergeto", int, 0,
            """
            session文件合并 
            0: 不合并到其它文件, 
            1: 合并到Api文件夹的其它文件, 
            2: 合并到dev文件夹的同名文件, 
            3: 合并到dev文件夹的所有文件 
            """
        )

    def configure(self, updated):
        ctx.log.info('event: configure')

    def running(self):
        ctx.log.info('event: running')
        ctx.log.error('session = ' + ctx.options.session)
        ctx.log.error('guess-as-session = ' + ctx.options.guess_as_session)

    def done(self):
        print('event: done')
        try:
            print('session_hit')
            print(str(self.session_hit))

            sessions_by_app = {}
            # 生成app下的 session_xxx.py
            for device, app in self.session_hit:
                app_filter: App = None
                for item in self.appfilters:
                    if item.app_name == app:
                        app_filter = item
                        break

                sessions_jinja_data = sessions_by_app.setdefault(app, list())
                sessions_jinja_data.append({
                    'file': f'session_{device}',
                    'session': device,
                })

                hosts = self.headers[device][app]
                for _, d in hosts.items():
                    remove_unnecessary_headers(d)


                var_dict = dict()
                var_dict['session_id'] = device 
                var_dict['api_ok'] = app_filter.api_ok

                def abc(data: dict, var_name, var_dict: dict, mergehost=True):
                    try:
                        dd = data[device][app]
                        merge_hosts = {}
                        try:
                            if mergehost:
                                for _, ddd in dd.items():
                                    merge_hosts.update(ddd)
                            else:
                                merge_hosts = dd
                        except:
                            merge_hosts = dd
                        var_dict[var_name] = merge_hosts
                        print(f"生成 App - {app:20} - session_{device}.py {var_name} 成功")
                    except Exception as e:
                        # traceback.print_exc()
                        print(e)
                        var_dict[var_name] = {}
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

                session_xxx_py = self.api_dir.joinpath(app, f'session_{device}.py') 
                from_session = AppSession(var_dict)
                to_session = AppSession(session_xxx_py)

                merge_tool = MergerSession(from_session, to_session)
                merge_tool.merge(merge_rules=app_filter.merge_rules())
                merge_tool.save_as_file(path=session_xxx_py)

                # ----------- 报告 - 加密数据未采集 ----------- #
                need_ = set()
                for _, api in app_filter.flts:
                    if isinstance(api, Api):
                        to_session: AppSession = merge_tool.to_seession
                        url_path = api.url_path if api.url_path else api.url
                        if api.f_p_enc and (url_path not in to_session.params_encry):
                            need_.add((url_path, api.log))

                        if api.f_b_enc and (url_path not in to_session.bodys_encry):
                            need_.add((url_path, api.log))

                        if api.params_as_all and (url_path not in to_session.params_as_all):
                            need_.add((url_path, api.log))

                        if api.body_as_all and (url_path not in to_session.bodys_as_all):
                            need_.add((url_path, api.log))
                pprint.pprint(f'{device} - 下列Api需要采集')
                pprint.pprint(need_)
                # ----------- 报告 - 加密数据未采集 ----------- #

                main_mitm_merge_to(str(session_xxx_py), ctx.options.mergeto)


            # 生成app下的 code.py, sessions.py
            for app, apis in self.app_apis.items():
                print(f'生成code - {app}')
                seq = apis.values()

                tfile = f'code_template.j2.py'
                gfile = self.api_dir.joinpath(app, f'code-{app}.py')
                self.gen_file_from_jinja2(tfile, gfile, seq=seq)

                tfile = f'sessions.j2.py'
                gfile = self.api_dir.joinpath(app, 'sessions.py')
                self.gen_file_from_jinja2(tfile, gfile, seq=sessions_by_app[app])

            print('done !!!')
        except Exception as e:
            logging.error('有异常：')
            traceback.print_exc()

    def response(self, flow: http.HTTPFlow):
        # 不处理'options'方法的请求
        method = flow.request.method.lower()
        if method == 'OPTIONS':
            return 

        ft = None
        for i, flt in enumerate(self.appfilters):
            if flt(flow):
                ft = flt
                if not flt == self.appfilters[0]:
                    self.appfilters.pop(i)
                    self.appfilters.insert(0, flt)
                break
        if ft:
            ctx.log.error('|' + '-'*20 + '|') 
            api: Api = ft.current_api
            request: http.HTTPRequest = flow.request

            parse_result = urlparse(request.url)
            url_path = parse_result.path
            if api.url_path and (not api.url_path == url_path):
                api = Api(url_path)
                ft.add(api)

            if len(api.api_ok):
                ft.api_ok[url_path] = api.api_ok

            ctx.log.error(f'触发 App = {ft.app_name}')
            ctx.log.error(f'触发 api = {api} {request.method}')

            function_name = re.sub(r'[./-]', '_', url_path).strip('_').lower()
            api_url = f'{request.scheme}://{request.pretty_host}{url_path}'
            headers_code = self.headers_string(flow)
            params_code = self.params_string(flow)
            data_code = self.data_string(flow, api)

            path = self.api_dir.joinpath(ft.app_name) 
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            with (path/f'{function_name}.text').open('a') as f:

                app_apis = self.app_apis.setdefault(ft.app_name, dict())
                if function_name not in app_apis:
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

                device = self._guess_session(flow, api)

                self.gather_params_and_bodys(flow, api, device=device, app=ft.app_name)
                self.session_hit.add((device, ft.app_name))

                d_v = self.app_fn_url.setdefault(device, dict())
                fn_url = d_v.setdefault(ft.app_name, dict())
                fn_url[url_path] = api_url

            ctx.log.error('|' + '-'*20 + '|')

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

        host = request.pretty_host

        # 收集headers
        d = inner(self.headers, device=device, app=app, host=host)
        d.update(flow.request.headers)

        # 收集params
        d = inner(self.params, device=device, app=app, host=host)
        d.update(flow.request.query)

        # 收集bodys
        bodys_keys = list()
        d = inner(self.bodys, device=device, app=app, host=host)
        body_dict = self.dict_from_request_body(flow, api)
        if body_dict:
            d.update(body_dict)
            bodys_keys = list(body_dict.keys())

        parse_result = urlparse(request.url)
        fname = parse_result.path

        dd = inner(self.bodys_keys, device=device, app=app, host=host)
        dd[fname] = bodys_keys

        d = inner(self.params_keys, device=device, app=app, host=host)
        d[fname] = list(flow.request.query.keys())


        d = inner(self.params_as_all, device=device, app=app, host=host)
        limit = inner_by_list(self.params_as_all_limit, [device, app])
        if api.params_as_all:
            if not api.url_path in d:
                d[api.url_path] = []
                limit[api.url_path] = api.p_as_all_limit
            if api.p_as_all_limit > len(d[api.url_path]):
                d[api.url_path].append(dict(flow.request.query))

        d = inner(self.bodys_as_all, device=device, app=app, host=host)
        if api.body_as_all:
            if not api.url_path in d:
                d[api.url_path] = []
            d[api.url_path].append(dict(body_dict))

        if api.f_p_enc and not api.params_as_all:
            d = inner_by_list(self.params_encry,[device, app, host, api.url_path])
            for k in api.f_p_enc:
                l = d.setdefault(k, list())
                l.append(flow.request.query[k])

        if api.f_b_enc and not api.body_as_all:
            d = inner_by_list(self.bodys_encry,[device, app, host, api.url_path])
            for k in api.f_b_enc:
                l = d.setdefault(k, list())
                l.append(body_dict[k])

    def _gen_file(self, o, f, fold, mode='w'):
        path = fold#pathlib.Path(fold)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        with (path/f).open(mode=mode) as fd:
            json.dump(o, fd, indent=2, sort_keys=True)
            print(f"生成 {f} 成功")

    def _guess_session(self, flow: http.HTTPFlow, api: Api):
        session = ''
        guess_by_data = ''
        request = flow.request

        if ctx.options.session:
            session = ctx.options.session
            ctx.log.error(f'指定为：session = {session}')
            return session

        def guess(data):
            nonlocal guess_by_data, session
            found = False
            for k, v in data:
                for s, r in self.guess_session.items():
                    if r.search(v):
                        session = s
                        guess_by_data = v
                        found = True
                        break
                if found:
                    break

        guess(itertools.chain(request.headers.items(), request.query.items()))
        if not session:
            d = self.dict_from_request_body(flow, api)
            if d:
                guess(d.items())

        ctx.log.error(f'依据值：{guess_by_data}')
        ctx.log.error(f'猜测为：session = {session}')
        if session == '':
            ctx.log.error(f"not guess: {request.url}")
            session = ctx.options.guess_as_session
        return session

    def gen_file_from_jinja2(self, tfile, gfile, **kwargs):
        t = self.env.get_template(tfile)
        ss = t.render(**kwargs)
        with open(gfile, mode='w') as ff:
            ff.write(ss)

    def dict_from_request_body(self, flow: http.HTTPFlow, api: Api):
        d = None
        if api.content_type == 'json':
            try:
                d = json.loads(flow.request.text)
            except:
                pass

        elif api.content_type == 'urlencoded_form' or flow.request.urlencoded_form:
            # 返回的类型是 multidict.MultiDictView
            d = flow.request.urlencoded_form
            api.content_type = 'urlencoded_form'

        elif api.content_type == 'multipart_form' or flow.request.multipart_form:
            ctx.log.error('content-type = multipart_form')
            d = dict()
            for key, value in flow.request.multipart_form.items():
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

if not __name__ == "__main__": 
    addons = [
        GenCode()
    ]



def inner(d, device='', app='', host=''):
    d = d.setdefault(device, dict())
    d = d.setdefault(app, dict())
    d = d.setdefault(host, dict())
    return d

def inner_by_list(d, l: list):
    for key in l:
        d = d.setdefault(key, dict())
    return d


def test_jinja():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    t = env.get_template('code_template.j2.py')

    api = Api(r'/mission/intPointReward', f_p_enc={'p_enc'})
    seq = [api]
    code = t.render(seq=seq)
    print(code)

if __name__ == "__main__":
    import shlex
    import subprocess

    test_jinja()
    

    api =Api(r'/mission/intPointReward',params_as_all=False, body_as_all=False,f_p_arg=['p1','p2'], f_b_arg={'b1', 'b2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',f_name='hourly_sign', log='时段签到', params_as_all=False, body_as_all=False,f_p_arg=['p1','p2'], f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    # api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True,f_p_arg=['p1','p2'], f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True)#时段签到
    print(api.str_fun_params())
    api = Api(r'/mission/intPointReward', f_p_enc={'p_enc'})
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
        # print(ss)
    print('done')
