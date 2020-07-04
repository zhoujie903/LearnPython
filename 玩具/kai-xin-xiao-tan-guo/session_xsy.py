
session_id = 'xsy'

header_values = {
  "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; POT-AL00a Build/HUAWEIPOT-AL00a)",
  "oaid": "fbe7bf38-feb7-7625-aff2-6fceef7f4291",
  "tuid": "k2665GZWETzqN5krxNxHNA",
  "user-agent": "okhttp/3.11.0"
}

fn_url = {
  "/happy/protocol": "https://qutoutiao.atigame.com/happy/protocol",
  "/happy/qtt/apkuserinfo": "https://qutoutiao.atigame.com/happy/qtt/apkuserinfo",
  "/x/cocos/gapp-game-init": "https://newidea4-gamecenter-backend.1sapp.com/x/cocos/gapp-game-init",
  "/x/user/token": "http://newidea4-gamecenter-backend.1sapp.com/x/user/token"
}

params_keys = {
  "newidea4-gamecenter-backend.1sapp.com": {
    "/x/cocos/gapp-game-init": [
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
      "token",
      "app_name",
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
      "source",
      "app_id",
      "origin_type",
      "dtu",
      "vn",
      "tk",
      "v",
      "dc",
      "tuid",
      "user_mode"
    ]
  },
  "qutoutiao.atigame.com": {
    "/happy/protocol": [
      "uid"
    ],
    "/happy/qtt/apkuserinfo": [
      "ticket"
    ]
  }
}

bodys_keys = {
  "newidea4-gamecenter-backend.1sapp.com": {
    "/x/cocos/gapp-game-init": [],
    "/x/user/token": []
  },
  "qutoutiao.atigame.com": {
    "/happy/protocol": [
      "data"
    ],
    "/happy/qtt/apkuserinfo": []
  }
}

param_values = {
  "OSVersion": "10",
  "app_id": "a3MasNnLgxAY",
  "app_name": "game_kxxtg",
  "dc": "",
  "deviceCode": "",
  "dtu": "10419",
  "lat": "0.0",
  "lon": "0.0",
  "network": "wifi",
  "oaid": "fbe7bf38-feb7-7625-aff2-6fceef7f4291",
  "origin_type": "0",
  "os": "android",
  "platform": "gapp",
  "sign": "6b2dee934e7682c64cb64c486326f40b",
  "source": "287001",
  "ticket": "t11Xk3ZN7JkZ42Fptn35y",
  "time": "1585222617796",
  "tk": "ACGTbrrkZlYRPOo3mSvE3Ec0dUJgyHQU7hBnbWt4eHRn",
  "token": "4660Ol5zZTBPsJ0Khj6qY0cDynFENJD_MxlXYUaQ3lZrWZaspw8omIcQbyTcpYuUcSP6HMdwyj5yQXiZIbn6SVDys5_XP4bGrJKv",
  "tuid": "k2665GZWETzqN5krxNxHNA",
  "uid": "1",
  "user_mode": "",
  "uuid": "70e7623ee57d412493fb782d7a9c19e0",
  "v": "10203000",
  "version": "10203000",
  "versionName": "1.2.3.000.0306.1716",
  "vn": "1.2.3.000.0306.1716"
}

body_values = {
  "data": "{\"data\":[{\"uid\":17167536,\"uk\":\"2oLrPywd\",\"openId\":\"u11Xk3YwT88M7qZj8Dfh9\",\"gender\":0,\"province\":\"\",\"appVersion\":\"1.0.1\",\"deviceModel\":\"test\",\"apkVersion\":\"1.0.0\"},[{\"method\":\"startGame\",\"levelType\":0}]]}"
}

params_as_all = {
  "/x/cocos/gapp-game-init": [
    {
      "OSVersion": "10",
      "app_id": "a3MasNnLgxAY",
      "app_name": "game_kxxtg",
      "dc": "",
      "deviceCode": "",
      "dtu": "10419",
      "lat": "0.0",
      "lon": "0.0",
      "network": "wifi",
      "oaid": "fbe7bf38-feb7-7625-aff2-6fceef7f4291",
      "os": "android",
      "platform": "gapp",
      "sign": "6b2dee934e7682c64cb64c486326f40b",
      "source": "287001",
      "time": "1585222617796",
      "tk": "ACGTbrrkZlYRPOo3mSvE3Ec0dUJgyHQU7hBnbWt4eHRn",
      "token": "4660Ol5zZTBPsJ0Khj6qY0cDynFENJD_MxlXYUaQ3lZrWZaspw8omIcQbyTcpYuUcSP6HMdwyj5yQXiZIbn6SVDys5_XP4bGrJKv",
      "tuid": "k2665GZWETzqN5krxNxHNA",
      "uuid": "70e7623ee57d412493fb782d7a9c19e0",
      "v": "10203000",
      "version": "10203000",
      "versionName": "1.2.3.000.0306.1716",
      "vn": "1.2.3.000.0306.1716"
    }
  ]
}

bodys_as_all = {}

params_encry = {}

bodys_encry = {}

api_ok = {
  "app_ok": {
    "code": [
      0
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