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

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))

def gen_file_from_jinja2(tfile, gfile, **kwargs):
    t = env.get_template(tfile)
    ss = t.render(**kwargs)
    with open(gfile, mode='w') as ff:
        ff.write(ss)

if __name__ == "__main__":
    
    from_file = pathlib.Path('/Users/zhoujie/Desktop/dev/qu-jian-pan/session_ios.py')

    session_module = import_module(from_file)

    session_id = get_data(session_module, 'session_id')
    header_values = get_data(session_module, 'header_values')
    fn_url = get_data(session_module, 'fn_url')
    params_keys = get_data(session_module, 'params_keys')
    bodys_keys = get_data(session_module, 'bodys_keys')
    param_values = get_data(session_module, 'param_values')
    body_values = get_data(session_module, 'body_values')
    params_as_all = get_data(session_module, 'params_as_all')
    bodys_as_all = get_data(session_module, 'bodys_as_all')
    params_encry = get_data(session_module, 'params_encry')
    bodys_encry = get_data(session_module, 'bodys_encry')
    session_data = get_data(session_module, 'session_data')

    # -----------------------------
    remove_unnecessary_headers(header_values)
    remove_unnecessary_and_print_missing(param_values, params_keys)
    remove_unnecessary_and_print_missing(body_values, bodys_keys)
    # -----------------------------

    # exist = set(['1', '2', '3'])
    # alls = set(['1', '3', '4'])

    # pprint.pprint('缺失：')
    # pprint.pprint(alls - exist)

    # pprint.pprint('多余：')
    # pprint.pprint(exist - alls)

    # pprint.pprint('删除多余：')
    # exist &= alls
    # pprint.pprint(exist)

    # pprint.pprint('增加缺失：')
    # exist |= alls
    # pprint.pprint(exist)

    
    # exist ^= alls
    # pprint.pprint(exist)

    # alls ^= exist
    # pprint.pprint(alls)

    # -----------------------------


    var_dict = dict()
    var_dict['session_id'] = f'{session_id!r}'

    var_dict['header_values'] = json.dumps(header_values, indent=2, sort_keys=True)
    var_dict['fn_url'] = json.dumps(fn_url, indent=2, sort_keys=True)
    var_dict['params_keys'] = json.dumps(params_keys, indent=2, sort_keys=True)
    var_dict['bodys_keys'] = json.dumps(bodys_keys, indent=2, sort_keys=True)
    var_dict['param_values'] = json.dumps(param_values, indent=2, sort_keys=True)
    var_dict['body_values'] = json.dumps(body_values, indent=2, sort_keys=True)
    var_dict['params_as_all'] = json.dumps(params_as_all, indent=2, sort_keys=True)
    var_dict['bodys_as_all'] = json.dumps(bodys_as_all, indent=2, sort_keys=True)
    var_dict['params_encry'] = json.dumps(params_encry, indent=2, sort_keys=True)
    var_dict['bodys_encry'] = json.dumps(bodys_encry, indent=2, sort_keys=True)


    tfile = f'session_xxx.j2.py'
    gfile = from_file.parent/f'session_{session_id}_format.py' 
    gen_file_from_jinja2(tfile, gfile, seq=var_dict)
    pass
