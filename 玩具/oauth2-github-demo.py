'''
oauth2授权登录，获取资源
这个例子是：登录GitHub, 获取资源(github用户信息)
参考文章：https://www.jianshu.com/p/65225f50fe76
'''


import json

from flask import Flask, request, jsonify, redirect
import requests
from furl import furl

client_id = ''
client_secret = ''

app = Flask(__name__)

'''
"GET /oauth2/github/callback?code=18ece3352a0cae99d1aa&state=An+unguessable+random+string. HTTP/1.1"
'''
@app.route('/oauth2/<service>/callback')
def oauth2_call(service):
    print(service)

    code = request.args.get('code')
    access_token_url = 'https://github.com/login/oauth/access_token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        # 'redirect_uri':
        'state': 'An unguessable random string.'
    }

    r = requests.post(access_token_url, json=payload,
                      headers={'Accept': 'application/json'})
    access_token = json.loads(r.text).get('access_token')

    access_user_url = 'https://api.github.com/user'
    r = requests.get(access_user_url, headers={
                     'Authorization': 'token ' + access_token})
    return jsonify({
        'status': 'success',
        'data': json.loads(r.text)
    })


@app.route('/', methods=['GET', 'POST'])
def index():
    url = 'https://github.com/login/oauth/authorize'
    params = {
        'client_id': client_id,
        # 如果不填写redirect_uri那么默认跳转到oauth中配置的callback url。
        # 'redirect_uri': 'http://dig404.com/oauth2/github/callback',
        'scope': 'read:user',
        # 随机字符串，防止csrf攻击
        'state': 'An unguessable random string.',
        'allow_signup': 'true'
    }
    url = furl(url).set(params)
    return redirect(url, 302)


if __name__ == "__main__":
    app.run()
