import json
import requests

# 利用有道翻译API，把需要翻译的内容做为参数，传到相应的 url 里。
# 然后通过有道的服务器返回一个 json 数据，我们就可以获得相应的翻译结果


def translate(word):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key = {
        'type': 'json',
        'i': word,
        'doctype': 'json',
        'version': '2,1',
        'keyfrom': 'fany.web',
        'ue': 'UTF-8',
        'action': 'FY_BY_CLICKBUTTON',
        'typoResult': 'true'
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        return response.text
    else:
        print('有道词典调用失败')
        return None


def get_result(response):
    result = json.loads(response)
    print("输入的词为：%s" % result['translateResult'][0][0]['src'])
    print("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])


def main():
    print("本程序调用有道词典的API进行翻译，可达到以下效果：")
    print("外文-->中文")
    print("中文-->英文")
    word = input('请输入你想要翻译的词或句：')
    list_trans = translate(word)
    get_result(list_trans)


if __name__ == '__main__':
    main()
