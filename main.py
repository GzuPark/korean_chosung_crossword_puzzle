import argparse
import os

from utils import kor_char_chosung_decompose


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default='example.txt')
    args = parser.parse_args()

    realpath = os.path.dirname(os.path.realpath(__file__))
    args.data_path = os.path.join(realpath, 'data')
    args.file_path = os.path.join(args.data_path, args.file)
    args.results_path = os.path.join(realpath, 'results')

    return args


def read_words(args):
    with open(args.file_path, 'r') as f:
        result = f.readlines()
    result = [word.replace('\n', '').rstrip() for word in result]

    return result


def main():
    args = get_args()
    words = read_words(args)

    result = []
    for word in words:
        temp = []
        for chararcter in word:
            temp.append(kor_char_chosung_decompose(ord(chararcter)))
        result.append(''.join(temp))

    print(result)


if __name__ == '__main__':
    main()
