import sys
import pickle
import random
from init import loadAlphabet, loadCorpus, translate

pinyin, chinese, index = loadAlphabet('data/alphabet.txt')
file = open("data/split-probability.pk", 'rb')
mats = pickle.load(file)
file.close()

def train(plist, clist, lr):
    if lr < 1e-8: lr = 1e-8
    if lr > 1e-1: lr = 1e-1
    dist = []
    frms = []
    for p in plist:
        # print(p, len(chinese[p]))
        if chinese.get(p) == None:
            print(p, plist, clist)
            return 0, 0
        dist.append([1e50 for _ in chinese[p]])
        frms.append([-1 for _ in chinese[p]])
    dist[0][0] = 0
    for i in range(len(plist)):
        if i == 0: continue
        mat = mats[(plist[i - 1], plist[i])]
        for j in range(len(chinese[plist[i]])):
            for k in range(len(chinese[plist[i - 1]])):
                if dist[i][j] > dist[i - 1][k] + mat[(k, j)]:
                    dist[i][j] = dist[i - 1][k] + mat[(k, j)]
                    frms[i][j] = k
    now = len(plist) - 1
    mxp = 0
    ret = ''
    right = 0
    while now > 0:
        oldmxp = mxp
        mxp = frms[now][mxp]
        now -= 1
        if chinese[plist[now]][mxp] == clist[now] and chinese[plist[now + 1]][oldmxp] == clist[now + 1]:
            mats[(plist[now], plist[now + 1])][(mxp, oldmxp)] *= 1.0 - lr
        else:
            mats[(plist[now], plist[now + 1])][(mxp, oldmxp)] *= 1.0 + lr * 0.05
        if now > 0 and chinese[plist[now]][mxp] == clist[now]:
            right += 1
    return right, len(plist) - 2
    # return ret


if __name__ == '__main__':
    for t in range(10000):
        for i in range(48):
            data = loadCorpus(i + 1)
            random.shuffle(data)

            right_sen, tot_sen = 0, 0
            right_word, tot_word = 0, 0
            for j in range(len(data) // 1000):
                cn = data[j][0]
                py = translate(cn)
                cn = list('【' + cn + '】')
                py = ['begin'] + py + ['end']
                mnr, mxr, s = 10000, 0, 0
                for k in range(20):
                    r, s = train(py, cn, lr = 5e-3)
                    if r < mnr: mnr = r
                    if r > mxr: mxr = r
                print("Case {}.{} : {} / {}          ( + {} )".format(i + 1, j + 1, mxr, s, mxr - mnr))
                right_word += mxr
                tot_word += s
                if tot_word > 0:
                    tot_sen += 1
                    if r == s: right_sen += 1
            
            print("Case {} done, Sentences: {}, Words: {}".format(i + 1, right_sen / tot_sen, right_word / tot_word))
            
            file = open("data/split-probability.pk", 'wb')
            pickle.dump(mats, file)
            file.close()