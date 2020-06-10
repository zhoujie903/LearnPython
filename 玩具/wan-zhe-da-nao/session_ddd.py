
session_id = 'ddd'

header_values = {
  "access_token": "a3db31fa-3bd9-4b52-aab6-a230d7daeb00",
  "oaid": "7efa779f-e7ff-05d8-3d99-5ffd04cf5a3c",
  "origin": "https://static.game.iggdata.com",
  "referer": "https://static.game.iggdata.com/zlcj/qtt_app/app/index.html?app_id=a3NqP2sbHEzE&app_name=%E7%8E%8B%E8%80%85%E5%A4%A7%E8%84%91%E5%8F%91%E8%A1%8CAPP&appid=a3NqP2sbHEzE&dc=860928043486407&dtu=10010&ext=eyJzb3VyY2UiOiIyODcwMDEifQ%3D%3D&origin_type=0&platform=gapp&sdk_version=cocos.a08287c394db320fd8e95b0c8b1fe1b1.js&sign=26e6fcc74595a4b98fb0c7271a61760b&source=287001&tag_id=&ticket=t11XrvT46MoR16kDTsMzP&time=1591337028&uuid=ef09f60da4d949939d4bcdc66fc21416",
  "tuid": "FlRO_CqsveKY_eAGkTm2JQ",
  "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; DUB-TL00 Build/HUAWEIDUB-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36 qapp_android qapp_version_10202000",
  "x-requested-with": "com.heitu.wzdn"
}

fn_url = {
  "/api/v1/z6qtt/exchange": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/exchange",
  "/api/v1/z6qtt/get_rank": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/get_rank",
  "/api/v1/z6qtt/get_rank_reward": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/get_rank_reward",
  "/api/v1/z6qtt/get_reward": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/get_reward",
  "/api/v1/z6qtt/login": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/login",
  "/api/v1/z6qtt/lottery": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/lottery",
  "/api/v1/z6qtt/sign": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/sign",
  "/api/v1/z6qtt/updateInfo": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/updateInfo",
  "/api/v1/z6qtt/upload_rank": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/upload_rank",
  "/api/v1/z6qtt/user_coin": "https://z6qtt.game.jingyougz.com/api/v1/z6qtt/user_coin",
  "/qapptoken": "https://oauth2-api.1sapp.com/qapptoken",
  "/withdraw/getBindInfo": "https://openapi.1sapp.com/withdraw/getBindInfo",
  "/withdraw/getCoinLog": "https://openapi.1sapp.com/withdraw/getCoinLog",
  "/withdraw/order/create": "https://openapi.1sapp.com/withdraw/order/create",
  "/withdraw/order/listApp": "https://openapi.1sapp.com/withdraw/order/listApp",
  "/withdraw/sku/list": "https://openapi.1sapp.com/withdraw/sku/list",
  "/x/open/game": "https://newidea4-gamecenter-backend.1sapp.com/x/open/game",
  "/x/user/token": "https://newidea4-gamecenter-backend.1sapp.com/x/user/token"
}

params_keys = {
  "newidea4-gamecenter-backend.1sapp.com": {
    "/x/open/game": [
      "dtu",
      "os",
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
      "uuid",
      "token"
    ]
  },
  "oauth2-api.1sapp.com": {
    "/qapptoken": [
      "token",
      "scope",
      "native_id"
    ]
  },
  "openapi.1sapp.com": {
    "/withdraw/getBindInfo": [
      "tk",
      "tuid"
    ],
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
  "z6qtt.game.jingyougz.com": {
    "/api/v1/z6qtt/exchange": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/get_rank": [
      "open_id",
      "type",
      "count",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/get_rank_reward": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/get_reward": [
      "activity_id",
      "relive",
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/login": [
      "platform",
      "ticket",
      "pid",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/lottery": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/sign": [
      "open_id",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/updateInfo": [],
    "/api/v1/z6qtt/upload_rank": [
      "open_id",
      "score",
      "data",
      "type",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/user_coin": [
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
  "newidea4-gamecenter-backend.1sapp.com": {
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
      "sku_id",
      "tuid"
    ],
    "/withdraw/order/listApp": [],
    "/withdraw/sku/list": []
  },
  "z6qtt.game.jingyougz.com": {
    "/api/v1/z6qtt/exchange": [],
    "/api/v1/z6qtt/get_rank": [],
    "/api/v1/z6qtt/get_rank_reward": [],
    "/api/v1/z6qtt/get_reward": [],
    "/api/v1/z6qtt/login": [],
    "/api/v1/z6qtt/lottery": [],
    "/api/v1/z6qtt/sign": [],
    "/api/v1/z6qtt/updateInfo": [
      "open_id",
      "data",
      "pid",
      "puid",
      "utag",
      "cver",
      "source"
    ],
    "/api/v1/z6qtt/upload_rank": [],
    "/api/v1/z6qtt/user_coin": []
  }
}

param_values = {
  "OSVersion": "8.1.0",
  "activity_id": "6",
  "android_id": "95d659b5b08e95e9",
  "app": "game_wzdn",
  "app_id": "a3NqP2sbHEzE",
  "app_name": "game_wzdn",
  "count": "50",
  "cver": "9",
  "data": "{\"a\":\"http://thirdwx.qlogo.cn/mmopen/vi_32/3F69vPYZxt7TukWX6RMvQcMXGTqy8FrSSxKxe5vFOg5puRo4tV03o97NGJ7OR1FngWEezo4GHpNII04swhmN8A/132\",\"n\":\"\u535a\u7231\"}",
  "dc": "860928043486407",
  "deviceCode": "860928043486407",
  "device_code": "860928043486407",
  "dtu": "10010",
  "env": "prod",
  "g_token": "",
  "lat": "0.0",
  "lon": "0.0",
  "memberid": "1074353721",
  "mission": "3",
  "native_id": "46",
  "network": "wifi",
  "oaid": "7efa779f-e7ff-05d8-3d99-5ffd04cf5a3c",
  "open_id": "u11XrvT72Eg5z19JrjqcK",
  "origin_type": "0",
  "os": "android",
  "page": "1",
  "page_size": "50",
  "pid": "1581046020",
  "platform": "gapp",
  "puid": "61287",
  "referrer": "",
  "relive": "2",
  "request_id": "673e4675125ba907d0e067764f954d75",
  "request_timestamp": "1591337309422",
  "scope": "passport,withdraw,charge",
  "score": "29.9",
  "session_timestamp": "1591337309420",
  "sign": "4c0a8d87a718e5eb339e6d783f8a97ef",
  "source": "287001",
  "ticket": "t11XrvT46MoR16kDTsMzP",
  "time": "1591337027929",
  "tk": "ACEWVE78Kqy94pj94AaRObYlFWKsskQDYYhnbXd6ZG4",
  "token": "cddbIaYq-kFyQVlyoTndPWiKTcjsy8GD9Iy-F9nTPo83WX2rABUkIRjYkgioYZr8F9ob50wPcdtYQi4-itnmc8_lez6wlgE35jsc",
  "tuid": "FlRO_CqsveKY_eAGkTm2JQ",
  "type": "2",
  "user_mode": "",
  "utag": "1",
  "uuid": "1074353721",
  "v": "10202000",
  "version": "10202000",
  "versionName": "1.2.2.000.0229.1416",
  "vn": "1.2.2.000.0229.1416"
}

body_values = {
  "cver": "9",
  "data": "{\"level\":9,\"developLv\":0,\"powerTime\":1591337168749,\"maxVideoPower\":0,\"tipVideoCount\":0,\"isNew\":false,\"items\":{\"1\":0},\"lastDayoutTime\":1591337047415,\"tipCount\":3,\"nActionPoints\":[1005,1004,3001,100015,1006,4001,3002,4002,3003,4003,3004,4004,3005,4005,3006,4006,3007,4007,3008,4008,3009,4009],\"inviteGotList\":[],\"entryList\":[],\"dailyPullInfo\":{\"2\":{\"s\":0,\"v\":1},\"7\":{\"s\":0,\"v\":1},\"8\":{\"s\":0,\"v\":2},\"11\":{\"s\":0,\"v\":2},\"12\":{\"s\":0,\"v\":1}},\"dailyRewardInfo\":{\"2\":{\"state\":1}},\"subscribTime\":0,\"isEntry1Show\":false,\"isEntry2Show\":false,\"redbagCache\":0,\"appTipCoin\":false,\"source\":0,\"brainCount\":1,\"brainBest\":\"29.9\",\"brainTodayCount\":1,\"videoClickCount_Old\":0,\"videoClickCount\":0,\"activeNum\":0,\"activeGet\":true,\"dayTaskList\":{\"1\":{\"id\":1,\"process\":1,\"state\":2},\"2\":{\"id\":2,\"process\":5,\"state\":2},\"3\":{\"id\":3,\"process\":0,\"state\":0},\"4\":{\"id\":4,\"process\":3,\"state\":2},\"5\":{\"id\":5,\"process\":3,\"state\":2},\"6\":{\"id\":6,\"process\":2,\"state\":0},\"7\":{\"id\":7,\"process\":1,\"state\":2}}}",
  "open_id": "u11XrvT72Eg5z19JrjqcK",
  "pid": "1581046020",
  "puid": "61287",
  "sku_id": "40461",
  "source": "287001",
  "tk": "ACEWVE78Kqy94pj94AaRObYlFWKsskQDYYhnbXd6ZG4",
  "tuid": "FlRO_CqsveKY_eAGkTm2JQ",
  "utag": "1"
}

params_as_all = {}

bodys_as_all = {}

params_encry = {}

bodys_encry = {}

api_ok = {
  "/api/v1/z6qtt/add_coin": {
    "code": [
      1
    ]
  },
  "/api/v1/z6qtt/draw_a_char": {
    "code": [
      1
    ]
  },
  "/api/v1/z6qtt/get_rank": {
    "code": [
      1
    ]
  },
  "/api/v1/z6qtt/get_rank_reward": {
    "code": [
      1,
      402
    ]
  },
  "/api/v1/z6qtt/get_reward": {
    "code": [
      1
    ]
  },
  "/api/v1/z6qtt/login": {
    "code": [
      1
    ]
  },
  "/api/v1/z6qtt/lottery": {
    "code": [
      1,
      10010
    ]
  },
  "/withdraw/order/listApp": {
    "code": [
      0
    ]
  },
  "/x/open/game": {
    "code": [
      0
    ]
  },
  "/x/user/token": {
    "code": [
      0
    ]
  },
  "app_ok": {
    "code": [
      1
    ]
  },
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