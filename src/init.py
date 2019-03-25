import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('error')
    else:
        filename = sys.argv[1]
        file = open(filename, 'r', encoding='utf-8')

        set = file.readlines()

        pinyin = dict()
        for line in set:
            line = line.strip()
            line = line.split(' ')
            for value in line:
                if value == line[0]:
                    continue
                pinyin[value] = line[0]

        print(len(pinyin))
