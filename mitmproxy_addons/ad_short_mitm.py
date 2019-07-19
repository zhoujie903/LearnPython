import json
import re
import random

from mitmproxy import ctx
from mitmproxy import flowfilter

'''
缩短广告的播放时间
原理：通过替换为一个时长短的视频的URL
'''


videos = [
    "http://vd2.bdstatic.com/mda-jesntzw6569xqudw/mda-jesntzw6569xqudw.mp4",
    "https://vd3.bdstatic.com/mda-jfpeu3azyxp3yxjr/mda-jfpeu3azyxp3yxjr.mp4"    
]

class Ad_short(object):

    def __init__(self):
        self.filter = flowfilter.parse(r'~u https://is.snssdk.com/api/ad/union/sdk/get_ads')

    def response(self, flow):
        if flowfilter.match(self.filter, flow):
            text = flow.response.text
            url = '"video_url":"{}"'.format(random.choice(videos)) 
            url +='}'
            flow.response.text = re.sub(r'"video_url":"(.+)"}', url, text)


addons = [
    Ad_short()
]
