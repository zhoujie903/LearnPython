
session_id = 'huawei'

header_values = {
  "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00)",
  "oaid": "ff985efd-7fbe-e4b9-379f-9dfa5dfd1e3f",
  "tuid": "oRePuRdsf6d6gGIm9Et5DQ",
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
  "dtu": "10425",
  "lat": "0.0",
  "lon": "0.0",
  "network": "wifi",
  "oaid": "ff985efd-7fbe-e4b9-379f-9dfa5dfd1e3f",
  "origin_type": "0",
  "os": "android",
  "platform": "gapp",
  "sign": "e612d3305a62dcdf5ff313b682fe2458",
  "source": "287001",
  "ticket": "t11Xk2T5stBcd9yM2s655",
  "time": "1585205630320",
  "tk": "ACGhF4-5F2x_p3qAYib0S3kN-MK8f43idRxnbWt4eHRn",
  "token": "386eYRW_2-sH-wJECI3QAlLokchseSm46eb57sBZ1lcDb9nMiqrfUr4WF-zv90zCM9ywHvS2hL0M8zMmL2UfISjw3AjjZRoDgnuB",
  "tuid": "oRePuRdsf6d6gGIm9Et5DQ",
  "uid": "1",
  "user_mode": "",
  "uuid": "513ba5f588424da4b87bee76abb9726e",
  "v": "10203000",
  "version": "10203000",
  "versionName": "1.2.3.000.0306.1716",
  "vn": "1.2.3.000.0306.1716"
}

body_values = {
  "data": "{\"data\":[{\"uid\":17089383,\"uk\":\"s78Vhwff\",\"openId\":\"u11XjTT71n5CuprPSLWT1\",\"gender\":0,\"province\":\"\",\"appVersion\":\"1.0.1\",\"deviceModel\":\"test\",\"apkVersion\":\"1.0.0\"},[{\"method\":\"startGame\",\"levelType\":0}]]}"
}

params_as_all = {
  "/x/cocos/gapp-game-init": [
    {
      "OSVersion": "10",
      "app_id": "a3MasNnLgxAY",
      "app_name": "game_kxxtg",
      "dc": "",
      "deviceCode": "",
      "dtu": "10425",
      "lat": "0.0",
      "lon": "0.0",
      "network": "wifi",
      "oaid": "ff985efd-7fbe-e4b9-379f-9dfa5dfd1e3f",
      "os": "android",
      "platform": "gapp",
      "sign": "e612d3305a62dcdf5ff313b682fe2458",
      "source": "287001",
      "time": "1585205630320",
      "tk": "ACGhF4-5F2x_p3qAYib0S3kN-MK8f43idRxnbWt4eHRn",
      "token": "386eYRW_2-sH-wJECI3QAlLokchseSm46eb57sBZ1lcDb9nMiqrfUr4WF-zv90zCM9ywHvS2hL0M8zMmL2UfISjw3AjjZRoDgnuB",
      "tuid": "oRePuRdsf6d6gGIm9Et5DQ",
      "uuid": "513ba5f588424da4b87bee76abb9726e",
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