#!/usr/bin/env python3
# coding=utf-8

'''
代码模板
'''

import requests
import re
import time
import json
import sys
import logging
import random
import pathlib
from urllib.parse import urlparse
import traceback

from sessions import users

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)

logging.info(sys.stdout.encoding)

class User(object):
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
        self.session = requests.Session()
        self.session.headers = self._header()


    def _header(self):
        return {
            # 'Host': '',
            # 'Accept': 'application/json',
            'User-Agent': self.headers['User-Agent'],
            'user-agent': self.headers['user-agent'],
            # 'Cookie':self.headers['Cookie'],
        }

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
        result = res.text
        try:
            p(json.loads(result))
        except :
            p(result) 
        logging.info('')
        return result

    def _get(self, url, p=logging.warning, **kwargs):
        res = self.session.get(url, **kwargs)
        result = res.text
        try:
            p(json.loads(result))
        except :
            p(result)        
        logging.info('')
        return result

    def _params_from(self, url):
        parse_result = urlparse(url)
        host = parse_result.netloc
        path = parse_result.path
        params_keys = self.params_keys[host][path]
        return { k:v for k,v in self.params.items() if k in set(params_keys) }

    def _bodys_from(self, url):
        parse_result = urlparse(url)
        host = parse_result.netloc
        path = parse_result.path
        params_keys = self.bodys_keys[host][path]
        return { k:v for k,v in self.bodys.items() if k in set(params_keys) }

{% for request in seq %}
    def {{ request.f_name }}(self{{ request.fun_params }}):
    {%- if request.log %}
        logging.info('{{ request.log }}')
    {%- else %}
        logging.info('{{ request.f_name }}')
    {%- endif %}

        url = self.urls['{{ request.url_path }}']

        params = self._params_from(url)
    {%- if request.f_p_arg %}
    {%- for k in request.f_p_arg %}
        params['{{ k }}'] = {{ k }} 
    {%- endfor %}
    {%- endif %}

    {%- if request.f_p_kwarg %}
    {%- for k in request.f_p_kwarg %}
        params['{{ k }}'] = {{ k }} 
    {%- endfor %}
    {%- endif %}

    {%- if request.params_as_all %}
        params = params_as_all
    {%- endif %}

        data = self._bodys_from(url)
    {%- if request.f_b_arg %}
    {%- for k in request.f_b_arg %}
        data['{{ k }}'] = {{ k }} 
    {%- endfor %}
    {%- endif %}

    {%- if request.f_b_kwarg %}
    {%- for k in request.f_b_kwarg %}
        data['{{ k }}'] = {{ k }} 
    {%- endfor %}
    {%- endif %}

    {%- if request.body_as_all %}
        data = body_as_all
    {%- endif %}

    {% if request.content_type == 'json' %}
        result = self._{{ request.method }}(url, params=params, json=data)
    {% else %}
        result = self._{{ request.method }}(url, params=params, data=data)
    {% endif %}
        result = json.loads(result)
        return result
{% endfor %}


{% for request in seq %}
{%- if request.params_as_all and not request.body_as_all %}
def {{ request.f_name }}(user: User):
    for item in user.params_as_all['{{ request.url_path }}']:
        user.{{ request.name }}(item)
{%- endif %}

{%- if request.body_as_all and not request.params_as_all %}
def {{ request.f_name }}(user: User):
    for item in user.body_as_all['{{ request.url_path }}']:
        user.{{ request.name }}(item)
{%- endif %}

{%- if request.f_p_enc  and not request.params_as_all %}
def {{ request.f_name }}(user: User):
    for item in user.params_encry['{{ request.url_path }}']['{{ request.f_p_enc|first }}']:
        user.{{ request.name }}(item)
{%- endif %}

{%- if request.f_b_enc and not request.body_as_all %}
def {{ request.f_name }}(user: User):
    for item in user.bodys_encry['{{ request.url_path }}']['{{ request.f_b_enc|first }}']:
        user.{{ request.name }}(item)
{%- endif %}
{% endfor %}


def genUsers():
    for session_data in users:
        yield User(session_data)

if __name__ == "__main__":
    for user in genUsers():
        logging.info('\033[1;31m---------------------------\033[0m')
        try:
            pass
        except Exception as e:
            traceback.print_exc()    