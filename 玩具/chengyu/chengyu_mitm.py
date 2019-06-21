import json
import argparse

from mitmproxy import ctx

'''
> mitmdump -s chengyu_mitm.py '~u websock_m/websock_message'
'''

Red = '\033[0;31m'
Green = '\033[0;32m'
Yellow = '\033[0;33m' 
Blue = '\033[0;34m'
Purple = '\033[0;35m' 
Cyan = '\033[0;36m'  
White = '\033[0;37m' 

colors = {
    0:Red,
    1:Purple,
    2:Yellow,
    3:Blue,
    4:White,
}

class Chengyu(object):
    def __init__(self):
        self.dictpath = '/Users/zhoujie/chengyu.text' 
        self.chengyu = set()
        with open(self.dictpath, 'rt') as f:
            for line in f.readlines():
                self.chengyu.add(line.strip())
        
        self.answers = list()
        self.ask_string = ''
        self.ask_dict = dict()

    # General lifecycle
    def load(self, loader):
        ctx.log.info('\033[1;31mevent: load\033[0m')

    def configure(self, updated):
        ctx.log.info('\033[1;31mevent: configure\033[0m')



    # Websocket lifecycle
    def websocket_message(self, flow):
        """
            Called when a WebSocket message is received from the client or
            server. The most recent message will be flow.messages[-1]. The
            message is user-modifiable. Currently there are two types of
            messages, corresponding to the BINARY and TEXT frame types.
        """

        ctx.log.info('\033[1;31m websocket_message \033[0m')
        
        # get the latest message
        message = flow.messages[-1]

        # simply print the content of the message
        ctx.log.info('')
        ctx.log.info(message.content)
        ctx.log.info('')

        m = json.loads(message.content)
        t = m['type']
        if m.get('ask_string'):
            ask_string = m['ask_string']            
            self.ask_string = ask_string        
            # 计算答案
            self.find_answers_v2(ask_string)

        # 删除已回答正确的答案
        if m.get('ack') == 1:
            self.answers.remove(m['answer'])

        # 自动答题
        # self.auto_answer(flow)

        # 显示答案
        self.print_answers()


        # 把答案增加到内存字典中
        self.__add_new_worlds_to_memory(m)        

    def websocket_end(self, flow):
        """
            A websocket connection has ended.
        """
        ctx.log.info('\033[1;31m websocket_end \033[0m')

        with open(self.dictpath, 'wt') as f:
            l = list(self.chengyu)
            l.sort()
            for item in l:
                f.write(item)
                f.write('\n')


    # ---------------------------------------------
    def find_answers_v2(self, ask_string):
        '''
            在内存成语字典查找答案
        '''      
        ask_set = set(ask_string)
        self.ask_dict = dict( zip(ask_string, range(len(ask_string))))

        max_count = len(ask_string) / 4          
        for item in self.chengyu:
            item_set = set(item)
            if not (item_set - ask_set):
                self.answers.append(item)
                if max_count <= len(self.answers):
                    return

    def auto_answer(self, flow):
        if len(self.answers):
            item = self.answers[0]
            answer_index = [ str(self.ask_dict[c])  for c in item ]
            ask_string = self.ask_string
            while len(set(answer_index)) < 4:
                index = 0
                for i, v in enumerate(answer_index):
                    c = ask_string[int(v)]
                    index = ask_string.find(c,index)
                    print(index, v)
                    if index != -1:
                        answer_index[i] = str(index)
                    index += 1

            send_message = {
                'answer': self.answers[0],
                'answer_index': answer_index,
                'type': 'answer'
            }
            mm = json.dumps(send_message)
            print(mm)
            # 向服务器发送消息
            flow.inject_message(flow.server_conn, mm)


    def __add_new_worlds_to_memory(self, m):
        '''
            把答案增加到内存字典中
        '''
        if m['type'] == 'game_result':
            self.answers.clear()
            for answer in m['all_answer']:
                self.chengyu.add(answer['phrase'])

            ctx.log.info('\033[1;31m 共收录{}个成语 \033[0m'.format(len(self.chengyu)))

    def print_answers(self):
        '''
            图形化、色彩化显示答案
        '''        
        ask_string = self.ask_string
        length = len(ask_string)

        for item in self.answers:
            self.print_color(item)
            self.print_color('--'*6)

            global colors, White
            for i, c in enumerate(ask_string, 1):
                end = ''
                if i % 6 == 0 or i == length:
                    end = '\n'                
                
                color = White
                if c in item:                    
                    color = colors[item.index(c)]

                self.print_color(c, end=end, color=color)

            self.print_color('--'*6)

    def print_color(self, message, end='\n', color=Red):
        print('{}{}\033[0m'.format(color, message), end=end)



addons = [
    Chengyu()
]

# if __name__ == "__main__":
#     c = Chengyu()

#     ask_string = '腊见家义降德若功赎仁判悲生升道肘两身乐极尽立罪春命明回人捉襟性暗'
#     c.ask_string = ask_string
#     c.find_answers_v2(ask_string)
#     c.print_answers()

    

