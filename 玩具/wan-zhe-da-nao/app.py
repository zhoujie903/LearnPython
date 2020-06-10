from code_hard import *
import pandas as pd
import matplotlib.pyplot as plt

from session_xy import session_data as xy
from session_dyq import session_data as dyq
from session_ddd import session_data as ddd

users = [
    xy,
    dyq,
    ddd,
]
users = sorted(users,key=lambda x: x['session_id'])

sheet_name = '王者大脑'
xlsx = f'{sheet_name}.xlsx'

def df_from_network():
    global users
    a = []
    for user in users:
        try:
            user = User(user)
            rs = ti_xian_history(user)
            a.extend(rs)
        except:
            pass
    df = pd.DataFrame(a)
    return df

if __name__ == "__main__":
  
    df = df_from_network()
    df.to_excel(xlsx,sheet_name=sheet_name)
    # df = pd.read_excel(xlsx,sheet_name=sheet_name)
    print(df)


    gb = df['balance'].astype('float').groupby(df['tp_nickname'])
    print(gb.sum().reset_index(name='sum'))

    gb = df['balance'].groupby([df['tp_nickname'],df['create_time']])
    print(gb.sum())