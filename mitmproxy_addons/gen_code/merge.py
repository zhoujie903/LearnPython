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
from typing import List, Tuple, Dict
from typing import Callable, Mapping, Optional, Sequence, Type, Union

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

from api_app import Api, App

def import_module(path: pathlib.Path):
    import importlib.util
    try:
        spec = importlib.util.spec_from_file_location(path.stem,str(path))
        session_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(session_module)
        return session_module
    except Exception as e:
        logging.error(e)

    

def get_data(session_module, var_name):
    old_data = dict()
    try:
        old_data = getattr(session_module, var_name)
    except Exception as e:
        try:
            old_data = session_module[var_name]
        except:
            pass        
    return old_data

def remove_unnecessary_headers(headers):
    h = {
        ':authority', 'accept', 'accept-language', 'accept-encoding', 
        'connection', 'content-encoding', 'content-length', 'content-type', 'cache-control', 
        'host', 'pragma', 'proxy-connection',
    }
    for key in h:
        try:
            headers.pop(key.upper(), None)
            headers.pop(key.lower(), None)
            headers.pop(key.title(), None)
        except:
            pass

def remove_unnecessary_and_print_missing(exist_values, all_values):
    p_keys_all = set()
    for k, v in all_values.items():
        for kk, vv in v.items():
            p_keys_all |= set(vv)

    p_keys_exist = set(exist_values.keys())

    # 删除多余的值
    no_need_keys = p_keys_exist - p_keys_all
    for k in no_need_keys:
        del exist_values[k]

    # 打印缺失的值
    pprint.pprint('缺失：')
    pprint.pprint(p_keys_all - p_keys_exist)

def missing(p_keys_exist, p_keys_all) -> set:
    return set(p_keys_all - p_keys_exist)

def add_missing(from_values, to_values):
    p_keys_exist = set(from_values.keys())
    p_keys_all = set(to_values.keys())

    miss = missing(p_keys_all, p_keys_exist)
    for k in miss:
        to_values[k] = from_values[k]

def add_missing_level2(from_values, to_values):
    p_keys_exist = set(from_values.keys())
    p_keys_all = set(to_values.keys())

    common = p_keys_all & p_keys_exist
    for k in common:
        add_missing(from_values[k], to_values[k])

def update_values_level2(from_values, to_values):
    p_keys_exist = set(from_values.keys())
    p_keys_all = set(to_values.keys())    

    common = p_keys_all & p_keys_exist
    for k in common:
        to_values[k].update(from_values[k])

def merge_enc_level1(from_values, to_values, merge_rules:dict):
    for k, v in from_values.items():
        if merge_rules and merge_rules.get(k, None):
            merge = merge_rules[k]
            merged_data = merge(v, to_values.get(k, []))
            to_values[k] = merged_data

def merge_enc_level2(from_values, to_values, merge_rules:dict):
    for k, v in from_values.items():
        if merge_rules and merge_rules.get(k, None):
            merge = merge_rules[k]
            for kk,vv in v.items():
                a = to_values.setdefault(k, {})
                merged_data = merge(vv, a.get(kk, []))
                to_values[k][kk] = merged_data


def merge_app_ok(from_values, to_values, merge_rules:dict):
    for k, v in from_values.items():
        # k: 'app_ok','/path'
        # v: {'code':[0,200]}
        for kk, vv in v.items():
            # kk:'code'
            # vv:[0,200]
            a = to_values.setdefault(k, {})
            merge = merge_rules['app_ok']
            merged_data = merge(vv, a.get(kk, []))
            to_values[k][kk] = merged_data       

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))

def gen_file_from_jinja2(tfile, gfile, **kwargs):
    t = env.get_template(tfile)
    ss = t.render(**kwargs)
    print('生成文件: ', gfile)
    with open(gfile, mode='w') as ff:
        ff.write(ss)

class AppSession():
    keys = [
        'header_values', 'fn_url', 'api_ok', 
        'params_keys', 'bodys_keys', 
        'param_values', 'body_values', 
        'params_as_all', 'bodys_as_all',
        'params_encry', 'bodys_encry', 
    ]

    keys_level2 = [
        'params_keys', 'bodys_keys', 
        'params_encry', 'bodys_encry', 
    ]

    keys_u_level2 = [
        'params_keys', 'bodys_keys',  
    ]

    keys_u_level1 = [
        'header_values', 'fn_url', 'param_values', 'body_values',        
    ]

    keys_a_diff = [
        'fn_url', 'params_keys', 'bodys_keys', 'api_ok'
    ]

    keys_a_level2_diff = [
        'params_keys', 'bodys_keys',
    ]

    # 
    keys_enc_level1 = [
        'params_as_all', 'bodys_as_all',
    ]

    keys_enc_level2 = [
        'params_encry', 'bodys_encry',
    ]

    keys_app_ok = ['api_ok']

    def __init__(self, path_or_vardict):
        self.file = None
        o = {}
        if isinstance(path_or_vardict, str):
            self.file = pathlib.Path(path_or_vardict)

        if isinstance(path_or_vardict, pathlib.Path):
            self.file = path_or_vardict

        if isinstance(path_or_vardict, dict):
            o = path_or_vardict

        if (not self.file == None) and self.file.exists():
            self.session_module = import_module(self.file)
            o = self.session_module

        self.__set_memebers(o)

    def __set_memebers(self, o):
        self.session_id = get_data(o, 'session_id')
        self.api_ok = get_data(o, 'api_ok')
        self.header_values = get_data(o, 'header_values')
        self.fn_url = get_data(o, 'fn_url')
        self.params_keys = get_data(o, 'params_keys')
        self.bodys_keys = get_data(o, 'bodys_keys')
        self.param_values = get_data(o, 'param_values')
        self.body_values = get_data(o, 'body_values')
        self.params_as_all = get_data(o, 'params_as_all')
        self.bodys_as_all = get_data(o, 'bodys_as_all')
        self.params_encry = get_data(o, 'params_encry')
        self.bodys_encry = get_data(o, 'bodys_encry')
        self.session_data = get_data(o, 'session_data')

    def format(self):
        remove_unnecessary_headers(self.header_values)
        remove_unnecessary_and_print_missing(self.param_values, self.params_keys)
        remove_unnecessary_and_print_missing(self.body_values, self.bodys_keys)

    def delelte(self):
        '''
        fn_url中没有对应的URL时，删除params_keys, bodys_keys中对应的值
        '''
        u = {}
        for _, url in self.fn_url.items():
            o = urlparse(url)
            s = u.setdefault(o.netloc, set())
            s.add(o.path)

        uks = set(u.keys())
        for field in [self.params_keys, self.bodys_keys]:
            fks = set(field.keys())

            no_need_keys = fks - uks
            for k in no_need_keys:
                del field[k]

            common = fks & uks
            for netloc in common:
                pks = set(field[netloc].keys())
                hks = set(u[netloc]) 
                no_need_keys = pks - hks
                for k in no_need_keys:
                    del field[netloc][k]   



    def save_as_file(self, name='', path=None, inplace=False):
        var_dict = self.var_json_dict()
        tfile = f'session_xxx.j2.py'

        if path:
            gfile = path
        else:
            if inplace:
                gfile = self.file
            else:
                gfile = self.file.parent/f'session_{self.session_id}_{name}.py'

        if not gfile.parent.exists():
            gfile.parent.mkdir(parents=True, exist_ok=True)
        gen_file_from_jinja2(tfile, gfile, seq=var_dict)
        pass

    def var_json_dict(self):
        var_dict = dict()
        var_dict['session_id'] = f'{self.session_id!r}'

        var_dict['header_values'] = json.dumps(self.header_values, indent=2, sort_keys=True)
        var_dict['fn_url'] = json.dumps(self.fn_url, indent=2, sort_keys=True)
        var_dict['params_keys'] = json.dumps(self.params_keys, indent=2, sort_keys=True)
        var_dict['bodys_keys'] = json.dumps(self.bodys_keys, indent=2, sort_keys=True)
        var_dict['param_values'] = json.dumps(self.param_values, indent=2, sort_keys=True)
        var_dict['body_values'] = json.dumps(self.body_values, indent=2, sort_keys=True)
        var_dict['params_as_all'] = json.dumps(self.params_as_all, indent=2, sort_keys=True)
        var_dict['bodys_as_all'] = json.dumps(self.bodys_as_all, indent=2, sort_keys=True)
        var_dict['params_encry'] = json.dumps(self.params_encry, indent=2, sort_keys=True)
        var_dict['bodys_encry'] = json.dumps(self.bodys_encry, indent=2, sort_keys=True)
        var_dict['api_ok'] = json.dumps(self.api_ok, indent=2, sort_keys=True)

        return var_dict

    def var_dict(self):
        var_dict = dict()
        var_dict['session_id'] = self.session_id

        var_dict['header_values'] = self.header_values
        var_dict['fn_url'] = self.fn_url
        var_dict['params_keys'] = self.params_keys
        var_dict['bodys_keys'] = self.bodys_keys
        var_dict['param_values'] = self.param_values
        var_dict['body_values'] = self.body_values
        var_dict['params_as_all'] = self.params_as_all
        var_dict['bodys_as_all'] = self.bodys_as_all
        var_dict['params_encry'] = self.params_encry
        var_dict['bodys_encry'] = self.bodys_encry
        var_dict['api_ok'] = self.api_ok

        return var_dict

class MergerSession():
    def __init__(self, from_session: AppSession, to_seession: AppSession):
        self.from_session = from_session
        self.to_seession = to_seession

    def merge(self, o=('a','u'), merge_rules:dict =None):
        '''
        cuda:create, update, delete, append
        '''
        if 'u' in o:
            self.update_values()

        if 'a' in o:
            self.add_missing()

        self.merge_enc(merge_rules)
        self.merge_app_ok(merge_rules)

    def save_as_file(self, path=None, inplace=False):
        self.to_seession.save_as_file(name='merge', path=path, inplace=inplace)

    def add_missing(self):
        if self.to_seession.file.exists():
            if self.to_seession.session_id == self.from_session.session_id:
                level_1_keys, level_2_keys = AppSession.keys, AppSession.keys_level2
            else:
                level_1_keys, level_2_keys = AppSession.keys_a_diff, AppSession.keys_a_level2_diff

            self._add_missing(level_1_keys, level_2_keys)
        else:
            self.to_seession = AppSession(self.from_session.var_dict())
            self.to_seession.file = pathlib.Path(re.sub('/api/', '/dev/', str(self.from_session.file)))
            pass

    def _add_missing(self, level_1_keys, level_2_keys):
        for k in level_1_keys:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            add_missing(from_v, to_v)

        for k in level_2_keys:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            add_missing_level2(from_v, to_v)

    def update_values(self):
        for k in AppSession.keys_u_level1:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            to_v.update(from_v)

        for k in AppSession.keys_u_level2:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            update_values_level2(from_v, to_v)

    def merge_enc(self, app=None):
        for k in AppSession.keys_enc_level1:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            merge_enc_level1(from_v, to_v, app)

        for k in AppSession.keys_enc_level2:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            merge_enc_level2(from_v, to_v, app)

    def merge_app_ok(self, app=None):
        if app == None or app.get('app_ok',None) == None:
            from merge_rule import unique_rule
            r_u = unique_rule()
            app = {'app_ok':r_u}

        for k in AppSession.keys_app_ok:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            merge_app_ok(from_v, to_v, app)
            pass


def main_mitm_merge_to(from_path: str, merge_to: int):
    '''
    session文件合并 
    0: 不合并到其它文件, 
    1: 合并到Api文件夹的其它文件, 
    2: 合并到dev文件夹的同名文件, 
    3: 合并到dev文件夹的所有文件 
    '''
    if merge_to == 0:
        return

    if merge_to == 1:
        # Tudo:
        return

    if merge_to == 2:
        main_merge_to_same_session(from_path)

    if merge_to == 3:
        main_merge_new_added_apis(from_path)
        return


def main_merge_all(api_dir: str, dev_dir: str):
    '''
    场景：目录级内所有对应session合并
    '''

    api_dir = pathlib.Path(api_dir)
    dev_dir = pathlib.Path(dev_dir)

    r = re.compile(r'session_[a-zA-Z]+\.py')
    target = api_dir.glob(r'*/session_huawei.py')
    target = [item for item in target if r.match(item.name)] 
    for item in sorted(target):
        part_path = item.relative_to(api_dir)
        to_file: pathlib.Path = dev_dir / part_path
        if to_file.exists():
            print(part_path)
            from_session = AppSession(item)
            to_seession = AppSession(to_file)

            merge_tool = MergerSession(from_session, to_seession)
            merge_tool.merge()
            merge_tool.save_as_file() 


def main_merge_new_added_apis(from_path: str):
    '''
    场景：有新增的接口录入时
    操作：1. 合并到同名的session, 2. 并合并非同名session
    '''

    main_merge_to_same_session(from_path)

    # 2. 并合并非同名session
    main_merge_to_other_session(from_path)


def main_merge_to_same_session(from_path: str):
    '''
    场景：合并api文件夹到dev文件夹下的同名session
    '''
    from data_api_app import helper_app_from_path 
    sessions = helper_gen_from_and_to_appsessions(from_path)
    app = helper_app_from_path(from_path) 

    merge_tool = MergerSession(*sessions)
    merge_tool.merge(merge_rules=app.merge_rules())
    merge_tool.save_as_file(inplace=True)


def main_merge_to_other_session(from_path: str):
    '''
    场景：从一个session合并到其它session
    操作：只合并键，比如urls,params_keys,body_keys，不能合并值 
    '''

    from_file = pathlib.Path(from_path)
    name = from_file.name 

    if '/dev/' in from_path:
        folder = from_file.parent

    if '/api/' in from_path:
        temp = re.sub('/api/', '/dev/', from_path)
        folder = pathlib.Path(temp).parent 

    print(folder, name)

    from_session = AppSession(from_file)

    r = re.compile(r'session_[a-zA-Z]+\.py')
    target = folder.glob(r'session_*.py')
    target = [item for item in target if r.match(item.name)] 
    target = [item for item in target if not from_file.samefile(item)] 
    for item in sorted(target):
        print(f'{name} -> {item.name}')        
        to_seession = AppSession(item)

        merge_tool = MergerSession(from_session, to_seession)
        merge_tool.merge(o=('a'))
        merge_tool.save_as_file(inplace=True)    


def helper_gen_from_and_to_appsessions(from_or_to_path: str):
    if '/api/' in from_or_to_path:
        fp = from_or_to_path
        tp = re.sub('/api/', '/dev/', from_or_to_path)
    else:
        tp = from_or_to_path    
        fp = re.sub('/dev/', '/api/', from_or_to_path)
    
        
    from_file = pathlib.Path(fp)
    from_session = AppSession(from_file)

    to_file = pathlib.Path(tp)
    to_seession = AppSession(to_file)    

    return from_session, to_seession


def helper_all_sessions(api_dir: str) -> list:
    '''
    场景：目录级内所有对应session合并
    '''

    api_dir = pathlib.Path(api_dir)

    r = re.compile(r'session_[a-zA-Z]+\.py')
    target = api_dir.glob(r'*/session_*.py')
    target = [item for item in target if r.match(item.name)] 
    return sorted(target)



def test_merge_enc():
    from data_api_app import app_qu_tou_tiao, app_cai_dan_sp
    fs = AppSession('/Users/zhoujie/Desktop/test/api/qu-tou-tiao/session_huawei.py')
    ts = AppSession('/Users/zhoujie/Desktop/test/dev/qu-tou-tiao/session_huawei.py')
    app = app_qu_tou_tiao()

    fs = AppSession('/Users/zhoujie/Desktop/test/api/cai-dan-sp/session_huawei.py')
    ts = AppSession('/Users/zhoujie/Desktop/test/dev/cai-dan-sp/session_huawei.py')
    app = app_cai_dan_sp()

    merge_tool = MergerSession(fs, ts)
    merge_tool.merge(merge_rules=app.merge_rules())
    merge_tool.save_as_file()

if __name__ == "__main__":

    api_dir = '/Users/zhoujie/Desktop/api'
    dev_dir = '/Users/zhoujie/Desktop/dev'

    # test_merge_enc()
    # exit()

    # 场景：整理
    # targets = helper_all_sessions(api_dir)
    # for p in targets:
    #     path = pathlib.Path(p)
    #     session = AppSession(path)
    #     session.format()
    #     session.delelte()
    #     session.save_as_file(inplace=True)
    # exit()


    # 场景：删除
    # from_path = pathlib.Path('/Users/zhoujie/Documents/heroku/jason903/auto_app/qu-tou-tiao/session_xsy.py') 
    # from_session = AppSession(from_path)
    # from_session.delelte()
    # from_session.save_as_file()
    # exit()


    # from_path = pathlib.Path('/Users/zhoujie/Desktop/dev/qu-tou-tiao/session_xiaomi.py') 
    # from_session = AppSession(from_path)
    # d = {}
    # for k, url in from_session.fn_url.items():
    #     l = d.setdefault(url, list())
    #     l.append(k)
    # for url, v in d.items():
    #     if len(v) > 1:
    #         pprint.pprint(v)
    # exit()


    # 场景：全部合并
    # main_merge_all(api_dir, dev_dir)
    # exit()

    from_path = '/Users/zhoujie/Desktop/dev/you-xi-he-zi/session_xiaomi.py'

    # 场景：同名session从api同步到dev
    # main_merge_to_same_session(from_path)

    # 场景：不同session之间合并
    main_merge_to_other_session(from_path)

    print('done!!!')
