import sys
import pickle
from init import loadAlphabet

pinyin, chinese, index = loadAlphabet('data/alphabet.txt')
file = open("data/split-probability.pk", 'rb')
mats = pickle.load(file)
file.close()

def solve(plist):
    print(plist)
    dist = []
    frms = []
    for p in plist:
        # print(p, len(chinese[p]))
        if chinese.get(p) == None:
            return 'Error'
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
    while now > 0:
        mxp = frms[now][mxp]
        now -= 1
        if now > 0:
            ret = chinese[plist[now]][mxp] + ret
    return ret


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('error')
    else:
        ifname = sys.argv[1]
        ofname = sys.argv[2]

        ifile = open(ifname, 'r')
        ofile = open(ofname, 'w')

        if ifile == None:
            exit(0)

        ss = ifile.readlines()
        for s in ss:
            v = ('begin ' + s + ' end').split()
            print(solve(v))
