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
        # self.kai_xin_da_ti,
        # self.qu_jian_pan,
        # self.yang_ji_chang,
        # app_you_xi_he_zhi(),
        # self.zhong_qin_kd,
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

        # 金币-取现-账户
        Api('/qapptoken', log='获取access_token', f_name='get_access_token', f_p_arg=['app_id']),
        Api('/withdraw/getCoinLog',log='金币明细', f_p_arg=['page','page_size']),
        Api('/withdraw/getBindInfo',log='取现 - 用户账户信息'),
        Api('/withdraw/sku/list',log='取现 - 可取现金额列表'),
        Api('/withdraw/order/create',log='取现 - 取现', f_b_arg={'sku_id'}),
        Api('/user/withdraw/days',log='取现 - 条件'),
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
        Api(r'/task/timer_submit',log='看视频 - 得金币', f_b_enc={'qdata'}, f_b_arg={'qdata'}, f_merge_key=r_d),
        Api(r'/h5/task/submit',log='日常福利 - 观看小视频', body_as_all=True),
        Api(r'/h5/reduce/reward',log='瓜分他人金币', body_as_all=True),
        r'/h5/bubble/prize',
        Api('/h5/reward/prize',log='iphone免费抽'),
        Api('/qapptoken', log='获取access_token'),
        Api('/withdraw/getCoinLog',log='彩蛋视频 - 金币明细', f_p_arg=['page','page_size']),
        Api('/withdraw/order/listApp',log='彩蛋视频 - 提现列表'),
        Api('/withdraw/order/create',log='彩蛋视频 - 提现', f_b_arg=['sku_id']),
    ]
    urls.extend(api_common())
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

# ''' 填词小秀才 - 游戏
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
        Api(r'/mission/intPointReward', log='时段签到', params_as_all=True, api_ok={'code':[-312]}, f_merge_key=r_c_l1),
        Api(r'/taskcenter/getReward', log='任务完成 - 领金币', params_as_all=True, f_merge_key=r_c_l1),
        r'/x/game-center/user/sign-in',
        r'/x/game-center/user/last-sign-coin',
        Api('/x/game-report/special_report', log='special_report', f_name='game_do_task',f_b_arg={'app_id'},f_b_kwarg={'report_type':'round'}),
        Api('/x/game-report/duration_report', log='duration_report', f_name='game_duration_report',f_b_arg={'start_ts','duration'},f_b_kwarg={'report_type':'duration_addition'}),
        Api('/x/task/v2/take-reward', log='任务完成 - 领金币', f_name='game_take_reward',f_b_arg={'task_id'}),
        r'/newuserline/activity/signRewardNew',  # 挑战签到
        Api(r'/mission/receiveTreasureBox', log='趣头条-开宝箱', api_ok={'code':[-1710]}),
        Api(r'/content/readV2',params_as_all=True),
        Api(r'/app/re/taskCenter/info/v1/get', log='任务信息', params_as_all=True, p_as_all_limit=1, f_merge_key=r_c_l1),
        Api(r'/app/user/info/personal/v1/get', log='用户信息', params_as_all=True, p_as_all_limit=1, f_merge_key=r_c_l1),
        Api(r'/coin/service', body_as_all=True),
        r'readtimer/report',
        # Api(r'motivateapp/mtvcallback', params_as_all=True),
        Api(r'/x/feed/getReward', log='信息流-惊喜红包', params_as_all=True, api_ok={'code':[-308]}, f_merge_key=r_c_l1),
        Api(r'/lotteryGame/status', log='天天乐-信息'),
        Api(r'/tiantianle/video', log='天天乐-增加机会', params_as_all=True, f_merge_key=r_c_l1),
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
        Api(r'/x/open/coin/add', body_as_all=True, f_merge_key=chain_rule(sort_rule(lambda item: int(item['coin_num']), reverse=True),r_u)),

        # 游戏 - 糖果
        Api(r'/happy/qtt/userinfo', log='游戏 - 糖果 - 获取open_id', f_p_arg=['ticket']),
        Api(r'/happy/protocol', log='游戏 - 糖果 - 获取金币', f_b_arg={'data'}),            

        # 游戏 - 钓鱼
        Api(r'/xyx_sdk/gw/partner_login', log='游戏 - 钓鱼 - 登录', body_as_all=True, f_merge_key=r_c_l1),            
        Api(r'/qtt/coin/withdraw', log='游戏 - 钓鱼 - 获取金币'),            

        # 游戏 - 大脑
        Api(r'/api/v1/z6h5/sign', log='游戏 - 大脑 - 签到'),            
        Api(r'/api/v1/z6h5/lottery', log='游戏 - 大脑 - 获取红包'),            

        Api(r'/press_trigger',log='幸运大转盘'),

        # 金猪
        Api(r'/actcenter/piggy/videoConfirm',log='合成金猪 - 气泡', f_p_arg=['tag']),
        r'/actcenter/piggy/',

        Api(r'/member/getMemberIncome',log='收益详情', f_p_arg=['page','last_time']),
        Api(r'/search/searchContentNew',log='搜索内容得金币', params_as_all=True, p_as_all_limit=3, f_merge_key=chain_rule(r_c, limit_rule(3))),
        
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
        Api('/x/cash/time-bonus/info', log='时段金币 - 信息'),
        Api('/x/cash/time-bonus/get', log='时段金币 - 领取', f_b_arg={'index'}),
        # Api('/x/cash/task-bonus/amount', log='红包 - 领取', f_p_arg={'cnt'}),
        Api('/x/cash/task-bonus/get', log='红包 - 领取', f_p_arg={'cnt'}),
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
