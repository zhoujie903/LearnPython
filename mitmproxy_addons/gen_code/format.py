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

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


def import_module(path: pathlib.Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(path.stem,str(path))
    session_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(session_module)
    return session_module

def get_data(session_module, var_name):
    old_data = dict()
    try:
        old_data = getattr(session_module, var_name)
    except Exception as e:
        # traceback.print_exc()
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
    

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))

def gen_file_from_jinja2(tfile, gfile, **kwargs):
    t = env.get_template(tfile)
    ss = t.render(**kwargs)
    with open(gfile, mode='w') as ff:
        ff.write(ss)

class AppSession():
    keys = [
        'header_values', 'fn_url', 
        'params_keys', 'bodys_keys', 
        'param_values', 'body_values', 
        'params_as_all', 'bodys_as_all',
        'params_encry', 'bodys_encry', 
    ]

    keys_level2 = [
        'params_keys', 'bodys_keys', 
        'params_encry', 'bodys_encry', 
    ]

    def __init__(self, path):
        self.file = path
        self.session_module = import_module(path)
        self.session_id = get_data(self.session_module, 'session_id')
        self.header_values = get_data(self.session_module, 'header_values')
        self.fn_url = get_data(self.session_module, 'fn_url')
        self.params_keys = get_data(self.session_module, 'params_keys')
        self.bodys_keys = get_data(self.session_module, 'bodys_keys')
        self.param_values = get_data(self.session_module, 'param_values')
        self.body_values = get_data(self.session_module, 'body_values')
        self.params_as_all = get_data(self.session_module, 'params_as_all')
        self.bodys_as_all = get_data(self.session_module, 'bodys_as_all')
        self.params_encry = get_data(self.session_module, 'params_encry')
        self.bodys_encry = get_data(self.session_module, 'bodys_encry')
        self.session_data = get_data(self.session_module, 'session_data')
        pass

    def format(self):
        remove_unnecessary_headers(self.header_values)
        remove_unnecessary_and_print_missing(self.param_values, self.params_keys)
        remove_unnecessary_and_print_missing(self.body_values, self.bodys_keys)

    def save_as_file(self, name='', inplace=False):
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


        tfile = f'session_xxx.j2.py'
        if inplace:
            gfile = self.file
        else:
            gfile = self.file.parent/f'session_{self.session_id}_{name}.py' 
        gen_file_from_jinja2(tfile, gfile, seq=var_dict)
        pass

class MergerSession():
    def __init__(self, from_session: AppSession, to_seession: AppSession):
        self.from_session = from_session
        self.to_seession = to_seession

    def merge(self):
        self.add_missing()

    def save_as_file(self, inplace=False):
        self.to_seession.save_as_file('merge', inplace=inplace)

    def add_missing(self):
        for k in AppSession.keys:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            add_missing(from_v, to_v)

        for k in AppSession.keys_level2:
            from_v = getattr(self.from_session, k)
            to_v = getattr(self.to_seession, k)
            add_missing_level2(from_v, to_v)


def main_merge_all(api_dir: str, dev_dir: str):
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



if __name__ == "__main__":
    
    file_name = 'session_huawei.py' 
    from_file = pathlib.Path(f'/Users/zhoujie/Desktop/api/qu-tou-tiao/session_xsy.py')
    from_session = AppSession(from_file)

    from_session.format()

    from_session.save_as_file('format', inplace=True)
    pass
