import json
import re
import random

from mitmproxy import ctx
from mitmproxy import flowfilter

'''
缩短广告的播放时间
原理：通过替换为一个时长短的视频的URL
这里有2种广告：
1. is.snssdk.com  response方法里替换
2. ad.ixigua.com  Todo  
'''


videos = [
    "http://vd2.bdstatic.com/mda-jesntzw6569xqudw/mda-jesntzw6569xqudw.mp4",
    "https://vd3.bdstatic.com/mda-jfpeu3azyxp3yxjr/mda-jfpeu3azyxp3yxjr.mp4",
    "https://raw.githubusercontent.com/zhoujie903/LearnPython/master/mitmproxy_addons/2.mp4"    
]

class Ad_short(object):

    def __init__(self):
        self.filter = flowfilter.parse(r'~u https://is.snssdk.com/api/ad/union/sdk/get_ads')

    def response(self, flow):
        if flowfilter.match(self.filter, flow):
            url = f'"video_url":"{random.choice(videos)}"' 
            flow.response.replace(r'"video_url":"[^"]+"', url)

addons = [
    Ad_short()
]
