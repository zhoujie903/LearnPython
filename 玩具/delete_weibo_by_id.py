import requests
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Referer': 'https://weibo.com/u/1969776354/home?topnav=1&wvr=6',
    'Cookie': 'SINAGLOBAL=9310709215645.678.1544579888936; ULV=1553332608255:26:13:5:1783307815786.4724.1553332608215:1553175241107; UOR=,,login.sina.com.cn; SCF=Agq7TrBB2gvuVfzO8AQFLEY2LP1RyuCxrGkYqysE3f1Y9OIKVwsxNZ4_I2yNStNRl7IdmrQJJnGjlCA22I_JTZg.; SUHB=0P1NOkJQmT873m; UM_distinctid=167db866df4612-0febfb366338c6-4a566b-1aeaa0-167db866df667a; wb_cmtLike_1969776354=1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWdD50x8DOLA31FZHPjG2De5JpX5KMhUgL.Fo24So.NS0q0SKB2dJLoIEBLxKBLBonL1h5LxK-L1K5LB.zLxKqLBo2L1-qLxK-LBo2LBo2t; ALF=1584868557; YF-Page-G0=e1a5a1aae05361d646241e28c550f987|1553332608|1553332555; SUB=_2A25xkYkDDeRhGedH7VsW9yjPzjiIHXVS5v3LrDV8PUNbmtBeLRDTkW9NUIaM0Jq30i0iaA3jMLoB54ms1tPOpZHo; SSOLoginState=1553332562; YF-V5-G0=340a8661f2b409bf3ea4c8981c138854; _s_tentry=login.sina.com.cn; Apache=1783307815786.4724.1553332608215; wb_view_log_1969776354=1680*10502; webim_unReadCount=%7B%22time%22%3A1553332613684%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'
} 

t = requests.get(
    'https://weibo.com/1969776354/profile?profile_ftype=1&is_ori=1#_0', headers=headers).text

idx = re.findall('<a name=(\d+)', t, re.S)

for x in idx:
    print(x)
    datax = {'mid': x}

    # 4344002096965640代表这条微博：杨树林丫蛋小品《幸福快递》，杨树林成夫妻关系调解员？ 北京卫视春晚2017
    if x == '4344002096965640':
        break
    else:
        html = requests.post('https://weibo.com/aj/mblog/del?ajwvr=6', data=datax, headers=headers).text            
        print(html)
