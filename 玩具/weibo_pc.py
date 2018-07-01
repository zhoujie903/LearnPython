
# 获取用户的粉丝、关注的人

# ToDo
# 1、每次运行都需要用手机扫码登录
# 2、页码数被写死了，需要动态获取   Done
# 3、用户ID写死了，需要动态获取 Done


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

# 用户：一吻江山，1969776354, 1005051969776354 = 100505[不知道每个用户是不是一样] + 1969776354[用户ID]
USER_ID = 'xxxx' 

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 50)

fans = set()  # 我的粉丝
follows = set()  # 我的关注
follows_no_fans = set()  # 我关注的但不关注我的人
friends = set()  # 互相关注的人-朋友


def login_by_user():
    try:
        url = 'https://weibo.com/'
        browser.get(url)

        xpath = '//*[@id="pl_login_form"]/div/div[1]/div/a[2]'

        wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)))

        a = browser.find_element_by_xpath(xpath)
        a.click()
    except TimeoutException:
        # print('TimeoutException')
        pass


def wait_for_login():
    try:
        wait.until(EC.url_contains("https://weibo.com/u/"))
        url = browser.current_url

        result = re.search('https://weibo.com/u/(\\d+)/', url)
        userid = result.group(1)

        global USER_ID
        USER_ID = userid
        print('已登录:', userid)
    except TimeoutException:
        print('TimeoutException')


def get_fans():
    """
    获取我粉丝
    """
    def url_at_index(i):
        url = 'https://weibo.com/%s/fans?cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__87_page=%d#Pl_Official_RelationFans__87' % (USER_ID, i)            
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
        pages = count_of_pages(xpath)

        for i in range(2, pages+1):
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
        pages = count_of_pages(xpath)

        for i in range(2, pages+1):
            fetch_page_at_index(i)
    finally:
        pass


def count_of_pages(xpath):
    '''
    返回页数
    '''
    count_pages = browser.find_element_by_xpath(xpath)
    pages = int(count_pages.text)
    return pages


login_by_user()
wait_for_login()


get_fans()
print('\nfans:\n', fans)
print('total fans:', len(fans))

get_follows()
print('\nfollows:\n', follows)
print('total follows:', len(follows))

friends = follows.intersection(fans)
print('\nfriends:\n', friends)
print('total friends:', len(friends))

browser.close()
