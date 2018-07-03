# -*- coding: utf-8 -*-
# 登录PC端的微博, 获取登录用户的粉丝、关注的人、朋友[互相关注]

# ToDo
# 1、每次运行都需要用手机扫码登录:
#       解决方法:关闭登录保护[登录保护:开启后,在非受信任的设备登录需要短信或扫码验证],用户名和密码登录
#       缺点:降低了安全性
#       解决方法:登录过一次，记录下cookie，下次启动时用cookie登录
# 2、页码数被写死了，需要动态获取   Done
# 3、用户ID写死了，需要动态获取 Done
# 4、用logging模块显示日志 Done


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

import re
import pickle
import logging

# -- 微博的一些页面 --
WEIBO_URL = 'https://weibo.com/'
SETTING_URL = 'https://account.weibo.com/set/index'  # 设置页面
# ----

# -- 账号 --
LOGIN_NAME = 'zhoujie_903@163.com'
PASSWORD = ''
# 用户：一吻江山，1969776354, 1005051969776354 = 100505[不知道每个用户是不是一样] + 1969776354[用户ID]
USER_ID = None
# ----

# -- 配置 --
WAIT_TIME = 10
# ----

options = Options()
# options.set_headless()

# 禁止加载图片
# prefs = {
#     'profile.default_content_setting_values' : {
#         'images' : 2
#     }
# }
# options.add_experimental_option('prefs',prefs)
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, WAIT_TIME)

fans = set()        # 我的粉丝
follows = set()     # 我的关注
friends = set()     # 互相关注的人-朋友

logging.basicConfig(level=logging.INFO)

def is_login():
    url = SETTING_URL
    browser.get(url)

    try:
        # 载入Cookies
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
    except FileNotFoundError:
        logging.info('cookie文件不存在')

    browser.get(url)
    logging.info(browser.current_url)
    result = re.match(url, browser.current_url)
    return result is not None


def login_by_code():
    '''扫二维码登录'''
    try:
        url = WEIBO_URL
        browser.get(url)

        xpath = '//*[@id="pl_login_form"]/div/div[1]/div/a[2]'
        wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)))

        a = browser.find_element_by_xpath(xpath)
        a.click()
    except TimeoutException:
        pass


def login_by_password():
    '''用户名和密码登录'''
    logging.info('login_by_password')
    try:
        url = WEIBO_URL
        browser.get(url)

        xpath = '//*[@id="pl_login_form"]/div/div[1]/div/a[1]'
        wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)))

        xpath = '//*[@id="loginname"]'
        loginname = browser.find_element_by_xpath(xpath)
        loginname.clear()
        loginname.send_keys(LOGIN_NAME)

        xpath = '//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input'
        password = browser.find_element_by_xpath(xpath)
        password.clear()
        password.send_keys(PASSWORD)

        xpath = '//*[@id="pl_login_form"]/div/div[3]/div[6]/a'
        login = browser.find_element_by_xpath(xpath)
        login.click()
    except TimeoutException:
        pass


def wait_for_login():
    logging.info('wait_for_login')
    w = WebDriverWait(browser, 30, poll_frequency=1)
    w.until(EC.url_matches('https://weibo.com/u/\d+'))


def get_login_user_id():
    '''获取登录用户ID, 需要已登录才能获取'''
    logging.info('get_login_user_id')
    url = SETTING_URL
    browser.get(url)

    xpath = '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/div/span/a'
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    home = browser.find_element_by_xpath(xpath)
    home_URL = home.get_attribute('href')  # https://weibo.com/1969776354/info
    print(home_URL)

    result = re.search('/(\\d+)/', home_URL)
    user_id = result.group(1)
    return user_id


def get_fans():
    """
    获取我粉丝
    """
    def url_at_index(i):
        url = 'https://weibo.com/%s/fans?cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__87_page=%d#Pl_Official_RelationFans__87' % (
            USER_ID, i)
        return url

    def fetch_page_at_index(i):
        # 打开页面
        url = url_at_index(i)
        browser.get(url)

        # 等待页面获取完成
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'follow_inner')))

        # 获取粉丝昵称
        fans_list = browser.find_elements_by_css_selector(
            'div.follow_inner > ul > li > dl > dd.mod_info.S_line1 > div.info_name.W_fb.W_f14 > a.S_txt1')
        for item in fans_list:
            # print(item.text)
            fans.add(item.text)

    try:
        fetch_page_at_index(1)

        xpath = '//*[@id="Pl_Official_RelationFans__87"]/div/div/div/div[2]/div[2]/div/a[last()-1]'
        pages = _count_of_pages(xpath)

        for i in range(2, pages + 1):
            fetch_page_at_index(i)
    finally:
        pass


def get_follows():
    """
    获取我关注
    """
    def url_at_index(i):
        url = 'https://weibo.com/p/100505%s/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__92_page=%d#Pl_Official_RelationMyfollow__92' % (
            USER_ID, i)
        return url

    def fetch_page_at_index(i):
        # 打开页面
        url = url_at_index(i)
        browser.get(url)

        # 等待页面获取完成
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'member_ul')))

        follow_list = browser.find_elements_by_css_selector(
            'div.member_box > ul > li > div.member_wrap.clearfix > div.mod_info > div.title.W_fb.W_autocut > a.S_txt1')
        for item in follow_list:
            # print(item.text)
            follows.add(item.text)

    try:
        fetch_page_at_index(1)

        xpath = '//*[@id="Pl_Official_RelationMyfollow__92"]/div/div/div/div[4]/div/a[last()-1]'
        pages = _count_of_pages(xpath)

        for i in range(2, pages + 1):
            fetch_page_at_index(i)
    finally:
        pass


def _count_of_pages(xpath):
    '''
    返回页数
    '''
    count_pages = browser.find_element_by_xpath(xpath)
    pages = int(count_pages.text)
    return pages


def main():
    global USER_ID

    if is_login():
        logging.info('已登录')
    else:
        logging.info('未登录')
        login_by_password()
        wait_for_login()
        cookies = browser.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))

    USER_ID = get_login_user_id()
    if USER_ID:
        print('登录用户:', USER_ID)
        get_fans()
        print('\nfans:\n', fans)
        print('total fans:', len(fans))

        get_follows()
        print('\nfollows:\n', follows)
        print('total follows:', len(follows))

        friends = follows.intersection(fans)
        print('\nfriends:\n', friends)
        print('total friends:', len(friends))
    else:
        logging.warning('没用获取到用户ID')

    browser.close()


if __name__ == '__main__':
    main()
