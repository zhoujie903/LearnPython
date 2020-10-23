#!/usr/bin/env python3
# coding=utf-8

'''
代码模板
'''
import asyncio
import json
import logging
import pathlib
import random
import re
import sys
import time
import traceback
from functools import partial
from urllib.parse import urlparse

import requests

from sessions import users
from same_hard import CommonUser, framework_main

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)


class User(CommonUser):
    def __init__(self, session_data: dict): 
        super().__init__(session_data)


    def _header(self):
        return {
            'User-Agent': self.headers['User-Agent'],
            'user-agent': self.headers['user-agent'],
            # 'Cookie':self.headers['Cookie'],
        }

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

    {%- if request.content_type == 'json' %}
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
    for item in user.bodys_as_all['{{ request.url_path }}']:
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

async def run(runner, user: User):
    tasks = [

    ]
    for t in tasks:
        runner.send(t)

if __name__ == "__main__":
    framework_main(run, genUsers())
