# Crossword Puzzle for 딥러닝 초성 게임

## 개요

ANAIN 모임의 딥러닝 초성 게임을 Crossword Puzzle 형식으로 만들기 위해 주어진 단어 데이터베이스를 바탕으로 문제를 자동 생성해주는 프로그램입니다.

## 사용 방법

1. 초성 문제에 쓸 단어들을 [example.txt](./data/example.txt)처럼 만들어주세요.
2. `generate.py` 실행하여 문제들을 만들어 줍니다.
    - `--file`: 문제에 사용할 단어들이 있는 text 파일
    - `--dim`: Crossword puzzle 크기 (예: `15 15`)
    - `--timeout`: 문제를 만드는데 소요되는 최대 시간 (sec)
    - `--capacity`: 단어가 puzzle grid에 차지하는 한도 용량
3. `play.py` 실행하여 문제를 풀어봅시다!
    - 생성된 문제 목록 중 선택
    - 팀 등록은 1개 이상
