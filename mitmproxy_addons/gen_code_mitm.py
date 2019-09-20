import json
import re
from urllib.parse import urlparse

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy import http

'''
生成接口python代码
'''

class GenCode(object):
    def __init__(self):
        ctx.log.info('__init__')

        # 今日头条 - 
        urls = [
            'score_task/v1/task/page_data/',
            'score_task/v1/task/sign_in/',
            'score_task/v1/task/open_treasure_box/',
            'score_task/v1/task/new_excitation_ad/',            
            'score_task/v1/task/get_read_bonus/',
            'score_task/v1/task/done_task/',
            'score_task/v1/landing/add_amount/',             
            'search/suggest/homepage_suggest/',
            'search/suggest/initial_page/',
            'api/news/feed/v47/',#安卓视频tab页
            'api/news/feed/v64/',#ios视频tab页
            'api/search/content/',           
        ]
        self.toutiao = flowfilter.parse('|'.join(urls))

        # 火山极速版
        urls = [
            'luckycat/v1/task/page/',
            'luckycat/v1/task/sign_in/',
            'luckycat/v1/task/open_treasure_box/',
            'luckycat/v1/task/done_task/',
            'luckycat/v1/landing/add_amount/',
            'luckycat/v1/task/get_read_bonus/',            
        ]
        self.huoshan = flowfilter.parse('|'.join(urls))

        # 趣头条
        urls = [
            r'taskcenter/getListV2',
            r'api-coin-service.aiclk.com/coin/service',
            r'readtimer/report',
            r'motivateapp/mtvcallback',

            r'x/tree-game/',
            r'x/tree-game/left-plant-num',
            r'x/tree-game/plant-ok',
            r'x/tree-game/add-plant',
            r'x/tree-game/fertilizer/add',
            r'x/tree-game/fertilizer/use',
            r'x/tree-game/water-plants',
            r'x/tree-game/my-gift-box/draw-lottery',
            r'x/tree-game/my-gift-box/receive-prize',
        ]
        self.qu_tou_tiao = flowfilter.parse('|'.join(urls)) 

        # 百度 - 好看
        urls = [
            r'activity/acusercheckin', # 每日签到
            r'signIn/new/sign', # 游戏中心签到
            r'activity/acad/rewardad', #看视频
            r'api/task/1/task/379/complete', #看视频
        ]
        self.hao_kan = flowfilter.parse('|'.join(urls)) 

        self.flowfilters = [
            self.toutiao, 
            self.huoshan, 
            self.qu_tou_tiao, 
            self.hao_kan
        ]      

    def load(self, loader):
        ctx.log.info('event: load')

    def configure(self, updated):
        ctx.log.info('event: configure')

    def running(self):
        ctx.log.info('event: running')

    def done(self):
        ctx.log.info('event: done')



    def response(self, flow: http.HTTPFlow):
        if any( [ filter(flow) for filter in self.flowfilters ] ):

            request: http.HTTPRequest = flow.request

            parse_result = urlparse(request.url)
            url_path = parse_result.path

            function_name = re.sub(r'[/-]','_', url_path).strip('_')
            headers_code = self.headers_string(flow)
            params_code = self.params_string(flow)
            data_code = self.data_string(flow) 

            path = f'''/Users/zhoujie/Desktop/api/{function_name}.text'''  
            with open(path, 'a') as f:
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

                print(f'''Response:''',file=f)
                print(f'''{flow.response.text}''',file=f)
                print(f'''# ---------------------\n\n''',file=f)

    def headers_string(self, flow: http.HTTPFlow):
        lines = ''
        for key,value in flow.request.headers.items():
            lines += f"\n\t\t'{key}': '{value}',"
        s = f'''headers = {{{lines}\n\t}}'''        
        return s


    def params_string(self, flow: http.HTTPFlow):
        lines = ''
        for key,value in flow.request.query.items():
            lines += f"\n\t\t'{key}': '{value}',"
        s = f'''params = {{{lines}\n\t}}'''        
        return s

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
            d = json.loads(flow.request.text)
            for key,value in d.items():
                lines += f"\n\t\t'{key}': {value},"
        
        s = f'''data = {{{lines}\n\t}}'''        
        return s


    

addons = [
    GenCode()
]