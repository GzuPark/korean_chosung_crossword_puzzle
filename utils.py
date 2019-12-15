def kor_char_chosung_decompose(x):
    """
    https://github.com/naver/ai-hackathon/blob/ai_hackathon_1st/missions/examples/movie-review/example/kor_char_parser.py
    """
    cho = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"  # len = 19

    if x < ord('가') or x > ord('힣'):
        if x == ord(' '):
            return chr(x)
        else:
            raise ValueError('가 - 힣 범위에 있는 글자가 아닙니다. -> [{}]'.format(chr(x)))
    x = (x - ord('가')) // 28 // 21

    return cho[x]
