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

from sessions import users

logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m-%d %H:%M:%S', level=logging.INFO)

logging.info(sys.stdout.encoding)

class User(object):
    def __init__(self, session_data: tuple): 
        self.headers = session_data[0]
        self.params_keys = session_data[1]
        self.bodys_keys = session_data[2]
        self.urls = session_data[3]
        self.params = session_data[4]
        self.bodys = session_data[5]
        self.session = requests.Session()
        self.session.headers = self._header()

        # with (pathlib.Path(__file__).parent/'data-params-keys.json').open() as f:            
        #     self.keys = json.load(f)


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
    def {{ request.name }}(self{{ request.fun_params }}):
        logging.info('{{ request.name }}')

        url = self.urls['{{ request.name }}']

        params = self._params_from(url)

        data = self._bodys_from(url)

    {% if request.content_type == 'json' %}
        result = self._{{ request.method }}(url, params=params, json=data)
    {% else %}
        result = self._{{ request.method }}(url, params=params, data=data)
    {% endif %}
        result = json.loads(result)
        return result
{% endfor %}

def genUsers():
    for session_data in users:
        yield User(session_data)

if __name__ == "__main__":
    for user in genUsers():
        logging.info('\033[1;31m---------------------------\033[0m')    