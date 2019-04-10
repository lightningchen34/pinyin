import sys
import pickle
import random
import numpy as np

from ChineseTone import PinyinHelper, PinyinFormat

def translate(cn):
    ret = PinyinHelper.convertToPinyinFromSentence(cn, pinyinFormat=PinyinFormat.WITHOUT_TONE)
    for i in range(len(ret)):
        if ret[i] == 'lve':
            ret[i] = 'lue'
        if ret[i] == 'nve':
            ret[i] = 'nue'
        if ret[i] == 'r':
            ret[i] = 'er'
    return ret

def loadAlphabet(filename):
    file = open(filename, 'r', encoding='utf-8')

    set = file.readlines()

    pinyin = dict()
    chinese = dict()
    chars = 0
    index = dict()
    for line in set:
        line = line.strip()
        line = line.split(' ')
        chinese[line[0]] = []
        for value in line:
            if value == line[0]:
                continue
            if index.get(value) == None:
                index[value] = chars
                chars += 1
            if pinyin.get(value) == None:
                pinyin[value] = [line[0]]
            else:
                pinyin[value].append(line[0])
            chinese[line[0]].append(value)
    return pinyin, chinese, index

def formatCorpus():

    def write(num, sentences):
        filename = "data/part{}-corpus.pk".format(num)
        file = open(filename, 'wb')
        pickle.dump(sentences, file)
        file.close()
        sentences.clear()

    def load(filename, index, sentences, tot, filetot):
        file = open(filename, 'rb')
        data = pickle.load(file)
        file.close()
        for value in data:
            tot = tot + 1
            print(tot)
            sens = value[index]
            slist = list(sens)
            spin = translate(sens)
            tmp_sen = ''
            tmp_pin = ''
            for j in range(len(slist)):
                if slist[j] == spin[j]:
                    if tmp_sen == '':
                        continue
                    sentences.append([tmp_sen])
                    if len(sentences) >= 1048576:
                        filetot += 1
                        write(filetot, sentences)
                    tmp_pin = ''
                    tmp_sen = ''
                else:
                    tmp_sen = tmp_sen + slist[j]
                    if tmp_pin == '':
                        tmp_pin = spin[j]
                    else:
                        tmp_pin = tmp_pin + ' ' + spin[j]
        return tot, filetot
    
    sentences = []
    tot = 0
    filetot = 0

    tot, filetot = load('data/main-corpus.pk', 'html', sentences, tot, filetot)
    tot, filetot = load('data/main-corpus.pk', 'title', sentences, tot, filetot)
    tot, filetot = load('data/sec-corpus.pk', 'title', sentences, tot, filetot)
    tot, filetot = load('data/sec-corpus.pk', 'content', sentences, tot, filetot)
    
    print(tot, filetot)

def loadCorpus(num):
    filename = "data/part{}-corpus.pk".format(num)
    file = open(filename, 'rb')
    data = pickle.load(file)
    file.close()
    return data

def init_probability(chinese, index):
    totmat = np.zeros((len(index), len(index)), np.int32)
    for i in range(48):
        print(i + 1)
        data = loadCorpus(i + 1)
        for item in data:            
            cn = list('【' + item[0] + '】')
            skip = False
            for x in cn:
                if index.get(x) == None:
                    skip = True
                    break
            if skip:
                continue
            l = len(cn)
            for j in range(l - 1):
                i1 = index[cn[j]]
                i2 = index[cn[j + 1]]
                totmat[(i1, i2)] += 1
    print('done')

    filename = "data/tot-probability.pk"
    file = open(filename, 'wb')
    pickle.dump(totmat, file)
    file.close()

    # return totmat

def split_probability(chinese, index):

    file = open("data/tot-probability.pk", 'rb')
    mat = pickle.load(file)
    file.close()

    mats = dict()
    pys = len(chinese)
    tot = 0

    def softmax(m):
        tmp1 = np.average(m, axis=1)
        tmp2 = np.max(m, axis=1)
        tmp = np.sqrt(tmp1 * tmp2)
        tmp = np.sqrt(tmp * tmp2)
        # tmp = np.sqrt(tmp)
        m /= tmp.reshape((m.shape[0], 1))
        m = np.exp(m)
        tmp = np.sum(m, axis=1)
        m /= tmp.reshape((m.shape[0], 1))
        m = -np.log(m)
        return m

    for k1, v1 in chinese.items():
        for k2, v2 in chinese.items():
            l1 = len(v1)
            l2 = len(v2)
            tot += l1 * l2
            tmp = np.zeros((l1, l2))
            for i1 in range(len(v1)):
                for i2 in range(len(v2)):
                    tmp[(i1, i2)] = mat[(index[v1[i1]], index[v2[i2]])]
            # print(k1, k2, np.sum(tmp))
            mats[(k1, k2)] = softmax(tmp)

    print(tot)

    file = open("data/split-probability.pk", 'wb')
    pickle.dump(mats, file)
    file.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('error')
    else:
        filename = sys.argv[1]
        pinyin, chinese, index = loadAlphabet(filename)
        # print(len(chinese))

        # formatCorpus()
        
        # mat = init_probability(chinese, index)

        split_probability(chinese, index)


        file = open("data/split-probability.pk", 'rb')
        mat = pickle.load(file)
        file.close()
        tot = 0
        for k, v in mat.items():
            print(k, v)
            tot += 1
            if tot == 100:
                break