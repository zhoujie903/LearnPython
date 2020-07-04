
session_id = 'xiaomi'

header_values = {
  "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; MI 5 MIUI/V10.2.1.0.OAACNXM)",
  "oaid": "ef8a43971141a8c5",
  "tuid": "X9YZGOyiKfXT7ke52nizWg",
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
      "device_code",
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
  "OSVersion": "8.0.0",
  "app_id": "a3MasNnLgxAY",
  "app_name": "game_kxxtg",
  "dc": "869161028541084",
  "deviceCode": "869161028541084",
  "device_code": "869161028541084",
  "dtu": "10255",
  "lat": "0.0",
  "lon": "0.0",
  "network": "wifi",
  "oaid": "ef8a43971141a8c5",
  "origin_type": "0",
  "os": "android",
  "platform": "gapp",
  "sign": "c8e0db122aa45cceadf4ef6a9d2b60ea",
  "source": "287001",
  "ticket": "t11Xk2D4e545n8oQCL4xP",
  "time": "1585201922892",
  "tk": "ACFf1hkY7KIp9dPuR7naeLNaJ1K__KEXGtNnbWt4eHRn",
  "token": "487ddoJfK10Gnfxpj2Zxvpi3lu7P_wxMh80A4_MAqUakzunoFukfnKDQH6nHSYVxPgrnUEnSnHsaRYpoHD7o9qiXQgVgep8pWNQx",
  "tuid": "X9YZGOyiKfXT7ke52nizWg",
  "uid": "1",
  "user_mode": "",
  "uuid": "66bec106390a4f99887bc816ef40deff",
  "v": "10203000",
  "version": "10203000",
  "versionName": "1.2.3.000.0306.1716",
  "vn": "1.2.3.000.0306.1716"
}

body_values = {
  "data": "{\"data\":[{\"uid\":16998996,\"uk\":\"JPTfGavi\",\"openId\":\"u11XinsMnCDP6KSDZx1jd\",\"gender\":0,\"province\":\"\",\"appVersion\":\"1.0.1\",\"deviceModel\":\"test\",\"apkVersion\":\"1.0.0\"},[{\"method\":\"startGame\",\"levelType\":0}]]}"
}

params_as_all = {
  "/x/cocos/gapp-game-init": [
    {
      "OSVersion": "8.0.0",
      "app_id": "a3MasNnLgxAY",
      "app_name": "game_kxxtg",
      "dc": "869161028541084",
      "deviceCode": "869161028541084",
      "dtu": "10255",
      "lat": "0.0",
      "lon": "0.0",
      "network": "wifi",
      "oaid": "ef8a43971141a8c5",
      "os": "android",
      "platform": "gapp",
      "sign": "c8e0db122aa45cceadf4ef6a9d2b60ea",
      "source": "287001",
      "time": "1585201922892",
      "tk": "ACFf1hkY7KIp9dPuR7naeLNaJ1K__KEXGtNnbWt4eHRn",
      "token": "487ddoJfK10Gnfxpj2Zxvpi3lu7P_wxMh80A4_MAqUakzunoFukfnKDQH6nHSYVxPgrnUEnSnHsaRYpoHD7o9qiXQgVgep8pWNQx",
      "tuid": "X9YZGOyiKfXT7ke52nizWg",
      "uuid": "66bec106390a4f99887bc816ef40deff",
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
    'code':[0]
  },
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