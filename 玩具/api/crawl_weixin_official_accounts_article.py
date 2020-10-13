# 通过登录自己的微信订阅号,  爬取 他人微信订阅号 的文章
# 参考文章：https://www.jianshu.com/p/8efa73f0c6e6
# 接口：https://mp.weixin.qq.com/cgi-bin/searchbiz?     
# 接口：https://mp.weixin.qq.com/cgi-bin/appmsg?

import re
from shutil import which
import time
import random
import traceback
import requests

from selenium import webdriver


class Spider(object):
    '''
    微信公众号文章爬虫
    '''

    def __init__(self):
        # 微信公众号账号
        self.account = ''
        # 微信公众号密码
        self.pwd = ''

        # 登录成功后获取到
        self.token = ''

        self.headers = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
        } 

    def create_driver(self):
        '''
        初始化 webdriver
        '''
        options = webdriver.ChromeOptions()
        # 禁用gpu加速，防止出一些未知bug
        options.add_argument('--disable-gpu')

        # 这里我用 chromedriver 作为 webdriver
        # 可以去 http://chromedriver.chromium.org/downloads 下载你的chrome对应版本
        self.driver = webdriver.Chrome(options=options)
        # 设置一个隐性等待 5s
        self.driver.implicitly_wait(5)

    def log(self, msg):
        '''
        格式化打印
        '''
        print('------ %s ------' % msg)

    def login(self):
        '''
        登录拿 cookies
        '''
        try:
            self.create_driver()
            # 访问微信公众平台
            self.driver.get('https://mp.weixin.qq.com/')
            # 等待网页加载完毕
            time.sleep(3)
            # 输入账号
            self.driver.find_element_by_xpath("./*//input[@name='account']").clear()
            self.driver.find_element_by_xpath("./*//input[@name='account']").send_keys(self.account)
            # 输入密码
            self.driver.find_element_by_xpath("./*//input[@name='password']").clear()
            self.driver.find_element_by_xpath("./*//input[@name='password']").send_keys(self.pwd)
            # 点击登录
            self.driver.find_elements_by_class_name('btn_login')[0].click()
            self.log("请拿手机扫码二维码登录公众号")
            # 等待手机扫描
            time.sleep(10)
            self.log("登录成功")
            # 获取cookies 然后保存到变量上，后面要用
            self.cookies = dict([[x['name'], x['value']] for x in self.driver.get_cookies()])

        except Exception as e:
            traceback.print_exc()
        finally:
            # 退出 chorme
            self.driver.quit()


    def get_article(self, query='', keyword=''):
        try:
            url = 'https://mp.weixin.qq.com'
            # 设置headers
            headers = {
                "HOST": "mp.weixin.qq.com",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
            }
            # 登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，
            # 从这里获取token信息
            response = requests.get(url=url, cookies=self.cookies)
            token = re.findall(r'token=(\d+)', str(response.url))[0]
            self.token = token
            time.sleep(2)

            self.log('正在查询[ %s ]相关公众号' % query)
            search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
            # 搜索微信公众号接口需要传入的参数，
            # 有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
            params = {
                'action': 'search_biz',
                'token': token,
                'random': random.random(),
                'query': query,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'begin': '0',
                'count': '5'
            }
            # 打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
            response = requests.get(search_url, cookies=self.cookies, headers=headers, params=params)
            time.sleep(2)
            # 取搜索结果中的第一个公众号
            lists = response.json().get('list')[0]
            # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
            fakeid = lists.get('fakeid')
            nickname = lists.get('nickname')

            app_msg_cnt = 5
            begin = 0
            while begin < app_msg_cnt:
                j = self.get_one_page(fakeid=fakeid, keyword=keyword, begin=begin, count=30)
                app_msg_list = j.get('app_msg_list', [])
                app_msg_cnt = j.get('app_msg_cnt', 5)
                begin += len(app_msg_list)
                
                for per in app_msg_list:
                    print(f"[{per.get('title')}]({per.get('link')})")
                
                time.sleep(2)

        except Exception as e:
            traceback.print_exc()

    def get_one_page(self, fakeid='', keyword='', begin=0, count=5):
        # 微信公众号文章接口地址
        search_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'

        # 搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
        params = {
            'action': 'list_ex',
            'token': self.token,
            'random': random.random(),
            'fakeid': fakeid,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'begin': begin,  # 不同页，此参数变化，变化规则为每页加5
            'count': count,
            'query': keyword,
            'type': '9'
        }

        # self.log('正在查询公众号[ %s ]相关文章' % nickname)

        # 打开搜索的微信公众号文章列表页
        response = requests.get(search_url, cookies=self.cookies, headers=self.headers, params=params)
        j = response.json()
        # print(j)
        return j


if __name__ == '__main__':
    spider = Spider()
    spider.login()
    # spider.get_article('程序员小灰','漫画')
    spider.get_article('Python绿色通道','Python办公自动化')

# 接口 https://mp.weixin.qq.com/cgi-bin/appmsg 的响应格式：
# {
#   "app_msg_cnt": 209,
#   "app_msg_list": [
#     {
#       "aid": "2653211187_1",
#       "album_id": "0",
#       "appmsg_album_infos": [],
#       "appmsgid": 2653211187,
#       "checking": 0,
#       "create_time": 1598231700,
#       "digest": "",
#       "is_original": 1,
#       "is_pay_subscribe": 0,
#       "item_show_type": 0,
#       "itemidx": 1,
#       "link": "http://mp.weixin.qq.com/s?__biz=MzIxMjE5MTE1Nw==&mid=2653211187&idx=1&sn=c062ab9598cf0af12acbf849478bb0d3&chksm=8c99b8e9bbee31ff9b1c86cfb32030b4cbabc0b98e9be850efe46fffb6eb6bac335f8b2b7b43#rd",
#       "tagid": [],
#       "title": "<em>漫画</em>：什么是 “跳表” ？",
#       "update_time": 1598231700
#     },
#     ...
#   ],
#   "base_resp": {
#     "err_msg": "ok",
#     "ret": 0
#   }
# }


