import json
import re
import time

from mitmproxy import ctx
from mitmproxy import flowfilter

'''
东方头条App - 幸运大转盘 - 重放
'''


# https://zhuanpan.dftoutiao.com/zhuanpan/get_zhuanpan_new
# https://zhuanpan.dftoutiao.com/zhuanpan/get_gold

def print_color(message):
    print(' \033[1;31m', message, '\033[0m')


class Zhuangpan(object):
    def __init__(self):
        self.filter = flowfilter.parse(r'(~u zhuanpan/get_zhuanpan_new) | (~u zhuanpan/get_gold)')
        self.flows = []
        self.urls = set()

    def request(self, flow):               
        if flowfilter.match(self.filter, flow):
            url = flow.request.url
            if not url in self.urls: 
                print_color(url)
                self.flows.append(flow)
                self.urls.add(url)
            

    def response(self, flow):
        if flowfilter.match(r'~u zhuanpan/get_zhuanpan_new', flow):
            text = flow.response.text
            data = json.loads(text)
            remain = data.get('data').get('cur_num')
            if remain > 0 and len(self.urls) >= 2:
                print_color('remain count:{}'.format(remain))
                flows = [f.copy() for f in self.flows]
                ctx.master.commands.call("replay.client", flows)
                time.sleep(1)                


addons = [
    Zhuangpan()
]
