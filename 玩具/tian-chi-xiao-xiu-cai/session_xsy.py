
session_id = 'xsy'

header_values = {
  "Origin": "http://newidea4-gamecenter-frontend.1sapp.com",
  "Referer": "http://newidea4-gamecenter-frontend.1sapp.com/gamecenter/platform/prod/missions-gapp/index.html?is_hide_arrow=true&platform=gapp",
  "User-Agent": "Mozilla/5.0 (Linux; Android 10; POT-AL00a Build/HUAWEIPOT-AL00a; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 qapp_android qapp_version_10203000",
  "X-Requested-With": "com.heitu.tcxxc",
  "access_token": "f99c73f5-92db-465f-bc1e-1ff1a5e59284",
  "origin": "https://static.game.jingyougz.com",
  "referer": "https://static.game.jingyougz.com/tcxxc_app/tcxxcRes/index.html?app_id=a3NqMwuuoZCC&app_name=%E5%A1%AB%E8%AF%8D%E5%B0%8F%E7%A7%80%E6%89%8D%E5%8F%91%E8%A1%8CAPP&appid=a3NqMwuuoZCC&dc=&dtu=10535&ext=eyJzb3VyY2UiOiIyODcwMDEifQ%3D%3D&origin_type=0&platform=gapp&sdk_version=cocos.dfc4c677d67e867c382c.js&sign=b20b84188fe73ec94c546f913c1fa3ed&source=287001&tag_id=&ticket=t11XkXQyfKmy1s9Pjuy3m&time=1585649599&uuid=57f748bab72347caa5b6718616c42902",
  "user-agent": "Mozilla/5.0 (Linux; Android 10; POT-AL00a Build/HUAWEIPOT-AL00a; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 qapp_android qapp_version_10203000",
  "x-requested-with": "com.heitu.tcxxc"
}

fn_url = {
  "/api/v1/tczyapp/add_coin": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/add_coin",
  "/api/v1/tczyapp/draw_a_char": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/draw_a_char",
  "/api/v1/tczyapp/event": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/event",
  "/api/v1/tczyapp/exchange": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/exchange",
  "/api/v1/tczyapp/get_rank": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/get_rank",
  "/api/v1/tczyapp/get_rank_reward": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/get_rank_reward",
  "/api/v1/tczyapp/get_reward": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/get_reward",
  "/api/v1/tczyapp/get_words_info": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/get_words_info",
  "/api/v1/tczyapp/login": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/login",
  "/api/v1/tczyapp/lottery": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/lottery",
  "/api/v1/tczyapp/open_redpacket": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/open_redpacket",
  "/api/v1/tczyapp/round_report": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/round_report",
  "/api/v1/tczyapp/sign": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/sign",
  "/api/v1/tczyapp/updateInfo": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/updateInfo",
  "/api/v1/tczyapp/upload_rank": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/upload_rank",
  "/api/v1/tczyapp/user_coin": "https://tczy2.game.jingyougz.com/api/v1/tczyapp/user_coin",
  "/qapptoken": "https://oauth2-api.1sapp.com/qapptoken",
  "/withdraw/getBindInfo": "https://openapi.1sapp.com/withdraw/getBindInfo",
  "/withdraw/getCoinLog": "https://openapi.1sapp.com/withdraw/getCoinLog",
  "/withdraw/order/create": "https://openapi.1sapp.com/withdraw/order/create",
  "/withdraw/order/listApp": "https://openapi.1sapp.com/withdraw/order/listApp",
  "/withdraw/sku/list": "https://openapi.1sapp.com/withdraw/sku/list",
  "/x/game-center/gapp/sign-in": "https://newidea4-gamecenter-backend.1sapp.com/x/game-center/gapp/sign-in",
  "/x/game-center/gapp/sign-in-double": "https://newidea4-gamecenter-backend.1sapp.com/x/game-center/gapp/sign-in-double",
  "/x/game-report/duration_report": "https://newidea4-gamecenter-backend.1sapp.com/x/game-report/duration_report",
  "/x/game-report/special_report": "https://newidea4-gamecenter-backend.1sapp.com/x/game-report/special_report",
  "/x/gapp/task/list": "http://newidea4-gamecenter-backend.1sapp.com/x/gapp/task/list",
  "/x/open/game": "https://newidea4-gamecenter-backend.1sapp.com/x/open/game",
  "/x/user/token": "http://newidea4-gamecenter-backend.1sapp.com/x/user/token"
}

params_keys = {
  "game-center-new.1sapp.com": {
    "/x/user/token": [
      "token",
      "platform",
      "source",
      "app_id",
      "dtu",
      "vn",
      "tk",
      "v",
      "dc",
      "tuid",
      "user_mode"
    ]
  },
  "newidea4-gamecenter-backend.1sapp.com": {
    "/x/game-center/gapp/sign-in": [
      "request_timestamp"
    ],
    "/x/game-center/gapp/sign-in-double": [
      "request_timestamp"
    ],
    "/x/game-report/duration_report": [],
    "/x/game-report/special_report": [],
    "/x/gapp/task/list": [
      "request_timestamp",
      "request_id",
      "source",
      "platform",
      "memberid",
      "tuid",
      "tk",
      "dtu",
      "oaid",
      "android_id",
      "dc",
      "v",
      "vn",
      "os",
      "app_id",
      "referrer",
      "session_timestamp",
      "env",
      "user_mode",
      "app",
      "network",
      "g_token",
      "uuid"
    ],
    "/x/open/game": [
      "dtu",
      "sign",
      "lon",
      "tuid",
      "deviceCode",
      "source",
      "versionName",
      "uuid",
      "version",
      "platform",
      "network",
      "app_name",
      "g_token",
      "v",
      "tk",
      "vn",
      "OSVersion",
      "time",
      "app_id",
      "lat",
      "oaid",
      "dc"
    ],
    "/x/user/token": [
      "token",
      "platform",
      "app_id",
      "dtu",
      "vn",
      "tk",
      "v",
      "dc",
      "tuid",
      "user_mode",
      "request_id"
    ]
  },
  "oauth2-api.1sapp.com": {
    "/qapptoken": [
      "app_id",
      "token",
      "scope",
      "native_id",
      "app_name"
    ]
  },
  "openapi.1sapp.com": {
    "/withdraw/getBindInfo": [],
    "/withdraw/getCoinLog": [
      "page",
      "page_size"
    ],
    "/withdraw/order/create": [],
    "/withdraw/order/listApp": [],
    "/withdraw/sku/list": [
      "tk"
    ]
  },
  "tczy2.game.jingyougz.com": {
    "/api/v1/tczyapp/add_coin": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/draw_a_char": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/event": [
      "pid",
      "puid",
      "utag",
      "cver",
      "event",
      "source",
      "data"
    ],
    "/api/v1/tczyapp/exchange": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/get_rank": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/get_rank_reward": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/get_reward": [
      "task",
      "activity_id",
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/get_words_info": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/login": [
      "platform",
      "ticket",
      "pid",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/lottery": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/open_redpacket": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/round_report": [
      "round",
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/sign": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/updateInfo": [
      "open_id",
      "data",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/upload_rank": [
      "open_id",
      "score",
      "data",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/tczyapp/user_coin": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ]
  }
}

bodys_keys = {
  "game-center-new.1sapp.com": {
    "/x/user/token": []
  },
  "newidea4-gamecenter-backend.1sapp.com": {
    "/x/game-center/gapp/sign-in": [
      "source",
      "platform",
      "memberid",
      "tuid",
      "tk",
      "dtu",
      "oaid",
      "android_id",
      "dc",
      "v",
      "vn",
      "os",
      "app_id",
      "referrer",
      "session_timestamp",
      "env",
      "user_mode",
      "app",
      "network",
      "request_id",
      "g_token",
      "uuid"
    ],
    "/x/game-center/gapp/sign-in-double": [
      "source",
      "platform",
      "memberid",
      "tuid",
      "tk",
      "dtu",
      "oaid",
      "android_id",
      "dc",
      "v",
      "vn",
      "os",
      "app_id",
      "referrer",
      "session_timestamp",
      "env",
      "user_mode",
      "app",
      "network",
      "request_id",
      "g_token",
      "uuid"
    ],
    "/x/game-report/duration_report": [
      "report_type",
      "start_ts",
      "duration",
      "token",
      "platform",
      "g_token",
      "source",
      "app_id",
      "origin_type",
      "vn",
      "tk",
      "v",
      "dtu",
      "tuid",
      "request_id"
    ],
    "/x/game-report/special_report": [
      "report_type",
      "target_value",
      "report_sub_type",
      "token",
      "platform",
      "g_token",
      "source",
      "app_id",
      "origin_type",
      "vn",
      "tk",
      "v",
      "dtu",
      "tuid",
      "request_id"
    ],
    "/x/gapp/task/list": [],
    "/x/open/game": [],
    "/x/user/token": []
  },
  "oauth2-api.1sapp.com": {
    "/qapptoken": []
  },
  "openapi.1sapp.com": {
    "/withdraw/getBindInfo": [],
    "/withdraw/getCoinLog": [],
    "/withdraw/order/create": [
      "tk",
      "sku_id"
    ],
    "/withdraw/order/listApp": [],
    "/withdraw/sku/list": []
  },
  "tczy2.game.jingyougz.com": {
    "/api/v1/tczyapp/add_coin": [],
    "/api/v1/tczyapp/draw_a_char": [],
    "/api/v1/tczyapp/event": [],
    "/api/v1/tczyapp/exchange": [],
    "/api/v1/tczyapp/get_rank": [],
    "/api/v1/tczyapp/get_rank_reward": [],
    "/api/v1/tczyapp/get_reward": [],
    "/api/v1/tczyapp/get_words_info": [],
    "/api/v1/tczyapp/login": [],
    "/api/v1/tczyapp/lottery": [],
    "/api/v1/tczyapp/open_redpacket": [],
    "/api/v1/tczyapp/round_report": [],
    "/api/v1/tczyapp/sign": [],
    "/api/v1/tczyapp/updateInfo": [],
    "/api/v1/tczyapp/upload_rank": [],
    "/api/v1/tczyapp/user_coin": []
  }
}

param_values = {
  "activity_id": "5",
  "android_id": "7d8eb5111916d12e",
  "app": "game_tcxxc",
  "app_id": "a3NqMwuuoZCC",
  "app_name": "undefined",
  "cver": "9",
  "data": "{\"data\":{\"level\":25},\"power\":60,\"newPower\":10,\"powerTime\":1584789193806,\"maxVideoPower\":0,\"isNewPalyer\":false,\"cash\":0,\"item\":{},\"dailyVideoCount\":2,\"lastDayoutTime\":1585649630686,\"tipCount\":3,\"levelupNum\":4,\"cmpCount\":0,\"cmpExCount\":0,\"rateNum\":0,\"rateMax\":10,\"dayAnwerNum\":0,\"taskList\":{},\"dayTaskList\":{\"101\":{\"id\":101,\"process\":1,\"state\":1},\"102\":{\"id\":102,\"process\":0,\"state\":0},\"103\":{\"id\":103,\"process\":0,\"state\":0},\"104\":{\"id\":104,\"process\":0,\"state\":0},\"105\":{\"id\":105,\"process\":2,\"state\":0},\"107\":{\"id\":107,\"process\":2,\"state\":0},\"109\":{\"id\":109,\"process\":0,\"state\":0}},\"weekReward\":3,\"nActionPoints\":[100013,100016,100015,100014,100100,10004,10005,10006,10007,10008,110100,100010,10009,100200,110200,100012,100300,110300,100400,110400],\"dailyPoints\":[],\"devLevel\":25,\"appTipCoin\":false,\"snowRewardGotTime\":0,\"activeNum\":10,\"activeGet\":true,\"activeWordLottery\":1,\"activeWordPass\":0,\"activeWordOnceGet\":true,\"isNewCheck\":true,\"isloadCheck\":1,\"isStartCheck\":1,\"isOpenRank\":true,\"videoClickCount\":0}",
  "dc": "",
  "dtu": "10535",
  "env": "prod",
  "g_token": "2eBNL6pJrGKf9fme-Gtf9PqJnj15WZ-4u6NqAGCi-7ON-Gpk-Gt8DsBfL6nRAGCJu7AUr7Y1u8pku8KN-3WJ-jy1u3xJ98B197O4-vOqr6pJcp==",
  "memberid": "981097889",
  "native_id": "undefined",
  "network": "wifi",
  "oaid": "fbe7bf38-feb7-7625-aff2-6fceef7f4291",
  "open_id": "u11Xg9zC9Y1ZZYDC2N5D1",
  "origin_type": "0",
  "os": "android",
  "page": "1",
  "page_size": "50",
  "pid": "1575266631",
  "platform": "gapp",
  "puid": "1032306",
  "referrer": "",
  "relive": "0",
  "request_id": "f284d2fe90d66888d28f4afde6ff757c",
  "request_timestamp": "1585649643376",
  "scope": "passport,withdraw,charge",
  "score": "29.2",
  "session_timestamp": "1585649643376",
  "source": "287001",
  "task": "101",
  "ticket": "t11XkXQyfKmy1s9Pjuy3m",
  "tk": "ACGTbrrkZlYRPOo3mSvE3Ec0zHQzB61ho31nbXRjeHhj",
  "token": "056558S_--kO7iwseoPhvQ4d_qdrFzWNs91yyX6yBK9GY3NxA59_o9YhCBlwYRz-HZO0Qr_EP7EZjubqxKNSJ0LlkSQkF1rQRfBN",
  "tuid": "k2665GZWETzqN5krxNxHNA",
  "user_mode": "",
  "utag": "0",
  "uuid": "981097889",
  "v": "10203000",
  "vn": "1.2.3.000.0311.1904"
}

body_values = {
  "app_id": "a3NqMwuuoZCC",
  "dtu": "10535",
  "duration": "12",
  "g_token": "2eBNL6pJrGKf9fme-Gtf9PqJnj15WZ-4u6NqAGCi-7ON-Gpk-GA8DsBfL6nRAGCJuGOf-6TU9Ggfu6yJu39U-v11WGm4W7WgWv13-7_39v9Jcp==",
  "origin_type": "0",
  "platform": "gapp",
  "report_type": "duration_addition",
  "request_id": "0c6078ae21c07f2025617c02fb99dd6b",
  "source": "287001",
  "start_ts": "1585649643",
  "tk": "ACGTbrrkZlYRPOo3mSvE3Ec0zHQzB61ho31nbXRjeHhj",
  "token": "056558S_--kO7iwseoPhvQ4d_qdrFzWNs91yyX6yBK9GY3NxA59_o9YhCBlwYRz-HZO0Qr_EP7EZjubqxKNSJ0LlkSQkF1rQRfBN",
  "tuid": "k2665GZWETzqN5krxNxHNA",
  "v": "10203000",
  "vn": "1.2.3.000.0311.1904"
}

params_as_all = {}

bodys_as_all = {}

params_encry = {}

bodys_encry = {}

api_ok = {
  "/api/v1/tczyapp/add_coin": {
    "code": [
      1
    ]
  },
  "/api/v1/tczyapp/draw_a_char": {
    "code": [
      1
    ]
  },
  "/api/v1/tczyapp/get_rank": {
    "code": [
      1
    ]
  },
  "/api/v1/tczyapp/get_rank_reward": {
    "code": [
      1,
      402
    ]
  },
  "/api/v1/tczyapp/login": {
    "code": [
      1
    ]
  },
  "/api/v1/tczyapp/lottery": {
    "code": [
      1,
      10010
    ]
  },
  "app_ok": [
    0,
    1
  ],
  "app_ok_key": [
    "code"
  ]
}


session_data = {
    'session_id': session_id,
    'header_values': header_values,
    'fn_url': fn_url,
    'params_keys': params_keys,
    'bodys_keys': bodys_keys,
    'param_values': param_values,
    'body_values': body_values,
    'params_as_all': params_as_all,
    'bodys_as_all': bodys_as_all,
    'params_encry': params_encry,
    'bodys_encry': bodys_encry,
    'api_ok': api_ok,    
}