import json
import re

import click
import requests

from mitmproxy import ctx
from mitmproxy import flowfilter
"""
百度极速版 - 晒收入
1. 百度极速版中晒收入到微博
2. 微博中打开分享条目
3. 其它百度系app中自动完成了晒收任务
"""

class Baidu_mitm(object):
    def __init__(self):
        self.filter = flowfilter.parse(r'~u https://vv.baidu.com/activity/h5/landpage')

    def request(self, flow):               
        if flowfilter.match(self.filter, flow):
            url = flow.request.url
            ctx.log.info(click.style(url, fg="red"))
            for pid in ['1','4','2','6']:
                u = re.sub(r'productid=\d', 'productid={}'.format(pid), url)
                ctx.log.info(click.style(u,fg="red"))                
                requests.get(u)

    def response(self, flow):
        pass

   
addons = [
    Baidu_mitm()
]
