import json
import time
import collections

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

        # {'和':[1,8], '我':[11]}
        self.char_indexs_dict = dict()

        # {1:'和', 8:'和', 11:'我'}
        self.index_char_dict = dict()

        self.count = 0

        # 自动提交答案的网络发送次数
        self.auto_send_count = 0

        # 自动发送的成语
        self.auto_send_list = list()

        # 服务器确定正确的成语
        self.ack_true_list = list()

        # 找到的的成语中各异字符为2个的答案数量：如 [真真假假]
        self.answer_2chars_count = 0

        # {'中流砥柱':[1,9,21,25]}
        self.answer_indexs_dict = dict()

        # {'中流砥柱':set('中流砥柱')}
        self.answer_charset_dict = dict()

        # 查找到的错误答案
        self.error_answers = []

        # 玩了多少局
        self.play_times = 0

        self.firt_auto_answer = True



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
        message_type = m['type']
        if m.get('ask_string'):
            self.ask_string = m['ask_string']
            # 计算答案
            self.find_answers_v2(self.ask_string)
            self.play_times += 1

        # {"answer": "\u957f\u9a71\u76f4\u5165", "answer_index": ["0", "20", "43", "41"], "type": "answer"}
        if message_type == 'answer':
            self.answer_indexs_dict[m['answer']] = m['answer_index']

        # 删除已回答正确的答案
        ack = False

        # {"answer":"长驱直入","type":"answer_ack","seq":0,"ack":1}
        if m.get('ack') == 1:

            answer = m['answer']
            self.ack_true_list.append(answer)
            answer_index = self.answer_indexs_dict.get(answer,[])
            for i in answer_index:
                self.index_char_dict[int(i)] = '  '

            for c,i in zip(answer,answer_index):                
                indexs = self.char_indexs_dict[c]
                indexs.remove(int(i))

            try:
                ack = True
                self.answers.remove(m['answer'])
            except:
                pass

        if message_type == 'answer_ack' and m.get('ack') == 0:
            pass


        # 自动答题
        if message_type == 'answer_ack' or self.firt_auto_answer:
            
            self.auto_answer(flow)

        # 显示答案
        if len(self.ask_string):
            self.print_answers()


        if message_type == 'game_result':
            # 把答案增加到内存字典中
            self.__add_new_worlds_to_memory(m)

            self.reset_data_to_init()


    def websocket_end(self, flow):
        """
            A websocket connection has ended.
        """
        ctx.log.info('\033[1;31m websocket_end \033[0m')

        self.reset_data_to_init()

        if self.play_times % 5 == 0:
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
        for i, c in enumerate(ask_string):
            self.char_indexs_dict.setdefault(c, []).append(i)
        self.index_char_dict = dict( zip(range(len(ask_string)), ask_string))

        max_count = len(ask_string) / 4
        for item in self.chengyu:
            item_set = self.answer_charset_dict.setdefault(item, set(item))
            if not (item_set - ask_set):
                self.answers.append(item)
                if len(item_set)<4:
                    self.answer_2chars_count += 1
                if len(self.answers) - self.answer_2chars_count >= max_count :
                    self.count = len(self.answers)
                    return
        self.count = len(self.answers)

    def auto_answer(self, flow):
        while len(self.answers) > 0:
            item = self.answers[0]
            answer_index = []
            counter = collections.Counter(item)

            b_continue = False
            for char, count in counter.items():
                if len(self.char_indexs_dict[char]) < count:
                    self.error_answers.append(item)
                    self.answers.remove(item)
                    b_continue = True
                    break # break for

            if b_continue:
                continue

            char_index = {}
            for c in item:                
                x = char_index.get(c, 0)
                index = self.char_indexs_dict[c][x]
                answer_index.append( str(index) )
                char_index[c] = x+1

            if len(set(answer_index)) < 4:
                ctx.log.error(f'?算法有错误：{answer_index} 小于4')
                continue

            send_message = {
                'answer': item,
                'answer_index': answer_index,
                'type': 'answer'
            }
            mm = json.dumps(send_message)
            # -----------------------
            print(mm)
            # -----------------------
            self.answer_indexs_dict[item] = answer_index
            # 向服务器发送消息
            if not flow.ended and not flow.error:
                self.firt_auto_answer = False
                self.auto_send_count += 1
                self.auto_send_list.append(item)
                self.answers.remove(item)
                time.sleep(2)
                flow.inject_message(flow.server_conn, mm)
                break




    def __add_new_worlds_to_memory(self, m):
        '''
            把答案增加到内存字典中
        '''
        for answer in m['all_answer']:
            self.chengyu.add(answer['phrase'])

        ctx.log.info('\033[1;31m 共收录{}个成语 \033[0m'.format(len(self.chengyu)))
        ctx.log.info(f'\033[1;31m 共玩了 {self.play_times} 局\033[0m')

    def print_answers(self):
        '''
            图形化、色彩化显示答案
        '''
        self.print_color(self.ask_string)
        self.print_color('共找到 {}/{} 个成语'.format(self.count, len(self.ask_string)//4))
        self.print_color('错误成语 {}'.format(self.error_answers))
        self.print_color('共自动 {} 次提交'.format(self.auto_send_count))
        self.print_color('自动{:2}个：{}'.format(len(self.auto_send_list),self.auto_send_list))
        self.print_color('确认{:2}个：{}'.format(len(self.ack_true_list),self.ack_true_list))
        for item in self.answers:
            self.print_color(item)
            self.print_matrix(item)

        if (not self.answers) and self.index_char_dict:
            self.print_matrix()


    def print_matrix(self, item = []):
        '''
        item: '腊尽春回' or []
        '''
        chars_in_line = 6
        length = len(self.ask_string)

        lines = (length + chars_in_line - 1) // chars_in_line
        PADDING = ' '*(lines * chars_in_line - length)
        is_need_padding = len(PADDING) != 0

        global colors, White
        
        self.print_color('--'*chars_in_line)

        for i, c in self.index_char_dict.items():
            end = ''
            if (i+1) % chars_in_line == 0 or (i+1) == length:
                end = '\n'

            color = White
            if c in item:
                color = colors[item.index(c)]

            line, first = divmod(i, chars_in_line)
            if is_need_padding and first == 0 and (line + 1 == lines):
                c = PADDING + c

            self.print_color(c, end=end, front_color=color)

        self.print_color('--'*chars_in_line)

    def print_color(self, message, end='\n', front_color=Red):
        print(f'{front_color}{message}\033[0m', end=end)


    def reset_data_to_init(self):
        self.ask_string = ''
        self.answers.clear()
        self.index_char_dict.clear()

        self.count = 0
        self.auto_send_count = 0
        self.answer_2chars_count = 0

        self.answer_indexs_dict.clear()
        self.char_indexs_dict.clear()
        self.error_answers.clear()
        self.ack_true_list.clear()
        self.auto_send_list.clear()
        self.firt_auto_answer = True


addons = [
    Chengyu()
]

if __name__ == "__main__":
    c = Chengyu()

    ask_string = '腊见家义降德若功赎仁判悲生升道肘两身乐极尽立罪春命明回人捉襟性暗'
    ask_string = '来戴恶自唇而怙到生二不马亡竹锲寒擒梅香听寒星圆其十贼其鸟舍悛口一自不月披青擒王说曝手然擒一齿齿石'
    ask_string = '侧拨扮相大拔挈然纲打富提敲如涌门见助济行踽全弄轩责刀危踽击贫独波可云岌日班思求斧乔备泉领旁岌劫装'
    c.ask_string = ask_string
    c.find_answers_v2(ask_string)
    print(c.answers)
    c.print_answers()



