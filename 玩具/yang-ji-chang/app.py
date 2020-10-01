from code_hard import *
import pandas as pd
import matplotlib.pyplot as plt



def users_ti_xian_record():
    from session_xy import session_data as xy
    from session_dyq import session_data as dyq
    # from session_ddd import session_data as ddd
    # from session_aaa import session_data as aaa

    users = [
        xy,
        dyq,
        # ddd,
        # aaa,
    ]
    users = sorted(users,key=lambda x: x['session_id'])
    return users

def users_ti_xian():
    from session_xy import session_data as xy
    from session_dyq import session_data as dyq
    # from session_ddd import session_data as ddd
    # from session_aaa import session_data as aaa
    from session_huawei import session_data as huawei
    from session_xiaomi import session_data as xiaomi
    from session_xsy import session_data as xsy

    users = [
        huawei,
        xiaomi,
        xsy,
        xy,
        dyq,
        # ddd,
        # aaa,
    ]
    users = sorted(users,key=lambda x: x['session_id'])
    return users

sheet_name = '养鸡场'
xlsx = f'/Users/zhoujie/Documents/zhoujie903/jie_suan/{sheet_name}.xlsx'
jie_shuang = '/Users/zhoujie/Desktop/dev/common/结算时间.xlsx'


def df_from_network():
    a = []
    for user in users_ti_xian_record():
        try:
            user = User(user)
            rs = ti_xian_history(user)
            a.extend(rs)
        except:
            pass
    df = pd.DataFrame(a)
    return df

def task_ti_xian():
    for user in users_ti_xian():
        try:
            user = User(user)
            logging.info(f'{user.session_id}')
            user.params['token'] = user.headers['Token']
            ti_xian(user)
        except:
            pass

def task_ti_xian_record(start_date=None):
    def filter_by_date(df, start_date=None):
        if start_date == None:
            jsdf = pd.read_excel(jie_shuang)
            start_date:pd.Series = pd.Series(jsdf[sheet_name].values, index=jsdf['tp_nickname'])

        l = []
        for user, date in start_date.iteritems():
            temp = df[ df['tp_nickname'] == user ]
            temp = temp[ temp['create_time'] > date ]
            temp = temp[ temp['status'] == '60' ]
            l.append(temp)

        df = pd.concat(l, ignore_index=True)
        return df

    df = df_from_network()
    df['create_time'] = pd.to_datetime(df['create_time'])
    df = filter_by_date(df)
    df.to_excel(xlsx,sheet_name=sheet_name)

    print(df)


    gb = df['balance'].astype('float').groupby(df['tp_nickname'])
    print(gb.sum().reset_index(name='sum'))

    gb = df['balance'].groupby([df['tp_nickname'],df['create_time']])
    print(gb.sum())

def task_coin_details():
    global users
    a = []
    for user in users:
        try:
            user = User(user)
            logging.info(f'{user.session_id}')
            rs = income(user)
            df = pd.DataFrame(rs,index=[item['title'] for item in rs])
            df['user'] = f'{user.session_id}'
            # df = df.reindex(df['title'])
            print(df)
            a.append(df)
        except:
            pass
    
    return a   

if __name__ == "__main__":

    # task_ti_xian()
  
    task_ti_xian_record()
