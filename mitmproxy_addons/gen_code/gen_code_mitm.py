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

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy import http

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

'''
生成接口python代码
mitmdump --flow-detail 0 --set session='huawei' -s "/Users/zhoujie/Documents/zhoujie903/LearnScrapy/mitmproxy_addons/gen_code/gen_code_mitm.py" 
'''


class Api(object):
    def __init__(self, url, f_name='', log='', params_as_all=False, p_as_all_limit=50, body_as_all=False, f_p_enc: set=None, f_b_enc: set=None, f_p_arg: set=None, f_p_kwarg: dict=None, f_b_arg: set=None, f_b_kwarg: dict=None, content_type=''):
        self.url = url
        self.url_path = ''
        self.f_name = f_name
        self._name = ''
        self.log = log

        self.f_p_arg = f_p_arg
        self.f_p_enc = f_p_enc
        if f_p_enc:
            if self.f_p_arg == None:
                self.f_p_arg = set()
            self.f_p_arg.update(f_p_enc)

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
        return f'Api(url={self.url})'

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
    def __init__(self, urls, app_name=''):
        self.app_name = app_name
        self.flts = dict()
        for u in urls:
            url = u
            if isinstance(u, Api):
                url = u.url
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

        # 今日头条
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
        self.toutiao = App(urls, 'jin-ri-tou-tiao')

        # 火山极速版
        urls = [
            'luckycat/v1/task/page/',
            'luckycat/v1/task/sign_in/',
            'luckycat/v1/task/open_treasure_box/',
            'luckycat/v1/task/done_task/',
            'luckycat/v1/landing/add_amount/',
            'luckycat/v1/task/get_read_bonus/',
        ]
        self.huoshan = App(urls, 'huo-shan')

        # 趣头条小视频
        urls = [
            Api(r'seafood-api.1sapp.com/v1/readtimer/report',log='看视频得金币', f_b_enc={'qdata'}, f_b_arg={'qdata'})
        ]
        self.qtt_video = App(urls, 'qtt-video')

        # 趣头条
        urls = [
            r'sign/sign',  # 每日签到
            Api(r'/mission/intPointReward', log='时段签到', params_as_all=True),
            r'/x/game-center/user/sign-in',
            r'/x/game-center/user/last-sign-coin',
            r'/newuserline/activity/signRewardNew',  # 挑战签到
            r'/mission/receiveTreasureBox',
            Api(r'/content/readV2',params_as_all=True),
            Api(r'/app/re/taskCenter/info/v1/get',params_as_all=True, p_as_all_limit=1),
            # r'taskcenter/getListV2',#旧版本 tab页：任务
            # r'api-coin-service.aiclk.com/coin/service',
            Api(r'/coin/service', body_as_all=True),
            r'readtimer/report',
            Api(r'motivateapp/mtvcallback', params_as_all=True),
            Api(r'x/feed/getReward', log='信息流-惊喜红包', params_as_all=True),
            r'x/v1/goldpig/bubbleWithdraw',  # 金猪 - 看视频
            r'x/v1/goldpig/withdraw',  # 金猪
            r'finance/piggybank/taskReward',  # 存钱罐

            r'x/tree-game/task-list',
            r'x/tree-game/left-plant-num',
            r'x/tree-game/plant-ok',
            r'x/tree-game/add-plant',
            r'x/tree-game/fertilizer/add',
            r'x/tree-game/fertilizer/use',
            r'x/tree-game/water-plants',
            r'x/tree-game/my-gift-box/draw-lottery',
            r'x/tree-game/my-gift-box/receive-prize',
            # r'x/tree-game/',

            r'x/open/game',
            r'x/task/encourage/activity/grant',  # 游戏 - 瓜分
            r'/api/Login',
            r'api/loginGame',
            r'api/qttAddCoin',
            r'api/AddCoin',  # 游戏 - 成语

            #游戏 - 切菜
            Api(r'/x/open/coin/add', body_as_all=True),

            # 金猪
            Api(r'/actcenter/piggy/videoConfirm',log='合成金猪 - 气泡', f_p_arg={'tag'}),
            r'/actcenter/piggy/',
        ]
        self.qu_tou_tiao = App(urls, 'qu-tou-tiao')

        # 百度 - 好看
        urls = [
            r'activity/acusercheckin',  # 每日签到
            r'signIn/new/sign',  # 游戏中心签到

            '/activity/acad/bubblead',
            Api(r'/activity/tasks/active', params_as_all=True, f_p_kwarg={'productid':1, 'tid':404}),
            Api(r'activity/acad/rewardad', params_as_all=True, f_p_kwarg={'productid':1, 'tid':404} ),  # 看视频
            Api(r'api/task/1/task/379/complete', f_p_arg={'rewardVideoPkg'}), # 看视频
            '/activity/tasks/taskreward',
        ]
        self.hao_kan = App(urls, 'hao-kan')

        # 百度 - 全民小视频
        urls = [
            r'mvideo/api',  # 每日签到
        ]
        self.quan_ming = App(urls, 'quan-ming')

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

            # 新版答题
            r'/v6/Answer/getData.json',
            r'/v5/answer/first_reward',
            r'/v6/Answer/answer_question.json',
            r'/v5/answer/answer_reward.json',

            Api(r'/WebApi/sleep/sleep_start',log='睡觉 - 开始'),
            Api(r' /WebApi/sleep/get_sleep_score',log='睡觉 - 醒来'),

            Api(r'article/haotu_video',log='看视频得金币', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'article/complete_article',log='读文章得金币', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'/v5/user/rewar_video_callback', log='视频广告 - 得金币', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'/v5/article/complete_welfare_score.json', log='福袋 - 得金币', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'/v5/user/adlickstart.json',log='点击广告领金币 - 开始', f_b_enc={'p'}, content_type='multipart_form'),
            Api(r'/v5/user/adlickend.json',log='点击广告领金币 - 结束', f_b_enc={'p'}, content_type='multipart_form'),

            # 旧版答题
            r'WebApi/Answer/getData',
            r'WebApi/Answer/answer_question',
            r'WebApi/Answer/answer_reward',
            r'WebApi/Answer/video_double',
            r'WebApi/Answer/fill_energy',
        ]
        self.ma_yi_kd = App(urls, 'ma-yi-kd')

        # 中青看点
        urls = [
            Api(r'getTimingRedReward.json', f_name='hourly_sign', log='时段签到'),
            r'webApi/AnswerReward/',
            Api(r'/v5/Game/GameVideoReward.json'),
            Api(r'/taskCenter/getAdVideoReward',log='任务中心 - 看视频'),
            Api(r'/WebApi/invite/openHourRed',log='开宝箱', body_as_all=True),
            Api(r'/v5/article/complete.json',log='看视频得金币', f_b_enc={'p'}, f_b_arg={'p'}, content_type='urlencoded_form'),
            Api(r'/WebApi/Task/receiveBereadRed',log='任务中心 - 领红包'),
        ]
        self.zhong_qin_kd = App(urls, 'zhong-qin-kd')

        # 东方头条
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
        self.dftt = App(urls, 'dong-fan-tt')

        # 彩蛋视频
        urls = [
            r'task/timer_submit',
            r'/h5/task/submit',
            r'/h5/bubble/prize',
        ]
        self.cai_dan_sp = App(urls, 'cai-dan-sp')

        urls = [
            r'/login/index',
            r'/main/index',
            r'/card/info',
            r'/card/open',
            r'/card/doublereward',
        ]
        self.kai_xin_da_ti = App(urls, 'kai-xin-da-ti')

        # 趣键盘
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
        self.qu_jian_pan = App(urls, 'qu-jian-pan')

        # 趣种菜
        urls = [
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
            # '/x/tree-game/gapp/pool/',
            # 兔子
            '/x/tree-game/gapp/activity/rabbit/',
            Api('/x/tree-game/gapp/activity/carrot/take-reward', log='趣种菜 - 植物 - 点我'),
        ]
        self.qu_zhong_cai = App(urls, 'qu-zhong-cai')

        # 金猪游戏盒子
        urls = [
            Api('/api/v1/tczyqtt/sign',log='填词小秀才 - 签到'),
            Api('/api/v1/tczyqtt/lottery',log='填词小秀才 - lottery'),
            Api('/api/v1/tczyqtt/get_reward',log='填词小秀才 - 任务完成'),
            Api('/api/v1/tczyqtt/add_coin',log='填词小秀才 - 过关领金币', params_as_all=True),

            Api('/x/v1/goldpig/info', log='游戏盒子 - 金猪信息'),
            Api('/x/v1/goldpig/withdraw', log='游戏盒子 - 金猪 - 双倍收金币'),
            Api('/x/task/v3/list',params_as_all=True),
            Api('/x/task/v2/take-reward', log='领金币'),
            Api('game-center-new.1sapp.com/x/open/game', log='1-打开游戏', f_name='open_game',f_p_arg={'app_id'}),
            Api('qttgame.midsummer.top/api/Login', log='2-登录游戏', f_name='api_login', f_b_arg={'ticket','game_id'}),
            Api('game-center-new.1sapp.com/x/game-report/special_report', log='special_report', f_name='game_do_task',f_b_arg={'app_id'},f_b_kwarg={'report_type':'round'}),
            Api('game-center-new.1sapp.com/x/game-report/duration_report', log='duration_report', f_name='game_duration_report',f_b_arg={'start_ts','duration'},f_b_kwarg={'report_type':'duration_addition'}),
            Api('game-center-new.1sapp.com/x/task/v2/take-reward', log='任务完成 - 领金币', f_name='game_take_reward',f_b_arg={'task_id'}),
            Api('qttgame.midsummer.top/api/AddCoin', log='成语 - 金币',f_b_arg={'AddCoinNum','session_id'}),
            Api('/x/open/coin/add', log='切菜 - 金币', body_as_all=True),
        ]
        self.you_xi_he_zi = App(urls, 'you-xi-he-zi')

        # 欢乐养鸡场
        urls = [
            Api('/x/chicken/info', log='欢乐养鸡场 - 信息'),
            Api('/x/chicken/task/take-award', log='达标领奖励'),
            Api('/x/chicken/feed', log='喂饲料'),
            Api('/x/chicken/get-fodder', log='领饲料', f_b_arg={'id','pos','again'}),
            '/x/chicken/video/accomplish',
        ]
        self.yang_ji_chang = App(urls, 'yang-ji-chang')

        self.flowfilters = [
            self.toutiao,
            self.huoshan,
            self.qtt_video,
            self.qu_zhong_cai,
            self.qu_tou_tiao,
            self.hao_kan,
            self.quan_ming,
            self.ma_yi_kd,
            self.dftt,
            self.zhong_qin_kd,
            self.cai_dan_sp,
            self.kai_xin_da_ti,
            self.qu_jian_pan,
            self.you_xi_he_zi,
            self.yang_ji_chang,
        ]

        

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

            def gen_app_data_to_file(data: dict, file_name):
                for device, app in self.session_hit:
                    try:
                        dd = data[device][app]
                        print(f"生成 App - {app}", end='\t')
                        self._gen_file(dd, f'{file_name}-{device}.json', self.api_dir.joinpath(app))
                    except:
                        pass

            # 生成app下的 data-bodys-keys.json, data-params-keys.json, data-fn-url.json
            gen_app_data_to_file(self.bodys_keys, 'data-bodys-keys')
            gen_app_data_to_file(self.params_keys, 'data-params-keys')
            gen_app_data_to_file(self.app_fn_url, 'data-fn-url')
            gen_app_data_to_file(self.params_as_all, 'data-params_as_all')
            gen_app_data_to_file(self.bodys_as_all, 'data-bodys_as_all')

            sessions_by_app = {}
            # 生成app下的 session_xxx.py
            for device, app in self.session_hit:
                sessions_jinja_data = sessions_by_app.setdefault(app, list())
                sessions_jinja_data.append({
                    'file': f'session_{device}',
                    'session': device,
                })


                hosts = self.headers[device][app]
                for h, d in hosts.items():
                    self._delete_some_headers(d)


                var_dict = dict()
                var_dict['session_id'] = f'{device!r}'

                def import_module(app, device):
                    import importlib.util
                    try:
                        module_name = f'session_{device}'
                        path = self.api_dir.joinpath(app, f'{module_name}.py')  
                        spec = importlib.util.spec_from_file_location(module_name, path)
                        session_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(session_module)
                        return session_module
                    except Exception as e:
                        logging.error(e)
                        

                session_module = import_module(app, device)

                def get_old_data(session_module, var_name):
                    old_data = dict()
                    try:
                        old_data = getattr(session_module, var_name)
                    except Exception as e:
                        # traceback.print_exc()
                        pass
                    return old_data

                def abc(data: dict, var_name, var_dict: dict, mergehost=True, list_append: bool=False, limit:dict=None):
                    try:
                        dd = data[device][app]
                        try:
                            l = limit[device][app]
                        except :
                            l = dict()
                        merge_hosts = {}
                        try:
                            if mergehost:
                                for host, ddd in dd.items():
                                    merge_hosts.update(ddd)
                            else:
                                merge_hosts = dd
                        except:
                            merge_hosts = dd
                        old_data = get_old_data(session_module, var_name)
                        merge_hosts = merge_data(merge_hosts, old_data, list_append=list_append, limit=l)
                        var_dict[var_name] = json.dumps(merge_hosts, indent=2, sort_keys=True)
                        print(f"生成 App - {app:20} - session_{device}.py {var_name} 成功")
                    except Exception as e:
                        # traceback.print_exc()
                        print(e)
                        var_dict[var_name] = '{}'
                abc(self.headers, 'header_values', var_dict)
                abc(self.app_fn_url, 'fn_url', var_dict)
                abc(self.params_keys, 'params_keys', var_dict, mergehost=False)
                abc(self.bodys_keys, 'bodys_keys', var_dict, mergehost=False)
                abc(self.params, 'param_values', var_dict)
                abc(self.bodys, 'body_values', var_dict)
                abc(self.params_as_all, 'params_as_all', var_dict, list_append=True,limit=self.params_as_all_limit)
                abc(self.bodys_as_all, 'bodys_as_all', var_dict, list_append=True)
                abc(self.params_encry, 'params_encry', var_dict, list_append=True)
                abc(self.bodys_encry, 'bodys_encry', var_dict, list_append=True)

                tfile = f'session_xxx.j2.py'
                gfile = self.api_dir.joinpath(app, f'session_{device}.py')
                self.gen_file_from_jinja2(tfile, gfile, seq=var_dict)

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
            print(e)
            logging.error(e)

    def response(self, flow: http.HTTPFlow):
        ft = None
        for i, flt in enumerate(self.flowfilters):
            if flt(flow):
                ft = flt
                if not flt == self.flowfilters[0]:
                    self.flowfilters.pop(i)
                    self.flowfilters.insert(0, flt)
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

            ctx.log.error(f'触发 App = {ft.app_name}')
            ctx.log.error(f'触发 api = {api} {request.method}')

            function_name = re.sub(r'[./-]', '_', url_path).strip('_').lower()
            api_url = f'{request.scheme}://{request.pretty_host}{url_path}'
            headers_code = self.headers_string(flow)
            params_code = self.params_string(flow)
            data_code = self.data_string(flow, api)

            path = pathlib.Path(f'{self.api_dir}{ft.app_name}')
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

    def _delete_some_headers(self, headers: dict):
        h = {
            ':authority', 'accept', 'accept-language', 'accept-encoding', 
            'connection', 'content-Length', 'cache-control', 
            'host', 'pragma'
        }
        for key in h:
            try:
                headers.pop(key.upper(), None)
                headers.pop(key.lower(), None)
                headers.pop(key.title(), None)
            except:
                pass

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

def get_data(session_module, var_name):
    old_data = dict()
    try:
        old_data = getattr(session_module, var_name)
    except Exception as e:
        # traceback.print_exc()
        pass
    return old_data

def merge_data(new_data: dict, old_data: dict, list_append: bool=False, limit:dict=None):
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


def import_module(path: pathlib.Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(path.stem,str(path))
    session_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(session_module)
    return session_module

def inner(d, device='', app='', host=''):
    d = d.setdefault(device, dict())
    d = d.setdefault(app, dict())
    d = d.setdefault(host, dict())
    return d

def inner_by_list(d, l: list):
    for key in l:
        d = d.setdefault(key, dict())
    return d

def merge_file(from_file: pathlib.Path, to_file: pathlib.Path):

    from_module = import_module(from_file)
    to_module = import_module(to_file)

    vars = [
        ('header_values',False),
        ('fn_url',False),
        ('params_keys',False),
        ('bodys_keys',False),
        ('param_values',False),
        ('body_values',False),
        ('params_as_all',True),
        ('bodys_as_all',True),
        ('params_encry',True),
        ('bodys_encry',True),
    ]
    var_dict = dict()
    for var in vars:
        from_data = get_data(from_module,var[0])
        to_data = get_data(to_module,var[0])
        data = merge_data(from_data, to_data)
        var_dict[var[0]] = json.dumps(data, indent=2, sort_keys=True)
    pass

    tfile = pathlib.Path(__file__).parent.joinpath('session_xxx.j2.py')
    gfile = to_file.parent.joinpath(f'{to_file.stem}_merged{to_file.suffix}')

    with open(tfile) as f:
        s = f.read()
        t = Template(s)
        ss = t.render(seq=var_dict)
        with open(gfile, mode='w') as ff:
            ff.write(ss)
    pass

def test_merge_file():
    from_file = pathlib.Path('/Users/zhoujie/Desktop/api/ma-yi-kd/session_xiaomi.py')
    to_file = pathlib.Path('/Users/zhoujie/Desktop/dev/ma-yi-kd/session_xiaomi.py')
    merge_file(from_file, to_file)

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

    # test_merge_file()
    test_jinja()
    

    api =Api(r'/mission/intPointReward',params_as_all=False, body_as_all=False,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'})#时段签到
    print(api.str_fun_params())
    api =Api(r'/mission/intPointReward',f_name='hourly_sign', log='时段签到', params_as_all=False, body_as_all=False,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
    print(api.str_fun_params())
    # api =Api(r'/mission/intPointReward',params_as_all=True, body_as_all=True,f_p_arg={'p1','p2'}, f_b_arg={'b1', 'b2'},f_p_kwarg={"pkw1":1, "pkw2":'2'})#时段签到
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
