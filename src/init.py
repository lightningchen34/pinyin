import sys
import pickle
from ChineseTone import PinyinHelper, PinyinFormat

def fromAlphabet(filename):
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
            chinese[line[0]].append(value)
            if pinyin.get(value) == None:
                pinyin[value] = [line[0]]
            else:
                pinyin[value].append(line[0])
    return pinyin, chinese

def fromCorpus():
    file = open('data/main-corpus.pk', 'rb')
    data = pickle.load(file)
    print(data[0])
    s = PinyinHelper.convertToPinyinFromSentence('长大，成长，变长，长短，边长，很长，长老', pinyinFormat=PinyinFormat.WITHOUT_TONE)
    print(s)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('error')
    else:
        # filename = sys.argv[1]
        # pinyin, chinese = fromAlphabet(filename)
        # print(len(pinyin))
        fromCorpus()
        

