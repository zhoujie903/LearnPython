import json
import re
import time

from mitmproxy import ctx
from mitmproxy import flowfilter

'''
东方头条App - 幸运大转盘 - 重放

以这2个请求为一组来重放
https://zhuanpan.dftoutiao.com/zhuanpan_v3/get_zhuanpan_new
https://zhuanpan.dftoutiao.com/zhuanpan_v3/get_gold
'''




def print_color(message):
    print(' \033[1;31m', message, '\033[0m')


class Zhuangpan(object):
    def __init__(self):
        self.filter = flowfilter.parse(r'(~u zhuanpan_v3/get_zhuanpan_new) | (~u zhuanpan_v3/get_gold)')
        self.new_fliter = flowfilter.parse(r'~u zhuanpan_v3/get_zhuanpan_new') 
        self.get_fliter = flowfilter.parse(r'~u zhuanpan_v3/get_gold')
        self.flows = []
        self.urls = set()
        self.remain = 0

    def request(self, flow):               
        if flowfilter.match(self.filter, flow):
            url = flow.request.url
            if not url in self.urls: 
                print_color(url)
                self.flows.append(flow)
                self.urls.add(url)
            

    def response(self, flow):
        if flowfilter.match(self.new_fliter, flow):
            flow.response.replace(r'"gold":0', '"gold":999')

            text = flow.response.text
            data = json.loads(text)
            self.remain = data.get('data').get('cur_num')
            print_color('remain count:{}'.format(self.remain))


        if flowfilter.match(self.get_fliter, flow):
            if self.remain > 0 and len(self.urls) >= 2:                
                flows = [f.copy() for f in self.flows]
                ctx.master.commands.call("replay.client", flows)
                time.sleep(0.2)                


addons = [
    Zhuangpan()
]
