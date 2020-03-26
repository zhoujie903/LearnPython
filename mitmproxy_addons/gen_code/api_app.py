__all__ = ['Api', 'App']

from collections import OrderedDict
from typing import List, Tuple, Dict
from typing import Callable, Mapping, Optional, Sequence, Type, Union

from mitmproxy import flowfilter, http
from mitmproxy.flowfilter import TFilter


class Api(object):
    def __init__(
            self, 
            url: str, 
            f_name: str='', 
            log: str='', 
            api_ok: Mapping[str, Sequence[int or str]]={}, 
            f_merge_key: Callable=None, 
            params_as_all=False, 
            p_as_all_limit=50, 
            body_as_all=False, 
            f_p_enc: set = None, 
            f_b_enc: set = None, 
            f_p_arg: list = None, 
            f_b_arg: set = None, 
            f_p_kwarg: dict = None, 
            f_b_kwarg: dict = None, 
            content_type=''
        ):
        self.url = url if url[0] == '/' else '/'+url
        self.url_path = ''
        self.f_name = f_name
        self._name = ''
        self.log = log
        self.api_ok = api_ok
        self.f_merge_key: Callable = f_merge_key

        self.f_p_arg = f_p_arg
        self.f_p_enc = f_p_enc
        if f_p_enc:
            if self.f_p_arg == None:
                self.f_p_arg = list()
            self.f_p_arg.extend(f_p_enc)

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
        self.p_as_all_limit = p_as_all_limit
        self.str_d = ''
        # content_type取值'json', 'multipart_form', 'urlencoded_form', 'get'
        self.content_type = content_type

    def __str__(self):
        return f'{self.__class__.__name__}(url={self.url})'

    def _str_fun_params(self):
        s = ''
        if self.f_p_arg and not self.params_as_all:
            s += ", "
            s += ", ".join(self.f_p_arg)

        if self.f_b_arg and not self.body_as_all:
            s += ", "
            s += ", ".join(self.f_b_arg)

        if self.f_p_kwarg and not self.params_as_all:
            for k, v in self.f_p_kwarg.items():
                s += f', {k}={v!r}'

        if self.f_b_kwarg and not self.body_as_all:
            for k, v in self.f_b_kwarg.items():
                s += f', {k}={v!r}'

        if self.params_as_all:
            s += ', params_as_all'
        if self.body_as_all:
            s += ', body_as_all'
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


class App(object):
    def __init__(self, urls, app_name='', api_ok=[0], api_ok_key=['code']):
        self.app_name = app_name
        self.current_api = None
        self.api_ok = dict()
        self.api_ok['app_ok'] = api_ok
        self.api_ok['app_ok_key'] = api_ok_key
        self.flts: List[Tuple[TFilter, Api]] = []
        self.url_a_dict: Mapping[str, Union[str, Api]] = OrderedDict()
        for u in urls:
            if isinstance(u, Api):
                url = u.url
                self.url_a_dict[url] = u
                if len(u.api_ok):
                    self.api_ok[url] = u.api_ok

            elif isinstance(u, str):
                url = u if u[0] == '/' else '/' + u
                self.url_a_dict[url] = u

        self.__temp = list(self.url_a_dict.keys()) 

    def __call__(self, f: http.HTTPFlow):
        for flt, api in self.flts:
            if flt(f):
                self.current_api = api
                return True
        if len(self.__temp) == 0:
            # print('*'*100)
            return False

        for path in self.__temp:
            a = self.url_a_dict[path]
            r = f.request
            api = a
            if isinstance(a, str):
                api = Api(a)
            
            self.__temp.remove(path)
            flt = flowfilter.parse(api.url)
            self.flts.append((flt, api))

            if r.path.startswith(path):
                self.current_api = api
                return True
            
        return False

    def add(self, api: Api):
        flt = flowfilter.parse(api.url)
        self.flts.append((flt, api))


    def merge_rules(self) -> Dict[str, Callable[[list, list], list]]:
        url_api_dict = dict()
        for url, a in self.url_a_dict.items():
            if isinstance(a, Api):
                api: Api = a
                url_api_dict[url] = api.f_merge_key
        return url_api_dict
