__all__ = ['Api', 'App']

from mitmproxy import ctx, flowfilter, http


class Api(object):
    def __init__(
            self, 
            url, 
            f_name='', 
            log='', 
            api_ok={}, 
            f_merge_key=None, 
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
        self.url = url
        self.url_path = ''
        self.f_name = f_name
        self._name = ''
        self.log = log
        self.api_ok = api_ok
        self.f_merge_key = f_merge_key

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
    def __init__(self, urls, app_name='', api_ok={'code': 0}):
        self.app_name = app_name
        self.api_ok = dict()
        self.api_ok['app_ok'] = api_ok
        self.flts = dict()
        self.url_api_dict = dict()
        for u in urls:
            url = u
            if isinstance(u, Api):
                url = u.url
                if len(u.api_ok):
                    # Todu:
                    self.api_ok[url] = u.api_ok
                self.url_api_dict[url] = u.f_merge_key
            flt = flowfilter.parse(url)
            self.flts[flt] = u
        self.current_api = None

    def __call__(self, f):
        for flt, api in self.flts.items():
            if flt(f):
                if isinstance(api, str):
                    api = Api(api)
                    self.flts[flt] = api
                self.current_api = api
                # Todu
                # self.url_api_dict[] = api
                return True
        return False

    def add(self, api: Api):
        flt = flowfilter.parse(api.url)
        self.flts[flt] = api


    def merge_rules(self):
        return self.url_api_dict
