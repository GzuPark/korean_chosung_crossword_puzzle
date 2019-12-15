from utils import kor_char_chosung_decompose


def main():
    test_word = '딥러닝'

    result = []
    for chararcter in test_word:
        result.append(kor_char_chosung_decompose(ord(chararcter)))

    print(''.join(result))


if __name__ == '__main__':
    main()
