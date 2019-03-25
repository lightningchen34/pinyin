import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('error')
    else:
        ifname = sys.argv[1]
        ofname = sys.argv[2]

        ifile = open(ifname, 'r')
        ofile = open(ofname, 'w')

        ofile.write('清华大学计算机系\n我上学去了\n今天回家比较晚\n两会在北京召开\n')
