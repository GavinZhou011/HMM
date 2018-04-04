#!/usr/bin/python
# -*-coding:utf-8

import sys
#import math
#import pdb

state_M = 4
word_N = 0

A_dic = {}              #状态转移概率矩阵
B_dic = {}              #观测概率矩阵
Count_dic = {}          #训练数据各状态总数
Pi_dic = {}             #初始状态概率矩阵
word_set = set()        #字集合
state_list = ['B', 'M', 'E', 'S']
line_num = -1

INPUT_DATA = "RenMinData.txt_utf8"
PROB_START = "prob_start.py"
PROB_EMIT = "prob_emit.py"
PROB_TRANS = "prob_trans.py"


def init():
    global state_M
    global word_N
    for state in state_list:
        A_dic[state] = {}
        for state1 in state_list:
            A_dic[state][state1] = 0.0
    for state in state_list:
        Pi_dic[state] = 0.0
        B_dic[state] = {}
        Count_dic[state] = 0


def getList(input_str):
    outpout_str = []
    if len(input_str) == 1:
        outpout_str.append('S')
    elif len(input_str) == 2:
        outpout_str = ['B', 'E']
    else:
        M_num = len(input_str) - 2
        M_list = ['M'] * M_num
        outpout_str.append('B')
        outpout_str.extend(M_list)
        outpout_str.append('S')
    return outpout_str


def Output():
    start_fp = open(PROB_START, 'w', encoding='UTF-8')
    emit_fp = open(PROB_EMIT, 'w', encoding='UTF-8')
    trans_fp = open(PROB_TRANS, 'w', encoding='UTF-8')

    print("len(word_set) = %s " % (len(word_set)))
    for key in Pi_dic:
        '''
        if Pi_dic[key] != 0:
            Pi_dic[key] = -1*math.log(Pi_dic[key] * 1.0 / line_num)
        else:
            Pi_dic[key] = 0
        '''
        Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
    print(Pi_dic, file=start_fp)

    for key in A_dic:
        for key1 in A_dic[key]:
            '''
            if A_dic[key][key1] != 0:
                A_dic[key][key1] = -1*math.log(A_dic[key][key1] / Count_dic[key])
            else:
                A_dic[key][key1] = 0
            '''
            A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
    print(A_dic, file=trans_fp)

    max_num = 0
    for key in B_dic:
        for word in B_dic[key]:
            '''
            if B_dic[key][word] != 0:
                B_dic[key][word] = -1*math.log(B_dic[key][word] / Count_dic[key])
            else:
                B_dic[key][word] = 0
            '''
            B_dic[key][word] = B_dic[key][word] / Count_dic[key]
            if(B_dic[key][word] > max_num):
                max_num = B_dic[key][word]
                print(max_num)
    print(B_dic, file=emit_fp)

    start_fp.close()
    emit_fp.close()
    trans_fp.close()


def train_file(filename):
    ifp = open(filename, encoding='UTF-8')
    global word_set
    global line_num
    for line in ifp:
        line_num += 1
        if line_num % 10000 == 0:
            print(line_num)


        line = line.strip()                         #移除字符串头尾的空格
        if not line: continue
        #line = line.decode("utf-8", "ignore")

        #更新word_set
        word_list = []
        for i in range(len(line)):
            if line[i] == " ": continue
            word_list.append(line[i])
        word_set = word_set | set(word_list)

        # 生成此行的状态序列
        lineArr = line.split(" ")                   #指定分隔符对字符串进行切片
        lineArr = filter(None, lineArr)             #过滤空格
        line_state = []
        for item in lineArr:
            line_state.extend(getList(item))

        if len(word_list) != len(line_state):
            print("[line_num = %d][word_list = %s][line_state = %s]" % (line_num, word_list, line_state), file=sys.stderr)
            input()
        else:
            for i in range(len(line_state)):
                if i == 0:
                    Pi_dic[line_state[0]] += 1
                    Count_dic[line_state[0]] += 1
                else:
                    A_dic[line_state[i - 1]][line_state[i]] += 1
                    Count_dic[line_state[i]] += 1
                    if word_list[i] not in B_dic[line_state[i]]:
                        B_dic[line_state[i]][word_list[i]] = 1
                    else:
                        B_dic[line_state[i]][word_list[i]] += 1
    ifp.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: [%s] [input_data1] [input_data2]" % (sys.argv[0]), file=sys.stderr)
        sys.exit(0)
    init()
    for i in range(len(sys.argv) - 1):
        print(sys.argv[i+1])
        train_file(sys.argv[i+1])
    Output()

if __name__ == "__main__":
    main()
