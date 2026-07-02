import re
import sys

def find_chinese(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if re.search(r'[\u4e00-\u9fff]', line):
                print(f'{i}: {line.rstrip()}')

if __name__ == '__main__':
    find_chinese(sys.argv[1])
