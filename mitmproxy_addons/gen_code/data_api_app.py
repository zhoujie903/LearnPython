from api_app import Api, App
from merge_rule import *

# r_xxx_yyy_zzz
# d: default, c: common, u: unique, l: limit
r_d = MergeRule()
r_c = common_rule() 
r_u = unique_rule()
r_c_u = chain_rule(r_c, r_u)
r_l_1 = limit_rule(1)
r_c_l1 = chain_rule(r_c,r_l_1) 

def apps():

    flowfilters = [
        # app_zjxsp(),
        # app_bai_du_flash(),
        # app_cai_dan_sp(),
        # app_cheng_yu_da_fu_hao(),
        # app_hao_kan(),
        # app_huo_shan(),
        app_jin_ri_tou_tiao(),
        # app_kai_xin_xiao_tan_guo(),
        # app_ma_yi_kd(),
        # app_qu_jian_pan(),
        # app_qu_jian_pan_flash(),
        # app_qu_zhong_cai(),
        # app_tian_chi_xiao_xiu_cai(),
        # app_wan_zhe_da_nao(),
        # app_yang_ji_chang(),
        # app_you_xi_he_zi(),
        # app_zhong_qin_kd(),
    ]

    return flowfilters



def api_common():
    common = [
        # 游戏
        Api(r'/x/user/token', log='/x/user/token - 获取g_token'),
        Api(r'/x/open/game', log='/x/open/game - 获取ticket', f_p_arg=['app_id']),

        # report_type={round,level} 
        Api('/x/game-report/special_report', log='special_report', f_name='game_special_report',f_b_arg=['app_id'],f_b_kwarg={'report_type':'round'}),
        Api('/x/game-report/duration_report', log='duration_report', f_name='game_duration_report',f_b_arg=['start_ts','duration'],f_b_kwarg={'report_type':'duration_addition'}),
        
        Api('/x/gapp/task/list',log='游戏 - 任务列表', f_b_arg=['app_id', 'app']),
        Api('/x/gapp/task/take-reward',log='游戏 - take-reward - 领金币', f_b_arg=['task_id', 'app_id', 'app']),

        # 金币-取现-账户
        Api('/qapptoken', log='/qapptoken - 获取access_token', f_name='get_access_token', f_p_arg=['app_id']),
        Api('/withdraw/getCoinLog',log='金币明细', f_p_arg=['page','page_size']),
        Api('/withdraw/getBindInfo',log='取现 - 用户账户信息'),
        Api('/withdraw/sku/list',log='取现 - 可取现金额列表'),
        Api('/withdraw/order/create',log='取现 - 取现', f_b_arg=['sku_id']),
        Api('/withdraw/order/listApp',log='取现 - 提现列表'),
        Api('/user/withdraw/days',log='取现 - 条件'),
    ]
    return common

def api_sign():
    urls = [
        Api('/x/game-center/gapp/sign-in', log='签到'),
        Api('/x/game-center/gapp/sign-in-double', log='签到 - double'),
    ]
    return urls

def api_baidu():
    urls = [
        '/activity/acad/bubblead',
        Api(r'/activity/tasks/active', params_as_all=True, f_p_arg=['productid', 'tid']),
        Api(r'/activity/acad/rewardad', f_p_arg=['productid', 'tid'] ),  # 看视频
        Api(r'/activity/tasks/taskreward'),
    ]
    return urls

def api_qu_jian_pan():
    ''' 趣键盘 '''
    urls = [
        r'/qjp-app/user/info',

        # 翻牌
        r'/qjp-app/game/fanpai/basicInfo',
        r'/qjp-app/game/fanpai/getAward',
        r'/qjp-app/game/fanpai/awardDouble',
        r'/qjp-app/game/fanpai/',

        # 储蓄罐
        r'/qjp-app/game/savingsBank/taskInfo',
        r'/qjp-app/game/savingsBank/signIn',
        r'/qjp-app/game/savingsBank/collectPigMoney',
        r'/qjp-app/game/savingsBank/exchangePigMoney',
        Api(r'/qjp-app/game/savingsBank/unlockDouble',f_b_arg=['taskType'], content_type='json'),
        Api(r'/qjp-app/game/savingsBank/finishTask',f_b_arg=['taskCode'], content_type='json'),
        Api(r'/qjp-app/game/savingsBank/doubleBox',f_b_arg=['ticket'], content_type='json'),

        # 小猪刮刮乐
        r'/qjp-app/game/guagua/',

        # 小猪转盘
        r'/qjp-app/pig/turntable/info',
        # type	Integer	3
        r'/qjp-app/pig/turntable/draw',
        Api('/qjp-app/pig/turntable/receiveVideoReward', f_b_arg=['ticket']),
        r'/qjp-app/pig/turntable/',

        #  大转盘
        r'/gk/draw/info',
        r'/gk/draw/extract',
        Api('/gk/draw/double', f_b_arg=['ticket']),
        r'/gk/draw/package',
        r'/gk/draw/pkdouble',

        # 便利店 - 已没有入口
        # Api('/gk/game/bianlidian/receiveBox', f_b_arg=['packageId']),
        # Api('/gk/game/bianlidian/draw/double', f_b_arg=['ticket']),
        # Api('/gk/game/bianlidian/receiveGift', log='便利店 - xxx金币礼包碎片', f_b_arg=['ticket']),
        # Api('/gk/game/bianlidian/receiveMediumCoin', log='便利店 - 随机金币奖励', f_b_arg=['ticket']),
        # r'/gk/game/bianlidian/',

        # 打地鼠 - 已没有入口 
        # r'/gk/game/dadishu/',


        r'/qujianpan/',

        # 已没有入口
        # r'/gk/garbage/',
    ]
    return urls

# ''' 填词小秀才 - 游戏
def api_tczyqtt():
    c_tczyqtt = [
        # 游戏 - 填词小秀才
        Api('/api/v1/tczyqtt/login', log='填词小秀才 - 登录 - 获取open_id', f_p_arg=['ticket'], api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/sign',log='填词小秀才 - 签到'),
        Api('/api/v1/tczyqtt/lottery',log='填词小秀才 - lottery', api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/exchange',log='填词小秀才 - 红包满20元兑换成金币'),
        Api('/api/v1/tczyqtt/get_reward',log='填词小秀才 - 任务完成', f_p_arg=['activity_id'], api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/open_redpacket',log='填词小秀才 - 红包', api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/draw_a_char',log='填词小秀才 - 抽字', api_ok={'code':[1]}),
        Api('/api/v1/tczyqtt/add_coin',log='填词小秀才 - add_coin'),
        '/api/v1/tczyqtt/'
    ]
    return c_tczyqtt

def app_zjxsp():
    '''  '''
    urls = [
        '/user/getallfloatgold',
        Api(r'/user/drawfloatgold', f_p_arg=['floatGoldId']), 
    ]
    urls.extend(api_baidu())
    return App(urls, 'zjxsp')

# ''' 百度 - 百度极速版 '''
def app_bai_du_flash():
    ''' 百度 - 百度极速版 '''
    urls = [
        Api(r'/api/task/1/task/381/complete', f_p_arg=['rewardVideoPkg']), # 看视频
    ]
    urls.extend(api_baidu())
    return App(urls, 'bai-du-flash')

# ''' 百度 - 好看 '''
def app_hao_kan():
    ''' 百度 - 好看 '''
    urls = [
        r'activity/acusercheckin',  # 每日签到
        r'signIn/new/sign',  # 游戏中心签到
        Api(r'api/task/1/task/379/complete', f_p_arg=['rewardVideoPkg']), # 看视频
    ]
    urls.extend(api_baidu())
    return App(urls, 'hao-kan')

# ''' 彩蛋视频 '''
def app_cai_dan_sp():
    ''' 彩蛋视频 '''
    urls = [
        Api('/h5/task/index',log='任务信息'),
        Api('/task/sign',log='sign - 签到、金币信息'),
        Api('/task/timer_submit',log='看视频 - 得金币', f_b_enc={'qdata'}, f_b_arg=['qdata'], f_merge_key=r_u),
        
        Api('/h5/task/submit',log='日常福利 - 观看小视频', body_as_all=True, f_merge_key=r_d),
        Api('/h5/reduce/reward',log='瓜分他人金币', body_as_all=True, f_merge_key=r_d),
        Api('/h5/reward/prize',log='iphone免费抽', body_as_all=True, f_merge_key=r_d),
        Api('/h5/active_value/reward_prize',log='活跃奖励', body_as_all=True, f_merge_key=r_d),
    ]
    urls.extend(api_common())
    return App(urls, 'cai-dan-sp')

# ''' 成语大富豪
def app_cheng_yu_da_fu_hao():
    urls = [
        Api('/x/cocos/gapp-game-init', params_as_all=True, f_merge_key=r_c_l1),#返回的url中含有ticket
        Api('/api/Login', log='2-登录游戏', f_name='api_login', f_b_arg=['ticket','game_id']),
        Api('/api/GetQCoin', log='获取金币数', f_b_arg=['session_id']),
        Api('/api/AddCoin', log='成语大富豪 - 金币',f_b_arg=['AddCoinNum','session_id']),
        Api('/api/AddSecondCoin', log='成语大富豪 - 金币 - AddSecondCoin',f_b_arg=['AddCoinNum','session_id']),
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    return App(urls, 'cheng-yu-da-fu-hao')

    
# ''' 火山极速版 '''
def app_huo_shan():
    ''' 火山极速版 '''
    urls = [
        Api('/luckycat/hotsoon/v1/task/done/excitation_ad_treasure_box', log='火山-开宝箱-看视频', f_name='task_done_excitation_ad_treasure_box'),

        Api('/luckycat/hotsoon/v1/task/page', log='火山-获取任务状态'),
        Api('/luckycat/hotsoon/v1/task/done/treasure_task', log='火山-开宝箱'),
        Api('/luckycat/hotsoon/v1/task/done/show_money', log='火山-晒收入', params_as_all=True),
        Api('/luckycat/hotsoon/v1/task/done/excitation_ad', log='火山-看视频赚海量金币', params_as_all=True),
        Api('/luckycat/hotsoon/v1/task/done/daily_read_1m', log='火山-1分钟', params_as_all=True),
        Api('/luckycat/hotsoon/v1/task/done/daily_read_2m', log='火山-2分钟', params_as_all=True),
        Api('luckycat/v1/task/page/', log='火山-获取任务状态', params_as_all=True, f_merge_key=r_c_l1),
        Api('luckycat/v1/task/sign_in/', log='火山-每日签到', params_as_all=True, f_merge_key=r_c_l1),
        Api('luckycat/v1/task/open_treasure_box/', log='火山-开宝箱', params_as_all=True),
        Api('luckycat/v1/task/done_task/', log='火山-开宝箱-看视频', params_as_all=True, body_as_all=True),
        Api('luckycat/v1/landing/add_amount/', log='火山-晒收入', params_as_all=True),
        Api('luckycat/v1/task/get_read_bonus/',params_as_all=True),
        Api('api/ad/v1/inspire/', log='火山-获取广告', params_as_all=True),
    ]
    return App(urls, 'huo-shan', api_ok={'code':[0],'err_no':[0]})

# ''' 开心消糖果 '''
def app_kai_xin_xiao_tan_guo():
    ''' 开心消糖果 '''
    urls = [
        Api('/x/cocos/gapp-game-init', params_as_all=True, f_merge_key=r_c_l1),#返回的url中含有ticket
        Api('/happy/qtt/apkuserinfo', log='/happy/qtt/apkuserinfo - 获取open_id', f_p_arg=['ticket']),
        '/happy/protocol'
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    return App(urls, app_name='kai-xin-xiao-tan-guo')

# ''' 趣键盘 '''
def app_qu_jian_pan():
    ''' 趣键盘 '''
    urls = [
    ]
    urls.extend(api_qu_jian_pan())
    return App(urls, 'qu-jian-pan')

# ''' 趣键盘极速版 '''
def app_qu_jian_pan_flash():
    ''' 趣键盘极速版 '''
    urls = [
    ]
    urls.extend(api_qu_jian_pan())
    return App(urls, 'qu-jian-pan-flash')

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
def app_you_xi_he_zi():
    ''' 金猪游戏盒子 '''
    urls = [
        # 游戏           
        Api('/x/task/v3/list', log='游戏任务列表'),
        Api('/x/cash/time-bonus/info', log='时段金币 - 信息'),
        Api('/x/cash/time-bonus/get', log='时段金币 - 领取', f_b_arg=['index']),
        Api('/x/cash/task-bonus/get', log='红包 - 领取', f_p_arg=['cnt']),
        Api('/x/cash/daily-bonus/get', log='签到 - 奖励', body_as_all=True, f_merge_key=r_c_l1),
        Api('/x/task/v2/take-reward', log='任务完成 - 领金币', f_name='game_take_reward',f_b_arg=['task_id']),


        # 抽奖 - 游戏嘉年华
        r'/x/raffle/detail',
        r'/x/raffle/roll',
        r'/x/raffle/add-times',
        
        # 金猪 withdraw:(从银行)取钱 
        r'/x/v1/goldpig/info',
        r'/x/v1/goldpig/foundLostPig', # 金猪 - 找回金猪
        r'/x/v1/goldpig/bubbleWithdraw',  # 金猪 - 看视频
        r'/x/v1/goldpig/withdraw',  # 金猪

        # 游戏 - 成语大富豪
        Api('qttgame.midsummer.top/api/Login', log='2-登录游戏', f_name='api_login', f_b_arg=['ticket','game_id']),
        Api('qttgame.midsummer.top/api/AddCoin', log='成语大富豪 - 金币',f_b_arg=['AddCoinNum','session_id']),

        # 游戏 - 成语消消乐
        Api('/chengyu/login', log='成语消消乐 - 登录 - 获取open_id', f_b_arg=['ticket']),
        Api('/chengyu/addcoin', log='成语消消乐 - 金币', f_b_arg=['add_num']),
        Api('/chengyu/update_red_packet', log='成语消消乐 - 过关得现金', f_b_arg=['level']),
        
        # 游戏 - 切菜
        Api('/x/open/coin/add', log='切菜 - 金币', body_as_all=True, f_merge_key=chain_rule(sort_rule(lambda item: int(item['coin_num']), reverse=True),r_u)),
        
        # 游戏 - 糖果
        Api(r'/happy/qtt/userinfo', log='游戏 - 糖果 - 获取open_id', f_p_arg=['ticket']),
        Api(r'/happy/protocol', log='游戏 - 糖果 - 获取金币', f_b_arg=['data']),

        # 游戏 - 钓鱼
        Api(r'/qtt/coin/withdraw', log='游戏 - 钓鱼 - 获取金币'),            

        # 游戏 - 王者大脑
        Api('/api/v1/z6h5/login', log='王者大脑 - 获取open_id', f_p_arg=['ticket']),
        Api('/api/v1/z6h5/sign',log='王者大脑 - 签到'),
        Api('/api/v1/z6h5/lottery',log='王者大脑 - lottery'),
        Api('/api/v1/z6h5/exchange',log='王者大脑 - 红包满20元兑换成金币'),
        Api('/api/v1/z6h5/get_reward',log='王者大脑 - 任务完成', f_p_arg=['activity_id']),
        Api('/api/v1/z6h5/open_redpacket',log='王者大脑 - 红包'),
        Api('/api/v1/z6h5/add_coin',log='王者大脑 - add_coin', params_as_all=True, f_merge_key=r_u),
        Api('/api/v1/z6h5/get_rank',log='王者大脑 - 判案比赛-排行信息'),
        Api('/api/v1/z6h5/get_rank_reward',log='王者大脑 - 判案比赛-领奖'),
        Api('/api/v1/z6h5/upload_rank',log='王者大脑 - 判案比赛 - 排行', f_p_arg=['score']),        
        '/api/v1/z6h5/',
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    urls.extend(api_tczyqtt())
    return App(urls, 'you-xi-he-zi')

# ''' 今日头条 '''
def app_jin_ri_tou_tiao():
    ''' 今日头条 '''
    urls = [
        Api('/task/page_data/', f_name='task_page_data'),            
        Api('/score_task/v1/task/sign_in/', f_name='task_sign_in'),            
        Api('/score_task/v1/task/open_treasure_box', f_name='task_open_treasure_box'),            
        Api('/score_task/v1/task/new_excitation_ad', f_name='task_new_excitation_ad', f_b_arg=['task_id'], params_as_all=True),            
        Api('/score_task/v1/task/get_read_bonus/', f_name='task_get_read_bonus', params_as_all=True, f_p_arg=['group_id'], f_merge_key=r_c_l1),            

        # 全场景计时器
        Api('/activity/done_whole_scene_task/', f_name='done_whole_scene_task', params_as_all=True, f_b_arg=['group_id'], f_merge_key=r_c_l1),            
        # 'score_task/v1/task/done_task/',
        # 'score_task/v1/landing/add_amount/',
        # 'score_task/v1/user/profit_detail/',

        # # 小说
        Api('/api/novel/book/directory/list/v1', log='书目录', f_p_arg=['book_id']),  
        Api('score_task/v1/novel/bonus/', f_b_arg=['item_id'], params_as_all=True, f_merge_key=r_c_l1),  # 读小说得金币

        # # 搜索 
        # 'search/suggest/homepage_suggest/',
        # 'search/suggest/initial_page/',
        # 'api/search/content/',
        # Api('/search/', log='搜索', f_p_arg=['keyword']),

        # # 走咯
        Api(r'score_task/v1/walk/count/', f_b_arg=['count']),
        r'score_task/v1/walk/',

        # # 睡觉
        'score_task/v1/sleep/status/',
        'score_task/v1/sleep/start/',
        'score_task/v1/sleep/stop/',
        'score_task/v1/sleep/done_task/',  # 睡觉领金币

        # # 农场
        Api('/ttgame/game_farm/home_info', f_name='farm_home_info', api_ok={'status_code':[0]}),            
        r'/ttgame/game_farm/',

        # # 吃
        r'/luckycat/lite/v1/eat/eat_info/',
        r'/luckycat/lite/v1/eat/done_eat/',
        # r'score_task/lite/v1/eat/eat_info/',
        # r'score_task/lite/v1/eat/done_eat/',

        'api/news/feed/v47/',  # 安卓视频tab页
        # 'api/news/feed/v64/',  # ios视频tab页
        
        # # 'score_task/v1',
        # 'score_task/v2',
    ]
    return App(urls, 'jin-ri-tou-tiao', api_ok={'code':[0],'err_no':[0],'message':['success']})

def app_ma_yi_kd():
    # 蚂蚁看点
    urls = [
        Api(r'article/treasure_chest', log='时段签到', f_name='hourly_sign', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/user/shai_income_task_award',log='晒收'),
        Api(r'TaskCenter/daily_sign', log='每日签到',f_name='daily_sign'),

        # 重点：看广告、看小视频、看文章
        Api(r'/v5/user/rewar_video_callback.json', log='视频广告 - 得金币', f_name='rewar_video_callback', f_b_enc={'p'}, f_merge_key=chain_rule(limit_rule(20),r_u),content_type='multipart_form'),
        Api(r'/v5/article/haotu_video.json',log='看视频 - 得金币', f_name='haotu_video',f_b_enc={'p'}, f_merge_key=chain_rule(limit_rule(20),r_u),content_type='multipart_form'),
        Api(r'/v5/article/complete_article',log='读文章 - 得金币', f_name='complete_article', f_b_enc={'p'}, f_merge_key=chain_rule(limit_rule(20),r_u),content_type='multipart_form'),

        # 2020-11-02
        Api('/WebApi/share/share_task_score',log='分享文章赚钱 - 每日免费领金币 - 间隔30分钟',f_name='share_task_score'),
        Api(r'/v3/user/userinfo.json', log='用户信息', f_name='userinfo', params_as_all=True, f_merge_key=r_c_l1, content_type='multipart_form'),

        # 提现相关
        Api('/WapPage/user_order_list',log='提现记录',f_name='ti_xian_history'),
        Api('/v3/cash/wechat.json',log='提现',f_name='ti_xian',f_merge_key=chain_rule(r_u, SortRule(key=lambda item: item['money'],reverse=True)), body_as_all=True, content_type='multipart_form'),
        Api('/WebApi/Exchange/getuserinfo', log='金币信息'),
        Api('/WebApi/Exchange/user_exchange_info', log='可提现项目'),


        # r'WebApi/',
        r'WebApi/Stage/task_reward',
        r'WapPage/get_video_status',

        # 装盘
        r'/WebApi/RotaryTable/turn_rotary_new',
        r'/WebApi/RotaryTable/turn_reward',
        r'/WebApi/RotaryTable/video_double',
        r'/WebApi/RotaryTable/chestReward',
        '/WebApi/RotaryTable/',

        # 睡觉
        Api(r'/WebApi/sleep/sleep_start',log='睡觉 - 开始'),
        Api(r'/WebApi/sleep/get_sleep_score',log='睡觉 - 醒来'),

        Api(r'/v5/article/complete_welfare_score.json', log='福袋 - 得金币', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/user/adlickstart.json',log='点击广告领金币 - 开始', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/user/adlickend.json',log='点击广告领金币 - 结束', f_b_enc={'p'}, content_type='multipart_form'),
        Api(r'/v5/user/task_second_callback.json',f_b_enc={'p'}, content_type='multipart_form'),
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
    return App(urls, 'ma-yi-kd', api_ok={'error_code':['0'],'status':[1]})

# ''' 填词小秀才app '''
def app_tian_chi_xiao_xiu_cai():
    ''' 填词小秀才 '''
    urls = [
        Api('/api/v1/tczyapp/login', log='填词小秀才 - 获取open_id', f_p_arg=['ticket']),
        Api('/api/v1/tczyapp/sign',log='填词小秀才 - 签到'),
        Api('/api/v1/tczyapp/lottery',log='填词小秀才 - lottery'),
        Api('/api/v1/tczyapp/exchange',log='填词小秀才 - 红包满20元兑换成金币'),
        Api('/api/v1/tczyapp/get_reward',log='填词小秀才 - 任务完成', f_p_arg=['activity_id']),
        Api('/api/v1/tczyapp/open_redpacket',log='填词小秀才 - 红包'),
        Api('/api/v1/tczyapp/draw_a_char',log='填词小秀才 - 抽字'),
        Api('/api/v1/tczyapp/add_coin',log='填词小秀才 - add_coin', params_as_all=True, f_merge_key=r_u),
        
        Api('/api/v1/tczyapp/get_rank',log='填词小秀才 - 判案比赛-排行信息'),
        Api('/api/v1/tczyapp/get_rank_reward',log='填词小秀才 - 判案比赛-领奖'),
        Api('/api/v1/tczyapp/upload_rank',log='填词小秀才 - 判案比赛 - 排行', f_p_arg=['score']),
        '/api/v1/tczyapp/'
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    return App(urls, 'tian-chi-xiao-xiu-cai')

# ''' 王者大脑app '''
def app_wan_zhe_da_nao():
    urls = [
        Api('/api/v1/z6qtt/login', log='王者大脑 - 获取open_id', f_p_arg=['ticket']),
        Api('/api/v1/z6qtt/sign',log='王者大脑 - 签到'),
        Api('/api/v1/z6qtt/lottery',log='王者大脑 - lottery'),
        Api('/api/v1/z6qtt/exchange',log='王者大脑 - 红包满20元兑换成金币'),
        Api('/api/v1/z6qtt/get_reward',log='王者大脑 - 任务完成', f_p_arg=['activity_id']),
        Api('/api/v1/z6qtt/open_redpacket',log='王者大脑 - 红包'),
        Api('/api/v1/z6qtt/add_coin',log='王者大脑 - add_coin', params_as_all=True, f_merge_key=r_u),
        
        Api('/api/v1/z6qtt/get_rank',log='王者大脑 - 判案比赛-排行信息'),
        Api('/api/v1/z6qtt/get_rank_reward',log='王者大脑 - 判案比赛-领奖'),
        Api('/api/v1/z6qtt/upload_rank',log='王者大脑 - 判案比赛 - 排行', f_p_arg=['score']),
        '/api/v1/z6qtt/'
    ]
    urls.extend(api_common())
    urls.extend(api_sign())
    return App(urls, 'wan-zhe-da-nao')

# ''' 欢乐养鸡场app '''
def app_yang_ji_chang():
    ''' 欢乐养鸡场 '''
    urls = [
        Api('/x/middle/open/user/ticket', log='欢乐养鸡场 - 获取s_token'),
        Api('/x/chicken/info', log='欢乐养鸡场 - 信息'),
        Api('/x/chicken/task/take-award', log='达标领奖励'),
        Api('/x/chicken/feed', log='喂饲料'),
        Api('/x/chicken/get-fodder', log='领饲料', f_b_arg=['id','pos','again']),
        Api('/x/chicken/mood/use-object', log='打赏'),
        '/x/chicken/video/accomplish',
        # 翻翻乐
        Api('/x/middle/flop/info', log='欢乐养鸡场 - 翻翻乐 - 信息'),
        Api('/x/middle/flop/start', log='欢乐养鸡场 - 翻翻乐 - 开始'),
        '/x/middle/flop/',

        # 砸蛋
        Api('/x/chicken/add-hit-count', log='欢乐养鸡场 - 增加砸蛋机会'),
        Api('/x/chicken/hit-egg/award', log='欢乐养鸡场 - 砸蛋 - 领奖', f_b_arg=['again']),

        '/x/chicken/'
    ]
    urls.extend(api_common())
    return App(urls, 'yang-ji-chang')

# ''' 中青看点 '''
def app_zhong_qin_kd():
    ''' 中青看点 '''
    urls = [
        Api('/TaskCenter/sign',log='每日签到',f_name='dayly_sign'),
        Api(r'/WebApi/TimePacket/getReward', f_name='time_packet', log='计时红包'),
        r'/webApi/AnswerReward/',
        Api(r'/v5/Game/GameVideoReward.json', log='2次可选领取 - 看广告视频', f_b_enc={'p'},f_merge_key=r_u),
        Api(r'/taskCenter/getAdVideoReward',log='任务中心 - 看视频'),

        # 重点api
        Api(r'/v5/article/complete.json',log='看视频或看文章得金币', f_b_enc={'p'}, f_b_arg=['p'], f_merge_key=r_c_u, content_type='urlencoded_form'),
        Api(r'/withdraw/getOrderList', log='提现记录', f_name='ti_xian_history'),

        # 相当 时段签到
        Api(r'/v5/CommonReward/toGetReward.json',log='可领取 - ', f_b_enc={'p'}, f_b_arg=['p'], f_merge_key=r_c_u),
        Api(r'/v5/CommonReward/toDouble.json',log='可领取 - 双倍', f_b_enc={'p'}, f_b_arg=['p'], f_merge_key=r_c_u),
        Api(r'/WebApi/Task/receiveBereadRed',log='任务中心 - 领红包'),

        Api(r'/WebApi/EverydayShare/share_back',log='每日分享奖励', f_b_arg=['uid'], ),

        # 天天抽奖
        '/WebApi/RotaryTable/turnRotary',
        '/WebApi/RotaryTable/',

        Api('/wap/user/balance', log='用户金币数量'),
        # 旧版
        # Api(r'/WebApi/invite/openHourRed',log='开宝箱', body_as_all=True),
        # Api(r'getTimingRedReward.json', log='时段签到', f_name='hourly_sign', ),
    ]
    return App(urls, 'zhong-qin-kd')

def helper_app_from_path(from_or_to_path: str) -> App:
    
    for k, v in globals().items():
        if k.startswith('app_') and isinstance(v, type(apps)):
            new_name = k.replace('app_', '')
            new_name = new_name.replace('_', '-')
            if new_name in from_or_to_path:
                return v()

def helper_health_check():
    pass
    
    no_merge_rule = {}
    for app in apps():
        a: App = app

        it = filter(lambda item: isinstance(item[1], Api), a.url_a_dict.items())
        for _, apii in it:
            api: Api = apii            
            if api.f_b_enc or api.f_p_enc or api.params_as_all or api.body_as_all:
                if api.f_merge_key == None:
                    l = no_merge_rule.setdefault(a.app_name, [])                    
                    l.append(api)

    if len(no_merge_rule):
        print('没有配置 f_merge_key')
        for app_name, apis in no_merge_rule.items():
            for api in apis:
                print(f'\t{app_name}\t{api.url}')


if __name__ == "__main__":
    # helper_app_from_path('/Users/zhoujie/Desktop/dev/tian-chi-xiao-xiu-cai/session_huawei.py')

    # 场景: apps()排序
    for k, v in sorted(globals().items(), key=lambda item: item[0]):
        print(f'{k}(),')

    # helper_health_check()
