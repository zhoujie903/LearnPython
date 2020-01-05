import json
import re
import random

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy import http

# 192.168.1.101:60431: Certificate verification error for sdk.e.qq.com: self signed certificate in certificate chain (errno: 19, depth: 1)
# 192.168.1.101:60431: Invalid certificate, closing connection. Pass --insecure to disable validation. 

'''
缩短广告的播放时间
原理：通过替换为一个时长短的视频的URL
这里有2种广告：
1. response返回广告视频的URL, 比如："video_url":"https://xxx.com/*.mp4" 
2. request.url为广告视频URL直接请求，比如：https://xxx.com/*.mp4

返回广告URL的源：
https://mi.gdt.qq.com/gdt_mview.fcg?posid=8000587800595533&ext=%7B%22req%22%3A%7B%22placement_type%22%3A10%2C%22sdk_src%22%3A%22%22%2C%22muidtype%22%3A2%2C%22c_isjailbroken%22%3Afalse%2C%22sdk_st%22%3A1%2C%22m5%22%3A%22C5AE84F2-18D0-4BB8-B11F-5D962C555543%22%2C%22c_device%22%3A%22iPhone%206s%20Plus%22%2C%22c_h%22%3A2208%2C%22muid%22%3A%22e09a6a64b3210028e076b85c20d5bb1c%22%2C%22lng%22%3A0%2C%22c_pkgname%22%3A%22com.ios.bubble.bear%22%2C%22c_os%22%3A%22ios%22%2C%22render_type%22%3A1%2C%22m7%22%3A%2296D340C6-51D9-F21B-3800-0938E4D00789%22%2C%22conn%22%3A1%2C%22scs%22%3A%22000136197ea9%22%2C%22c_devicetype%22%3A1%2C%22c_w%22%3A1242%2C%22m8%22%3A%2202D340C651D9F21B38000938E4D00745%22%2C%22carrier%22%3A1%2C%22support_c2s%22%3A1%2C%22c_sdfree%22%3A0%2C%22lat%22%3A0%2C%22c_ori%22%3A0%2C%22c_dpi%22%3A320%2C%22sdkver%22%3A%224.10.13%22%2C%22deep_link_version%22%3A1%2C%22max_duration%22%3A31%2C%22tmpallpt%22%3Atrue%2C%22c_osver%22%3A%2213.0%22%7D%7D&count=1&adposcount=1&datatype=2&support_https=1

广告源：
https://adsmind.apdcdn.tc.qq.com/adsmind.tc.qq.com/*.mp4

https://v3-ad.ixigua.com/3c1c49dca71627102020a99c0b5f352d/5dd60795/video/tos/cn/tos-cn-ve-51/5d3e508a7fe3404ba1871de9c634ed02/toutiao.mp4

https://adsmind.ugdtimg.com/*.mp4

https://cdn-creatives-tencent-prd.unityads.unitychina.cn/assets/5c62c5e03f68d9001c3b1d0e/H265_high.mp4

http://v.wallpaper.cdn.pandora.xiaomi.com/mitv/10013/5/d5287c72ad73e239e0e36e2d68d5c7e2.mp4

https://v2.aiclk.com/1000002/d1637a1c0182ec5022227e9b6887163e_1000002.mp4
'''


videos = [
    "http://vd2.bdstatic.com/mda-jesntzw6569xqudw/mda-jesntzw6569xqudw.mp4",
    "https://vd3.bdstatic.com/mda-jfpeu3azyxp3yxjr/mda-jfpeu3azyxp3yxjr.mp4",
    "https://raw.githubusercontent.com/zhoujie903/LearnPython/master/mitmproxy_addons/2.mp4"
]

class Ad_short(object):

    def __init__(self):
        f = open('/Users/zhoujie/Documents/zhoujie903/LearnScrapy/mitmproxy_addons/1.mp4','rb')
        self.content = f.read()
        # self.content = b'hello' 
        f.close()

        urls = [
            r'api/v1/king/rob/rob',
        ]
        self.huoshan = flowfilter.parse('|'.join(urls))

        self.flowfilters = [
            self.huoshan, 
        ]      

        mp4_urls = [
            '/*.mp4',
        ]
        self.mp4 = flowfilter.parse('|'.join(mp4_urls))

        cfg_urls = [
            # 响应字段："video_url"
            r'is.snssdk.com/api/ad/union/sdk/get_ads',

            # 响应字段："video":"
            r'mi.gdt.qq.com/gdt_mview.fcg',
        ]
        self.cfg = flowfilter.parse('|'.join(cfg_urls))


    def request(self, flow: http.HTTPFlow):
        if any( [ filter(flow) for filter in self.flowfilters ] ):
            flow.request.replace(r'result=false','result=true')
            return

        if self.mp4(flow):
            ctx.log.error('mp4 url hit......')
            ctx.log.error(flow.request.url)          

            # This example shows how to send a reply from the proxy immediately
            # without sending any data to the remote server.
            flow.response = http.HTTPResponse.make(
                200,  # (optional) status code
                self.content,  # (optional) content
                {"Content-Type": "video/mp4"}
            )
            return



    def response(self, flow):
        if self.cfg(flow):
            url = f'"video_url":"{random.choice(videos)}"'
            flow.response.replace(r'"video_url":"[^"]+"', url)
            flow.response.replace(r'"video":"[^"]+"', url)


    def done(self):
        # 不能使用ctx.log
        # ctx.log.info('event: done')
        print('event: done')

addons = [
    Ad_short()
]
