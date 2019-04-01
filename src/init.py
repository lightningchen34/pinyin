import sys
import pickle
import random
import numpy as np

from ChineseTone import PinyinHelper, PinyinFormat

def loadAlphabet(filename):
    file = open(filename, 'r', encoding='utf-8')

    set = file.readlines()

    pinyin = dict()
    chinese = dict()
    for line in set:
        line = line.strip()
        line = line.split(' ')
        chinese[line[0]] = []
        for value in line:
            if value == line[0]:
                continue
            if pinyin.get(value) == None:
                pinyin[value] = [(line[0], len(chinese[line[0]]))]
            else:
                pinyin[value].append((line[0], len(chinese[line[0]])))
            chinese[line[0]].append(value)
    return pinyin, chinese

def formatCorpus():

    def write(num, sentences):
        filename = "data/part{}-corpus.pk".format(num)
        file = open(filename, 'wb')
        pickle.dump(sentences, file)
        file.close()
        sentences.clear()

    def load(filename, index, important, sentences, tot, filetot):
        file = open(filename, 'rb')
        data = pickle.load(file)
        file.close()
        for value in data:
            tot = tot + 1
            print(tot)
            sens = value[index]
            slist = list(sens)
            spin = PinyinHelper.convertToPinyinFromSentence(sens, pinyinFormat=PinyinFormat.WITHOUT_TONE)
            tmp_sen = ''
            tmp_pin = ''
            for j in range(len(slist)):
                if slist[j] == spin[j]:
                    if tmp_sen == '':
                        continue
                    sentences.append([tmp_sen, tmp_pin, important])
                    if len(sentences) >= 1048576:
                        filetot += 1
                        write(filetot, sentences)
                    tmp_pin = ''
                    tmp_sen = ''
                else:
                    tmp_sen = tmp_sen + slist[j]
                    if spin[j] == 'lve':
                        spin[j] = 'lue'
                    if tmp_pin == '':
                        tmp_pin = spin[j]
                    else:
                        tmp_pin = tmp_pin + ' ' + spin[j]
        return tot, filetot
    
    sentences = []
    tot = 0
    filetot = 0

    tot, filetot = load('data/main-corpus.pk', 'html', 2, sentences, tot, filetot)
    tot, filetot = load('data/main-corpus.pk', 'title', 1, sentences, tot, filetot)
    tot, filetot = load('data/sec-corpus.pk', 'title', 4, sentences, tot, filetot)
    tot, filetot = load('data/sec-corpus.pk', 'content', 5, sentences, tot, filetot)
    
    print(tot, filetot)

def loadCorpus(num):
    filename = "data/part{}-corpus.pk".format(num)
    file = open(filename, 'rb')
    data = pickle.load(file)
    file.close()
    return data

def init_probability(chinese, pinyin):
    pys = len(chinese)
    mats = dict()
    for keyi, valuei in chinese.items():
        for keyj, valuej in chinese.items():
            a = len(valuei)
            b = len(valuej)
            mats[(keyi, keyj)] = np.zeros((a, b))
    cnt = 0

    def find_id(cn, py):
        if pinyin.get(cn) == None:
            return -1
        for item in pinyin[cn]:
            if item[0] is py:
                return item[1]
        return -1

    for i in range(1):
        data = loadCorpus(i + 1)
        for item in data:
            cnt += 1
            print(cnt, item)
            cn = list(item[0])
            py = item[1].split(' ')
            skip = False
            for x, y in zip(cn, py):
                if find_id(x, y) == -1:
                    skip = True
                    break
            if skip:
                continue
            l = len(py)
            for j in range(l - 1):
                i1 = find_id(cn[j], py[j])
                i2 = find_id(cn[j + 1], py[j + 1])
                mats[(py[j], py[j + 1])][(i1, i2)] += 1
    return mats

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('error')
    else:
        filename = sys.argv[1]
        pinyin, chinese = loadAlphabet(filename)
        # print(pinyin['惇'])
        print(len(chinese))

        # formatCorpus()
        
        # data = loadCorpus(10)
        # random.shuffle(data)
        # print(data[0:10])

        mats = init_probability(chinese, pinyin)

