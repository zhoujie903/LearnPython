import pathlib
import os.path
import json
import re
import time
import pprint
from urllib.parse import urlparse
import logging
import itertools
import collections
import importlib
import traceback

from mitmproxy import ctx, flowfilter, http

from jinja2 import Template, Environment, FileSystemLoader
from merge import *

'''
生成接口python代码
mitmdump -q --flow-detail 0 --set session='huawei' -s "/Users/zhoujie/Documents/zhoujie903/LearnScrapy/mitmproxy_addons/gen_code/gen_code_mitm.py" 
'''


def apps():

    # 百度 - 好看
    urls = [
        r'activity/acusercheckin',  # 每日签到
        r'signIn/new/sign',  # 游戏中心签到

        '/activity/acad/bubblead',
        Api(r'/activity/tasks/active', params_as_all=True, f_p_kwarg={'productid':1, 'tid':404}),
        Api(r'activity/acad/rewardad', params_as_all=True, f_p_kwarg={'productid':1, 'tid':404} ),  # 看视频
        Api(r'api/task/1/task/379/complete', f_p_arg=['rewardVideoPkg']), # 看视频
        '/activity/tasks/taskreward',
    ]
    hao_kan = App(urls, 'hao-kan')

    # 百度 - 百度极速版
    urls = [
        '/activity/acad/bubblead',
        Api(r'/activity/tasks/active', f_p_kwarg={'productid':2, 'tid':404}),
        Api(r'/activity/acad/rewardad', f_p_kwarg={'productid':2, 'tid':404} ),  # 看视频
        Api(r'/api/task/1/task/381/complete', f_p_arg=['rewardVideoPkg']), # 看视频
        '/activity/tasks/taskreward',
    ]
    bai_du_flash = App(urls, 'bai-du-flash')

    # 百度 - 全民小视频
    urls = [
        r'mvideo/api',  # 每日签到
        '/activity/acad/bubblead',
        Api(r'/activity/tasks/active', f_p_kwarg={'productid':4, 'tid':418}),
        Api(r'/activity/acad/rewardad', f_p_kwarg={'productid':4, 'tid':418} ),  # 看视频
        Api(r'/api/task/1/task/380/complete', f_p_arg=['rewardVideoPkg']), # 看视频
        '/activity/tasks/taskreward',
    ]
    quan_ming = App(urls, 'quan-ming')

    flowfilters = [
        # self.bai_du_flash,
        # app_cai_dan_sp(),
        # app_cheng_yu_qwx(),
        # self.toutiao,
        # self.huoshan,
        # self.qtt_video,
        # app_qu_zhong_cai(),
        app_qu_tou_tiao(),
        # app_tian_chi_xiao_xiu_cai(),
        # self.hao_kan,
        # self.quan_ming,
        # app_ma_yi_kd(),
        # self.dftt,
        # self.zhong_qin_kd,
        # self.kai_xin_da_ti,
        # self.qu_jian_pan,
        # app_you_xi_he_zhi(),
        # self.yang_ji_chang,
        # app_zhu_lai_le(),
    ]

    return flowfilters

    # urls = [
    #     r'/login/index',
    #     r'/main/index',
    #     r'/card/info',
    #     r'/card/open',
    #     r'/card/doublereward',
    # ]
    # kai_xin_da_ti = App(urls, 'kai-xin-da-ti')

    # 趣头条小视频
    # urls = [
    #     Api(r'seafood-api.1sapp.com/v1/readtimer/report',log='看视频得金币', f_b_enc={'qdata'}, f_b_arg={'qdata'})
    # ]
    # qtt_video = App(urls, 'qtt-video')

def api_common():
    common = [
        # 游戏
        Api(r'/x/user/token', log='获取g_token'),
        Api(r'/x/open/game', log='打开游戏 - 获取ticket', f_p_arg=['app_id']),
    ]
    return common

def api_sign():
    urls = [
        Api('/x/game-center/gapp/sign-in', log='签到'),
        Api('/x/game-center/gapp/sign-in-double', log='签到 - double'),
    ]
    return urls

# ''' 彩蛋视频 '''
def app_cai_dan_sp():
    ''' 彩蛋视频 '''
    urls = [
        Api(r'/task/sign',log='sign - 签到、金币信息'),
        Api(r'task/timer_submit',log='看视频 - 得金币', f_b_enc={'qdata'}, f_b_arg={'qdata'}),
        Api(r'/h5/task/submit',log='日常福利 - 观看小视频', body_as_all=True),
        Api(r'/h5/reduce/reward',log='瓜分他人金币', body_as_all=True),
        r'/h5/bubble/prize',
        Api('/h5/reward/prize',log='iphone免费抽'),
        Api('/qapptoken', log='获取access_token'),
        Api('/withdraw/getCoinLog',log='彩蛋视频 - 金币明细', f_p_arg=['page','page_size']),
        Api('/withdraw/order/listApp',log='彩蛋视频 - 提现列表'),
        Api('/withdraw/order/create',log='彩蛋视频 - 提现', f_b_arg=['sku_id']),
    ]
    return App(urls, 'cai-dan-sp')

# ''' 成语趣味消
def app_cheng_yu_qwx():
    urls = [
        Api('/chengyu_app/signin', log='签到'),
        Api('/chengyu_app/draw_fuca', log='抽字'),
        Api('/chengyu_app/addcoin', f_b_arg={'open_id','add_num'}),
        Api('/chengyu_app/update_task', f_b_arg={'task_index'}),
        Api('/chengyu_app/get_task_award', f_b_arg={'task_index'}),
        Api('/chengyu_app/'),
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    return App(urls, 'cheng-yu-qu-wei-xiao')

# ''' 东方头条 '''
def app_dftt():
    ''' 东方头条 '''
    urls = [
        r'sign/news_take_s',
        r'timesaward/timesaward/get_award',
        r'answer_question_new/get_question',
        r'answer_question_new/add_user_bonus',
        r'zhuanpan_v3/get_zhuanpan_new',
        r'zhuanpan_v3/get_gold',
        r'hit_susliks/hit_susliks/start_play_game',
        r'hit_susliks/hit_susliks/finish_play_game',
        r'hit_susliks/hit_susliks/set_user_video_num',
        r'hit_susliks/hit_susliks/lucky_draw',
        r'turn_over_packet/packet/add_packet_bonus',
    ]
    dftt = App(urls, 'dong-fan-tt')
    
# ''' 火山极速版 '''
def app_huo_shan():
    ''' 火山极速版 '''
    urls = [
        Api('/luckycat/hotsoon/v1/task/page', log='火山-获取任务状态'),
        Api('/luckycat/hotsoon/v1/task/done/treasure_task', log='火山-开宝箱'),
        Api('/luckycat/hotsoon/v1/task/done/show_money', log='火山-晒收入', params_as_all=True),
        Api('/luckycat/hotsoon/v1/task/done/excitation_ad', log='火山-', params_as_all=True, body_as_all=True),
        Api('/luckycat/hotsoon/v1/task/done/daily_read_1m', log='火山-1分钟', params_as_all=True),
        Api('/luckycat/hotsoon/v1/task/done/daily_read_2m', log='火山-2分钟', params_as_all=True),
        Api('luckycat/v1/task/page/', log='火山-获取任务状态', params_as_all=True),
        Api('luckycat/v1/task/sign_in/', log='火山-每日签到', params_as_all=True),
        Api('luckycat/v1/task/open_treasure_box/', log='火山-开宝箱', params_as_all=True),
        Api('luckycat/v1/task/done_task/', log='火山-开宝箱-看视频', params_as_all=True, body_as_all=True),
        Api('luckycat/v1/landing/add_amount/', log='火山-晒收入', params_as_all=True),
        Api('luckycat/v1/task/get_read_bonus/',params_as_all=True),
        Api('api/ad/v1/inspire/', log='火山-获取广告', params_as_all=True),
    ]
    return App(urls, 'huo-shan')

# 游戏 - 填词小秀才
def api_tczyqtt():
    c_tczyqtt = [
        # 游戏 - 填词小秀才
        Api('/api/v1/tczyqtt/login', log='填词小秀才 - 登录 - 获取open_id', f_p_arg=['ticket'], api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/sign',log='填词小秀才 - 签到'),
        Api('/api/v1/tczyqtt/lottery',log='填词小秀才 - lottery', api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/get_reward',log='填词小秀才 - 任务完成', f_p_arg=['activity_id'], api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/open_redpacket',log='填词小秀才 - 红包', api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/draw_a_char',log='填词小秀才 - 抽字', api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/add_coin',log='填词小秀才 - 过关领金币'),
        '/api/v1/tczyqtt/'
    ]
    return c_tczyqtt

# ''' 趣键盘 '''
def app_qu_jian_pan():
    ''' 趣键盘 '''
    urls = [
        r'/gk/game/fanpai/basicInfo',
        r'/gk/game/fanpai/getAward',
        r'/gk/game/fanpai/awardDouble',
        r'/gk/game/fanpai/',

        r'/gk/game/savingsBank/collectPigMoney',
        r'/gk/game/savingsBank/exchangePigMoney',
        Api(r'/gk/game/savingsBank/unlockDouble',f_b_arg={'taskType'}, content_type='json'),

        r'/gk/draw/info',
        r'/gk/draw/extract',
        Api('/gk/draw/double', f_b_arg={'ticket'}),
        r'/gk/draw/package',
        r'/gk/draw/pkdouble',

        # 便利店
        Api('/gk/game/bianlidian/receiveBox', f_b_arg={'packageId'}),
        Api('/gk/game/bianlidian/draw/double', f_b_arg={'ticket'}),
        Api('/gk/game/bianlidian/receiveGift', log='便利店 - xxx金币礼包碎片', f_b_arg={'ticket'}),
        Api('/gk/game/bianlidian/receiveMediumCoin', log='便利店 - 随机金币奖励', f_b_arg={'ticket'}),
        r'/gk/garbage/',
        r'/gk/game/dadishu/',
        r'/gk/game/bianlidian/',
        r'/qujianpan/',
    ]
    return App(urls, 'qu-jian-pan')

# ''' 趣头条 '''
def app_qu_tou_tiao():
    ''' 趣头条 '''
    urls = [
        Api(r'/sign/sign', log='每日签到', params_as_all=True),
        Api(r'/mission/intPointReward', log='时段签到', params_as_all=True, api_ok={'code':[-312]}),
        Api(r'/taskcenter/getReward', log='任务完成 - 领金币', params_as_all=True),
        r'/x/game-center/user/sign-in',
        r'/x/game-center/user/last-sign-coin',
        Api('/x/game-report/special_report', log='special_report', f_name='game_do_task',f_b_arg={'app_id'},f_b_kwarg={'report_type':'round'}),
        Api('/x/game-report/duration_report', log='duration_report', f_name='game_duration_report',f_b_arg={'start_ts','duration'},f_b_kwarg={'report_type':'duration_addition'}),
        Api('/x/task/v2/take-reward', log='任务完成 - 领金币', f_name='game_take_reward',f_b_arg={'task_id'}),
        r'/newuserline/activity/signRewardNew',  # 挑战签到
        Api(r'/mission/receiveTreasureBox', log='趣头条-开宝箱', api_ok={'code':[-1710]}),
        Api(r'/content/readV2',params_as_all=True),
        Api(r'/app/re/taskCenter/info/v1/get', log='任务信息', params_as_all=True, p_as_all_limit=1),
        Api(r'/app/user/info/personal/v1/get', log='用户信息', params_as_all=True, p_as_all_limit=1),
        Api(r'/coin/service', body_as_all=True),
        r'readtimer/report',
        # Api(r'motivateapp/mtvcallback', params_as_all=True),
        Api(r'/x/feed/getReward', log='信息流-惊喜红包', params_as_all=True, api_ok={'code':[-308]}),
        Api(r'/lotteryGame/status', log='天天乐-信息'),
        Api(r'/tiantianle/video', log='天天乐-增加机会', params_as_all=True),
        Api(r'/lotteryGame/order', log='天天乐-投注'),
        r'x/v1/goldpig/bubbleWithdraw',  # 金猪 - 看视频
        r'x/v1/goldpig/withdraw',  # 金猪
        Api(r'finance/piggybank/taskReward',api_ok={'code':-2004}),  # 存钱罐

        # 游戏 - 种菜
        r'x/tree-game/task-list',
        r'x/tree-game/left-plant-num',
        r'x/tree-game/plant-ok',
        r'x/tree-game/add-plant',
        r'x/tree-game/fertilizer/add',
        r'x/tree-game/fertilizer/use',
        r'x/tree-game/water-plants',
        r'x/tree-game/my-gift-box/draw-lottery',
        r'x/tree-game/my-gift-box/receive-prize',
        r'/x/tree-game/task-update',
        r'/x/tree-game/add-task-drips',
        # r'x/tree-game/',

        r'x/task/encourage/activity/grant',  # 游戏 - 瓜分
        r'api/loginGame',
        r'api/qttAddCoin',

        # 游戏 - 成语
        Api(r'/api/Login', log='猜成语赚钱 - 登录'),
        r'api/AddCoin',  

        # 游戏 - 成语消消乐
        Api('/chengyu/login', log='成语消消乐 - 登录 - 获取open_id', f_b_arg={'ticket'}),
        Api('/chengyu/addcoin', log='成语消消乐 - 金币', f_b_arg={'add_num'}),
        Api('/chengyu/update_red_packet', log='成语消消乐 - 过关得现金', f_b_arg={'level'}),

        # 游戏 - 切菜
        Api(r'/x/open/coin/add', body_as_all=True),

        # 游戏 - 糖果
        Api(r'/happy/qtt/userinfo', log='游戏 - 糖果 - 获取open_id', f_p_arg=['ticket']),
        Api(r'/happy/protocol', log='游戏 - 糖果 - 获取金币', f_b_arg={'data'}),            

        # 游戏 - 钓鱼
        Api(r'/xyx_sdk/gw/partner_login', log='游戏 - 钓鱼 - 登录', body_as_all=True),            
        Api(r'/qtt/coin/withdraw', log='游戏 - 钓鱼 - 获取金币'),            

        # 游戏 - 大脑
        Api(r'/api/v1/z6h5/sign', log='游戏 - 大脑 - 签到'),            
        Api(r'/api/v1/z6h5/lottery', log='游戏 - 大脑 - 获取红包'),            

        Api(r'/press_trigger',log='幸运大转盘'),

        # 金猪
        Api(r'/actcenter/piggy/videoConfirm',log='合成金猪 - 气泡', f_p_arg=['tag']),
        r'/actcenter/piggy/',

        Api(r'/member/getMemberIncome',log='收益详情', f_p_arg=['page','last_time']),
        Api(r'/search/searchContentNew',log='搜索内容得金币', params_as_all=True, p_as_all_limit=3),
        
    ]
    urls.extend(api_common())
    urls.extend(api_tczyqtt())
    return App(urls, 'qu-tou-tiao')

# ''' 趣种菜 '''
def app_qu_zhong_cai():
    ''' 趣种菜 '''
    urls = [
        Api('/x/tree-game/user', log='趣种菜 - 获取用户信息 - s_token'),
        Api('/x/tree-game/gapp/info', log='趣种菜 - 信息'),
        Api('/x/tree-game/gapp/box/my/rand-reward', log='趣种菜 - 拆礼物 - 点击'),
        Api('/x/tree-game/gapp/box/my/take-reward', log='趣种菜 - 拆礼物 - 收获'),
        Api('/x/tree-game/gapp/add-plant', log='趣种菜 - 植物 - 种下'),
        Api('/x/tree-game/gapp/plant-ok', log='趣种菜 - 植物 - 收获'),
        Api('/x/tree-game/gapp/water-plants', log='趣种菜 - 植物 - 浇水'),
        Api('/x/tree-game/gapp/remove-bug', log='趣种菜 - 植物 - 杀虫'),
        
        # 翻翻乐
        Api('/x/middle/flop/info', log='趣种菜 - 翻翻乐 - 信息'),
        Api('/x/middle/flop/start', log='趣种菜 - 翻翻乐 - 开始'),
        '/x/middle/flop/',

        # 水池
        Api('/x/tree-game/gapp/pool/info', log='趣种菜 - 水池 - 信息'),
        Api('/x/tree-game/gapp/pool/with-draw', log='趣种菜 - 水池 - 存到水壶'),
        Api('/x/tree-game/gapp/pool/speed-up', log='趣种菜 - 水池 - 加速'),
        # '/x/tree-game/gapp/pool/',

        # 兔子
        '/x/tree-game/gapp/activity/rabbit/',
        Api('/x/tree-game/gapp/activity/carrot/take-reward', log='趣种菜 - 植物 - 点我'),

        # Api('/x/tree-game/'),
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    return App(urls, 'qu-zhong-cai')

# ''' 金猪游戏盒子 '''
def app_you_xi_he_zhi():
    ''' 金猪游戏盒子 '''
    urls = [
        # 游戏           
        Api('/x/task/v3/list', log='游戏任务列表'),
        Api('/qapptoken', log='获取access_token'),
        Api('/x/cash/time-bonus/info', log='时段金币 - 信息'),
        Api('/x/cash/time-bonus/get', log='时段金币 - 领取', f_b_arg={'index'}),
        # Api('/x/cash/task-bonus/amount', log='红包 - 领取', f_p_arg={'cnt'}),
        Api('/x/cash/task-bonus/get', log='红包 - 领取', f_p_arg={'cnt'}),
        Api('/withdraw/getCoinLog',log='金币明细', f_p_arg=['page','page_size']),
        Api('game-center-new.1sapp.com/x/game-report/special_report', log='special_report', f_name='game_do_task',f_b_arg={'app_id'},f_b_kwarg={'report_type':'round'}),
        Api('game-center-new.1sapp.com/x/game-report/duration_report', log='duration_report', f_name='game_duration_report',f_b_arg={'start_ts','duration'},f_b_kwarg={'report_type':'duration_addition'}),
        Api('game-center-new.1sapp.com/x/task/v2/take-reward', log='任务完成 - 领金币', f_name='game_take_reward',f_b_arg={'task_id'}),

        # 游戏 - 成语大富豪
        Api('qttgame.midsummer.top/api/Login', log='2-登录游戏', f_name='api_login', f_b_arg={'ticket','game_id'}),
        Api('qttgame.midsummer.top/api/AddCoin', log='成语大富豪 - 金币',f_b_arg={'AddCoinNum','session_id'}),

        # 游戏 - 成语消消乐
        Api('/chengyu/login', log='成语消消乐 - 登录 - 获取open_id', f_b_arg={'ticket'}),
        Api('/chengyu/addcoin', log='成语消消乐 - 金币', f_b_arg={'add_num'}),
        Api('/chengyu/update_red_packet', log='成语消消乐 - 过关得现金', f_b_arg={'level'}),
        
        # 游戏 - 切菜
        Api('/x/open/coin/add', log='切菜 - 金币', body_as_all=True),
        
        # 游戏 - 糖果
        Api(r'/happy/qtt/userinfo', log='游戏 - 糖果 - 获取open_id', f_p_arg=['ticket']),
        Api(r'/happy/protocol', log='游戏 - 糖果 - 获取金币', f_b_arg={'data'}),

        # 游戏 - 钓鱼
        Api(r'/qtt/coin/withdraw', log='游戏 - 钓鱼 - 获取金币'),            
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    urls.extend(api_tczyqtt())
    return App(urls, 'you-xi-he-zi')

# ''' 今日头条 '''
def app_toutiao():
    ''' 今日头条 '''
    urls = [
        'score_task/v1/task/page_data/',
        'score_task/v1/task/sign_in/',
        'score_task/v1/task/open_treasure_box/',
        Api('score_task/v1/task/new_excitation_ad/', {"score_source":None}),            
        'score_task/v1/task/get_read_bonus/',
        'score_task/v1/task/done_task/',
        'score_task/v1/landing/add_amount/',
        'score_task/v1/user/profit_detail/',
        'score_task/v1/novel/bonus/',  # 读小说得金币
        'search/suggest/homepage_suggest/',
        'search/suggest/initial_page/',
        Api(r'score_task/v1/walk/count/', {"count": None}),
        r'score_task/v1/walk/',

        'score_task/v1/sleep/status/',
        'score_task/v1/sleep/start/',
        'score_task/v1/sleep/stop/',
        'score_task/v1/sleep/done_task/',  # 睡觉领金币

        r'ttgame/game_farm/',

        r'score_task/lite/v1/eat/eat_info/',

        'score_task/lite/v1/eat/done_eat/',
        'api/news/feed/v47/',  # 安卓视频tab页
        'api/news/feed/v64/',  # ios视频tab页
        'api/search/content/',
    ]
    return App(urls, 'jin-ri-tou-tiao')

def app_ma_yi_kd():
    # 蚂蚁看点
    urls = [
        Api(r'article/treasure_chest', log='时段签到', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/user/shai_income_task_award',log='晒收'),
        r'TaskCenter/daily_sign',
        # r'WebApi/',
        r'WebApi/Stage/task_reward',
        r'WapPage/get_video_status',
        r'WebApi/RotaryTable/turn_rotary_new',
        r'WebApi/RotaryTable/turn_reward',
        r'WebApi/RotaryTable/video_double',
        r'WebApi/RotaryTable/chestReward',


        Api(r'/WebApi/sleep/sleep_start',log='睡觉 - 开始'),
        Api(r'/WebApi/sleep/get_sleep_score',log='睡觉 - 醒来'),

        Api(r'article/haotu_video',log='看视频得金币', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'article/complete_article',log='读文章得金币', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/user/rewar_video_callback', log='视频广告 - 得金币', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/article/complete_welfare_score.json', log='福袋 - 得金币', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/user/adlickstart.json',log='点击广告领金币 - 开始', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/user/adlickend.json',log='点击广告领金币 - 结束', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/user/task_second_callback.json',f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v3/user/userinfo.json', log='用户信息', params_as_all=True, p_as_all_limit=1, content_type='multipart_form'),
        Api(r'/user/income_ajax', log='收益详情', f_p_arg=['page'], content_type='multipart_form'),

        # 新版答题
        r'/v6/Answer/getData.json',
        r'/v5/answer/first_reward',
        r'/v6/Answer/answer_question.json',
        r'/v5/answer/answer_reward.json',

        # 旧版答题
        # r'WebApi/Answer/getData',
        # r'WebApi/Answer/answer_question',
        # r'WebApi/Answer/answer_reward',
        # r'WebApi/Answer/video_double',
        # r'WebApi/Answer/fill_energy',
    ]
    return App(urls, 'ma-yi-kd')

# ''' 填词小秀才app '''
def app_tian_chi_xiao_xiu_cai():
    ''' 填词小秀才 '''
    urls = [
        Api(r'/x/user/token', log='获取g_token', params_as_all=True),
        Api(r'/x/open/game', log='打开游戏 - 获取ticket', params_as_all=True),
        Api('/api/v1/tczyapp/login', log='填词小秀才 - 获取open_id', f_p_arg=['ticket']),
        Api('/api/v1/tczyapp/sign',log='填词小秀才 - 签到'),
        Api('/api/v1/tczyapp/lottery',log='填词小秀才 - lottery'),
        Api('/api/v1/tczyapp/get_reward',log='填词小秀才 - 任务完成', f_p_arg=['activity_id']),
        Api('/api/v1/tczyapp/open_redpacket',log='填词小秀才 - 红包'),
        Api('/api/v1/tczyapp/draw_a_char',log='填词小秀才 - 抽字'),
        Api('/api/v1/tczyapp/add_coin',log='填词小秀才 - 过关领金币', params_as_all=True),
        
        Api('/api/v1/tczyapp/get_rank',log='填词小秀才 - 判案比赛-排行信息'),
        Api('/api/v1/tczyapp/get_rank_reward',log='填词小秀才 - 判案比赛-领奖'),
        Api('/api/v1/tczyapp/upload_rank',log='填词小秀才 - 判案比赛 - 排行', f_p_arg={'score'}),
        '/api/v1/tczyapp/'
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    return App(urls, 'tian-chi-xiao-xiu-cai')

def app_yang_ji_change():
    ''' 欢乐养鸡场 '''
    urls = [
        Api('/x/middle/open/user/ticket', log='欢乐养鸡场 - 获取s_token'),
        Api('/x/chicken/info', log='欢乐养鸡场 - 信息'),
        Api('/x/chicken/task/take-award', log='达标领奖励'),
        Api('/x/chicken/feed', log='喂饲料'),
        Api('/x/chicken/get-fodder', log='领饲料', f_b_arg={'id','pos','again'}),
        Api('/x/chicken/mood/use-object', log='打赏'),
        '/x/chicken/video/accomplish',
        # 翻翻乐
        Api('/x/middle/flop/info', log='欢乐养鸡场 - 翻翻乐 - 信息'),
        Api('/x/middle/flop/start', log='欢乐养鸡场 - 翻翻乐 - 开始'),
        '/x/middle/flop/',

        # 砸蛋
        Api('/x/chicken/add-hit-count', log='欢乐养鸡场 - 增加砸蛋机会'),
        Api('/x/chicken/hit-egg/award', log='欢乐养鸡场 - 砸蛋 - 领奖', f_b_arg={'again'}),

        '/x/chicken/'
    ]
    urls.extend(api_common())
    return App(urls, 'yang-ji-chang')

# ''' 中青看点 '''
def app_zhong_qin_kd(parameter_list):
    ''' 中青看点 '''
    urls = [
        Api(r'getTimingRedReward.json', f_name='hourly_sign', log='时段签到'),
        r'webApi/AnswerReward/',
        Api(r'/v5/Game/GameVideoReward.json'),
        Api(r'/taskCenter/getAdVideoReward',log='任务中心 - 看视频'),
        Api(r'/WebApi/invite/openHourRed',log='开宝箱', body_as_all=True),
        Api(r'/v5/article/complete.json',log='看视频得金币', f_b_enc={'p'}, f_b_arg={'p'}, content_type='urlencoded_form'),
        Api(r'/WebApi/Task/receiveBereadRed',log='任务中心 - 领红包'),
    ]
    return App(urls, 'zhong-qin-kd')

def app_zhu_lai_le():
    ''' 猪来了 '''
    urls = [
        Api(r'/pig/protocol', log='猪来了'),
    ]
    return App(urls, 'zhu-lai-le')


class Api(object):
    def __init__(self, url, f_name='', log='', api_ok={}, params_as_all=False, p_as_all_limit=50, body_as_all=False, f_p_enc: set=None, f_b_enc: set=None, f_p_arg: list=None, f_p_kwarg: dict=None, f_b_arg: set=None, f_b_kwarg: dict=None, content_type=''):
        self.url = url
        self.url_path = ''
        self.f_name = f_name
        self._name = ''
        self.log = log
        self.api_ok = api_ok

        self.f_p_arg = f_p_arg
        self.f_p_enc = f_p_enc
        if f_p_enc:
            if self.f_p_arg == None:
                self.f_p_arg = list()
            self.f_p_arg.extend(f_p_enc)

        self.f_b_arg = f_b_arg
        self.f_b_enc = f_b_enc
        if f_b_enc:
            if self.f_b_arg == None:
                self.f_b_arg = set()
            self.f_b_arg.update(f_b_enc)

        self.f_p_kwarg = f_p_kwarg
        self.f_b_kwarg = f_b_kwarg
        self.params_as_all = params_as_all
        self.body_as_all = body_as_all
        self.p_as_all_limit = p_as_all_limit
        self.str_d = ''
        # content_type取值'json', 'multipart_form', 'urlencoded_form', 'get'
        self.content_type = content_type

    def __str__(self):
        return f'{self.__class__.__name__}(url={self.url})'

    def _str_fun_params(self):
        s = ''
        if self.f_p_arg and not self.params_as_all:
            s += ", "
            s += ", ".join(self.f_p_arg)

        if self.f_b_arg and not self.body_as_all:
            s += ", "
            s += ", ".join(self.f_b_arg)

        if self.f_p_kwarg and not self.params_as_all:
            for k, v in self.f_p_kwarg.items():
                s += f', {k}={v!r}'

        if self.f_b_kwarg and not self.body_as_all:
            for k, v in self.f_b_kwarg.items():
                s += f', {k}={v!r}'

        if self.params_as_all:
            s += ', params_as_all'
        if self.body_as_all:
            s += ', body_as_all'
        return s

    def str_fun_params(self):
        if not self.str_d:
            self.str_d = self._str_fun_params()
        return self.str_d

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        if not self.f_name:
            self.f_name = name


class App(object):
    def __init__(self, urls, app_name='', api_ok={'code':0}):
        self.app_name = app_name
        self.api_ok = dict()
        self.api_ok['app_ok'] = api_ok
        self.flts = dict()
        for u in urls:
            url = u
            if isinstance(u, Api):
                url = u.url
                if len(u.api_ok):                
                    self.api_ok[url] = u.api_ok
            flt = flowfilter.parse(url)
            self.flts[flt] = u
        self.current_api = None

    def __call__(self, f):
        for flt, api in self.flts.items():
            if flt(f):
                if isinstance(api, str):
                    api = Api(api)
                    self.flts[flt] = api
                self.current_api = api
                return True
        return False

    def add(self, api: Api):
        flt = flowfilter.parse(api.url)
        self.flts[flt] = api


class GenCode(object):
    def __init__(self):
        ctx.log.info('__init__')
        # 设置代码文件生成的目录\文件夹
        self.api_dir = pathlib.Path('/Users/zhoujie/Desktop/api/')
        self.guess_session = collections.OrderedDict(
            ios=re.compile(r'iphone|ios', flags=re.IGNORECASE),
            xiaomi=re.compile(r'xiaomi|mi\+5|miui', flags=re.IGNORECASE),
            huawei=re.compile(r'huawei', flags=re.IGNORECASE),
        )

        self.env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
        self.api_template = self.env.get_template('api_template.j2.py')

        self.headers = {}
        self.params = {}
        self.bodys = {}

        self.params_keys = {}
        self.params_encry = {}
        self.bodys_keys = {}
        self.bodys_encry = {}
        self.params_as_all = dict()
        self.params_as_all_limit = dict()
        self.bodys_as_all = {}

        self.app_apis = {}
        self.app_fn_url = {}
        self.session_hit = set()

        self.appfilters = apps()
        

    def load(self, loader):
        ctx.log.info('event: load')
        loader.add_option(
            name='guess_as_session',
            typespec=str,
            default='default',
            help='若接口不能推断出session,则用这值来设定默认值',
        )

        loader.add_option(
            name='session',
            typespec=str,
            default='',
            help='指定session的值, 不用代码推断',
        )

    def configure(self, updated):
        ctx.log.info('event: configure')

    def running(self):
        ctx.log.info('event: running')
        ctx.log.error('session = ' + ctx.options.session)
        ctx.log.error('guess-as-session = ' + ctx.options.guess_as_session)

    def done(self):
        print('event: done')
        try:
            print('session_hit')
            print(str(self.session_hit))

            sessions_by_app = {}
            # 生成app下的 session_xxx.py
            for device, app in self.session_hit:
                sessions_jinja_data = sessions_by_app.setdefault(app, list())
                sessions_jinja_data.append({
                    'file': f'session_{device}',
                    'session': device,
                })

                hosts = self.headers[device][app]
                for _, d in hosts.items():
                    remove_unnecessary_headers(d)


                var_dict = dict()
                var_dict['session_id'] = device 

                # 设置var_dict['api_ok']
                for item in self.appfilters:
                    if item.app_name == app:
                        api_ok = item.api_ok
                        var_dict['api_ok'] = api_ok

                def abc(data: dict, var_name, var_dict: dict, mergehost=True):
                    try:
                        dd = data[device][app]
                        merge_hosts = {}
                        try:
                            if mergehost:
                                for _, ddd in dd.items():
                                    merge_hosts.update(ddd)
                            else:
                                merge_hosts = dd
                        except:
                            merge_hosts = dd
                        var_dict[var_name] = merge_hosts
                        print(f"生成 App - {app:20} - session_{device}.py {var_name} 成功")
                    except Exception as e:
                        # traceback.print_exc()
                        print(e)
                        var_dict[var_name] = {}
                abc(self.headers, 'header_values', var_dict)
                abc(self.app_fn_url, 'fn_url', var_dict)
                abc(self.params_keys, 'params_keys', var_dict, mergehost=False)
                abc(self.bodys_keys, 'bodys_keys', var_dict, mergehost=False)
                abc(self.params, 'param_values', var_dict)
                abc(self.bodys, 'body_values', var_dict)
                abc(self.params_as_all, 'params_as_all', var_dict)
                abc(self.bodys_as_all, 'bodys_as_all', var_dict)
                abc(self.params_encry, 'params_encry', var_dict)
                abc(self.bodys_encry, 'bodys_encry', var_dict)

                session_xxx_py = self.api_dir.joinpath(app, f'session_{device}.py') 
                from_session = AppSession(var_dict)
                to_session = AppSession(session_xxx_py)

                merge_tool = MergerSession(from_session, to_session)
                merge_tool.merge()
                merge_tool.save_as_file(path=session_xxx_py)

            # 生成app下的 code.py, sessions.py
            for app, apis in self.app_apis.items():
                print(f'生成code - {app}')
                seq = apis.values()

                tfile = f'code_template.j2.py'
                gfile = self.api_dir.joinpath(app, f'code-{app}.py')
                self.gen_file_from_jinja2(tfile, gfile, seq=seq)

                tfile = f'sessions.j2.py'
                gfile = self.api_dir.joinpath(app, 'sessions.py')
                self.gen_file_from_jinja2(tfile, gfile, seq=sessions_by_app[app])

            print('done !!!')
        except Exception as e:
            logging.error('有异常：')
            # print(e)
            # logging.error(e)
            traceback.print_exc()

    def response(self, flow: http.HTTPFlow):
        # 不处理'options'方法的请求
        method = flow.request.method.lower()
        if method == 'options':
            return 

        ft = None
        for i, flt in enumerate(self.appfilters):
            if flt(flow):
                ft = flt
                if not flt == self.appfilters[0]:
                    self.appfilters.pop(i)
                    self.appfilters.insert(0, flt)
                break
        if ft:
            ctx.log.error('|' + '-'*20 + '|') 
            api: Api = ft.current_api
            request: http.HTTPRequest = flow.request

            parse_result = urlparse(request.url)
            url_path = parse_result.path
            if api.url_path and (not api.url_path == url_path):
                api = Api(url_path)
                ft.add(api)

            if len(api.api_ok):
                ft.api_ok[url_path] = api.api_ok

            ctx.log.error(f'触发 App = {ft.app_name}')
            ctx.log.error(f'触发 api = {api} {request.method}')

            function_name = re.sub(r'[./-]', '_', url_path).strip('_').lower()
            api_url = f'{request.scheme}://{request.pretty_host}{url_path}'
            headers_code = self.headers_string(flow)
            params_code = self.params_string(flow)
            data_code = self.data_string(flow, api)

            path = self.api_dir.joinpath(ft.app_name) 
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            with (path/f'{function_name}.text').open('a') as f:

                app_apis = self.app_apis.setdefault(ft.app_name, dict())
                if not function_name in app_apis:
                    api.name = function_name
                    api.url = api_url
                    api.url_path = url_path
                    api.method = request.method.lower()
                    api.content_type = 'json' if 'json' in request.headers.get('content-type','') else ''
                    api.fun_params = api.str_fun_params()
                    if not 'options' == api.method:
                        app_apis[function_name] = api
    
                api.time = time.strftime('%m-%d %H:%M:%S')
                api.headers_code = headers_code
                api.params_code = params_code
                api.data_code = data_code
                api.response = flow.response.text

                code = self.api_template.render(request=api)
                f.write(code)

                device = self._guess_session(flow, api)

                self.gather_params_and_bodys(flow, api, device=device, app=ft.app_name)
                self.session_hit.add((device, ft.app_name))

                d_v = self.app_fn_url.setdefault(device, dict())
                fn_url = d_v.setdefault(ft.app_name, dict())
                fn_url[url_path] = api_url

            ctx.log.error('|' + '-'*20 + '|')

    def headers_string(self, flow: http.HTTPFlow, indent=1):
        d = dict(flow.request.headers)
        return 'headers = {'+json.dumps(d, indent='\t'*(indent+1)).strip('{}') + '\t}'

    def params_string(self, flow: http.HTTPFlow, indent=1):
        d = dict(flow.request.query)
        return 'params = {'+json.dumps(d, indent='\t'*(indent+1)).strip('{}') + '\t}'

    def data_string(self, flow: http.HTTPFlow, api: Api):
        lines = ''

        d = self.dict_from_request_body(flow, api)
        if d:
            for key, value in d.items():
                lines += f"\n\t\t'{key}': {value!r},"

        s = f'''data = {{{lines}\n\t}}'''
        return s

    def gather_params_and_bodys(self, flow: http.HTTPFlow, api: Api, device='', app=''):
        '''
        request.multipart_form: Key and value are bytes. json序列化时会出错：键不能为bytes
        '''
        request: http.HTTPRequest = flow.request

        by_host_device = request.pretty_host
        host = request.pretty_host

        # 收集headers
        d = inner(self.headers, device=device, app=app, host=host)
        d.update(flow.request.headers)

        # 收集params
        d = inner(self.params, device=device, app=app, host=host)
        d.update(flow.request.query)

        # 收集bodys
        bodys_keys = list()
        d = inner(self.bodys, device=device, app=app, host=host)
        body_dict = self.dict_from_request_body(flow, api)
        if body_dict:
            d.update(body_dict)
            bodys_keys = list(body_dict.keys())

        parse_result = urlparse(request.url)
        fname = parse_result.path

        dd = inner(self.bodys_keys, device=device, app=app, host=host)
        dd[fname] = bodys_keys

        d = inner(self.params_keys, device=device, app=app, host=host)
        d[fname] = list(flow.request.query.keys())


        d = inner(self.params_as_all, device=device, app=app, host=host)
        limit = inner_by_list(self.params_as_all_limit, [device, app])
        if api.params_as_all:
            if not api.url_path in d:
                d[api.url_path] = []
                limit[api.url_path] = api.p_as_all_limit
            if api.p_as_all_limit > len(d[api.url_path]):
                d[api.url_path].append(dict(flow.request.query))

        d = inner(self.bodys_as_all, device=device, app=app, host=host)
        if api.body_as_all:
            if not api.url_path in d:
                d[api.url_path] = []
            d[api.url_path].append(dict(body_dict))

        if api.f_p_enc and not api.params_as_all:
            d = inner_by_list(self.params_encry,[device, app, host, api.url_path])
            for k in api.f_p_enc:
                l = d.setdefault(k, list())
                l.append(flow.request.query[k])

        if api.f_b_enc and not api.body_as_all:
            d = inner_by_list(self.bodys_encry,[device, app, host, api.url_path])
            for k in api.f_b_enc:
                l = d.setdefault(k, list())
                l.append(body_dict[k])

    def _gen_file(self, o, f, fold, mode='w'):
        path = fold#pathlib.Path(fold)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        with (path/f).open(mode=mode) as fd:
            json.dump(o, fd, indent=2, sort_keys=True)
            print(f"生成 {f} 成功")

    def _guess_session(self, flow: http.HTTPFlow, api: Api):
        session = ''
        guess_by_data = ''
        request = flow.request

        if ctx.options.session:
            session = ctx.options.session
            ctx.log.error(f'指定为：session = {session}')
            return session

        def guess(data):
            nonlocal guess_by_data, session
            found = False
            for k, v in data:
                for s, r in self.guess_session.items():
                    if r.search(v):
                        session = s
                        guess_by_data = v
                        found = True
                        break
                if found:
                    break

        guess(itertools.chain(request.headers.items(), request.query.items()))
        if not session:
            d = self.dict_from_request_body(flow, api)
            if d:
                guess(d.items())

        ctx.log.error(f'依据值：{guess_by_data}')
        ctx.log.error(f'猜测为：session = {session}')
        if session == '':
            ctx.log.error(f"not guess: {request.url}")
            session = ctx.options.guess_as_session
        return session

    def gen_file_from_jinja2(self, tfile, gfile, **kwargs):
        t = self.env.get_template(tfile)
        ss = t.render(**kwargs)
        with open(gfile, mode='w') as ff:
            ff.write(ss)

    def dict_from_request_body(self, flow: http.HTTPFlow, api: Api):
        d = None
        if api.content_type == 'json':
            try:
                d = json.loads(flow.request.text)
            except:
                pass

        elif api.content_type == 'urlencoded_form' or flow.request.urlencoded_form:
            # 返回的类型是 multidict.MultiDictView
            d = flow.request.urlencoded_form
            api.content_type = 'urlencoded_form'

        elif api.content_type == 'multipart_form' or flow.request.multipart_form:
            ctx.log.error('content-type = multipart_form')
            d = dict()
            for key, value in flow.request.multipart_form.items():
                key = key.decode(encoding='utf-8')
                value = value.decode(encoding='utf-8')
                d[key] = value
            api.content_type = 'multipart_form'

        elif api.content_type == 'get':
            pass

        else:
            # api.content_type没有决定出来：1,没有设置且第1次击中api；2,body没有内容也无法决定content_type；3,get请求一般没有body

            if flow.request.text:
                ctx.log.error('有请求内容')
            else:
                ctx.log.error('没有请求内容')
                if flow.request.method == 'GET':
                    api.content_type = 'get'
                    return d

            try:
                d = json.loads(flow.request.text)
                api.content_type = 'json'
            except:
                pass

        return d

if not __name__ == "__main__": 
    addons = [
        GenCode()
    ]


def merge_data(new_data: dict, old_data: dict, list_append: bool=False, limit:dict=None):
    # Todo: 需要修正，和增强
    for k, v in old_data.items():
        if isinstance(v, dict):
            v.update(new_data.get(k, v))
        elif isinstance(v, list):
            if list_append:
                old_data[k].extend(new_data.get(k, list()))
                old_data[k] = old_data[k][:limit.get(k, 50)]
            else:
                old_data[k] = new_data.get(k, list())
        else:
            old_data[k] = new_data.get(k, v)
    new_data.update(old_data)
    return new_data


def inner(d, device='', app='', host=''):
    d = d.setdefault(device, dict())
    d = d.setdefault(app, dict())
    d = d.setdefault(host, dict())
    return d

def inner_by_list(d, l: list):
    for key in l:
        d = d.setdefault(key, dict())
    return d


def test_jinja():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    t = env.get_template('code_template.j2.py')

    api = Api(r'/mission/intPointReward', f_p_enc={'p_enc'})
    seq = [api]
    code = t.render(seq=seq)
    print(code)

if __name__ == "__main__":
    import shlex
    import subprocess

    test_jinja()
    

    api =Api(r'/mission/intPointReward',params_as_all=False, body_as_all=False,f_p_arg=['p1','p2'], f_b_arg={'b1', 'b2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',f_name='hourly_sign', log='时段签到', params_as_all=False, body_as_all=False,f_p_arg=['p1','p2'], f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    # api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True,f_p_arg=['p1','p2'], f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True)#时段签到
    print(api.str_fun_params())
    api = Api(r'/mission/intPointReward', f_p_enc={'p_enc'})
    print(api.str_fun_params())

    api.name = 'mission_intPointReward'
    api.method = 'post'
    api.content_type = 'json'
    api.fun_params = api.str_fun_params()
    # api.params_as_all = True
    # api.body_as_all = True
    seq = [api]

    template_dir = os.path.dirname(__file__)
    tfile = f'{template_dir}/code_template.j2.py'
    # tfile = f'{template_dir}/api_template.j2.py'
    with open(tfile) as f:
        s = f.read()
        t = Template(s)
        ss = t.render(seq=seq)
        # ss = t.render(request=api)
        # print(ss)
    print('done')
