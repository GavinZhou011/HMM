#!/usr/bin/python
# -*-coding:utf-8

#import os
import sys
#import pdb


line_num = -1


def load_model(f_name):
    ifp = open(f_name, 'rb')
    return eval(ifp.read())


prob_start = load_model("prob_start.py")
prob_trans = load_model("prob_trans.py")
prob_emit = load_model("prob_emit.py")


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]  # tabular
    path = {}
    for y in states:  # init
        V[0][y] = start_p[y] * emit_p[y].get(obs[0], 0)
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            #(prob, state) = max(
            #    [(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(obs[t], 0), y0) for y0 in states if V[t - 1][y0] > 0])
            (prob, state) = max(
                [(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(obs[t], 0), y0) for y0 in states])
            V[t][y] = prob * 1000
            #print(prob)
            newpath[y] = path[state] + [y]
        path = newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])


def cut(sentence):
    # pdb.set_trace()
    prob, pos_list = viterbi(sentence, ('B', 'M', 'E', 'S'), prob_start, prob_trans, prob_emit)
    return (prob, pos_list)


def trans(test_str, pos_list):
    des_str = []
    for (word,flag) in zip(test_str,pos_list):
        if (flag == 'S') | (flag == 'B'):
            des_str.append(' ')
        des_str.append(word)
    s_str = "".join(des_str)
    return(s_str.lstrip())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: [%s] [test_file] [target_file]" % (sys.argv[0]), file=sys.stderr)
        sys.exit(0)
    ifp = open(sys.argv[1], encoding='UTF-8')
    ofp = open(sys.argv[2], 'w', encoding='UTF-8')


    for line in ifp:
        line_num += 1
        if line_num % 1000 == 0:
            print(line_num)

        line = line.strip()  # 移除字符串头尾的空格
        if not line: continue

        prob, pos_list = cut(line)
        line = (trans(line, pos_list))
        #print(line)

        ofp.write(line+'\n')

    ifp.close()
    ofp.close()