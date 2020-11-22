import copy
import re

from utils import Config, clear, pickle_load, preview


class Game(object):
    def __init__(self, problem, problem_id):
        self.problem = problem
        self.problem_id = problem_id
        self.solved = []

    def register_team(self):
        self.teams = []
        while True:
            clear()
            flag = True

            if len(self.teams) != 0:
                print('등록된 팀: {}'.format(len(self.teams)))
                for t in self.teams:
                    print(' {}'.format(t.name))
                print()
            team_name = input('팀 이름을 등록해주세요. (종료: Enter) ')
            if team_name == '':
                if len(self.teams) == 0:
                    _ = input('아직 한 팀도 등록이 되지 않았습니다. (계속하려면 Enter를 누르세요.)')
                    flag = False
                else:
                    break
            if flag is True:
                team = Team()
                team.name = team_name
                self.teams.append(team)
                print('{} 등록 완료!'.format(team.name))

    def view_problem(self):
        _cnt = len(self.game_env['words']) - len(self.solved)
        if _cnt == 0:
            high_score = 0
            winner = []
            for idx, team in enumerate(self.teams):
                if high_score < team.score:
                    high_score = team.score
                    winner = [team.name]
                elif high_score == team.score:
                    winner.append(team.name)
            print('\n\tWinner: {}'.format(' & '.join(winner)))
            print('\nID: {} 게임을 종료합니다.'.format(self.problem_id))
            exit(0)
        print('\n목록: {} 문제 남았습니다.'.format(_cnt))
        for idx, candidate in enumerate(self.game_env['words']):
            if candidate['word'] not in self.solved:
                print(' {:2d}:\t{} {}'.format(idx, candidate['direction'], candidate['grid']))

    def view_team_score(self):
        print('\n현재 점수:')
        for t in self.teams:
            print(' {:16s}: {:2d}'.format(t.name, t.score))

    def start(self):
        for row, line in enumerate(self.game_env['env']):
            for col, element in enumerate(line):
                if element == 0:
                    self.game_env['env'][row][col] = u'\u2588'u'\u2588'
                else:
                    self.game_env['env'][row][col] = '  '
        preview(self.game_env, with_answer=False)

    def update(self, selected):
        _word = self.game_env['words'][selected]
        col = _word['grid'][0]
        row = _word['grid'][1]
        word = _word['word']

        if _word['direction'] == 'V':
            for idx, letter in enumerate(word):
                self.game_env['env'][col+idx][row] = letter
        if _word['direction'] == 'H':
            self.game_env['env'][col][row:row+len(list(word))] = list(word)
        preview(self.game_env, with_answer=False)

        print()
        for idx, team in enumerate(self.teams):
            print(' {:2d}. {}'.format(idx, team.name))
        print()
        w_flag = True
        while (w_flag is True):
            winner = input('"{}" 문제를 맞춘 팀은? '.format(word))
            if re.match(r'^[0-9]+$', winner):
                if int(winner) in list(range(len(self.teams))):
                    print('\n의도한 답은 "{}" 입니다.'.format(_word['guide']))
                    w_flag = False
        winner = int(winner)
        self.teams[winner].score += 1

    def run(self):
        self.register_team()
        clear()
        for t in self.teams:
            print(' {}'.format(t.name))
        print()
        _ = input('{}팀 등록 완료!'.format(len(self.teams)))

        self.game_env = copy.deepcopy(self.problem)

        total = len(self.problem['words'])
        flag = True
        selected = -1
        while (len(self.solved) < total):
            clear()
            if flag is True:
                self.start()
                flag = False
            else:
                _w = self.game_env['words'][selected]
                if _w['word'] not in self.solved:
                    self.solved.append(_w['word'])
                self.update(selected)
            self.view_team_score()
            self.view_problem()
            print()
            q_flag = True
            while (q_flag is True):
                selected = input('문제를 선택해주세요. ')
                if re.match(r'^[0-9]+$', selected):
                    if int(selected) in list(range(len(self.game_env['words']))):
                        q_flag = False
            selected = int(selected)


class Team(object):
    name = 'ANAIN'
    score = 0


def select_problem(db):
    problem_list = [(k, v['grid']) for k, v in db.items()]
    s_flag = True
    p_flag = True
    _id = ''
    selected = None

    while p_flag:
        clear()

        while s_flag:
            print('문제 {:14s}  {:8s}'.format('ID', '크기'))
            for i, p in enumerate(problem_list):
                print('{:3d}. {}, {}'.format(i, p[0], p[1]))

            print()
            selection = input('문제를 선택해주세요. (Number / (S)earch) ')
            if re.match(r'^[0-9]+$', selection):
                _id = problem_list[int(selection)][0]
                selected = db[_id]
                s_flag = False
            elif re.match(r'^s[0-9]{14}', selection.lower()):
                _id = selection.replace('s', '')
                selected = db[_id]
                s_flag = False
            else:
                clear()
                print('잘못된 선택입니다. 다시 선택해주세요.\n')

        clear()
        do_preview = input('미리보기를 하시겠습니까? (y/n) ')
        if do_preview.lower() in ['y', 'yes']:
            preview(selected)
            print()
            do_back = input('다른 문제를 선택하시겠습니까? (y/n) ')
            if do_back.lower() in ['y', 'yes']:
                s_flag = True
            else:
                p_flag = False
        else:
            p_flag = False
    return (_id, selected)


def main():
    db = pickle_load(Config.db_path)
    id, problem = select_problem(db)

    clear()
    _ = input('ID: {} 게임을 시작합니다!\n\n\t아무거나 입력하고 Enter를 누르세요.'.format(id))
    game = Game(problem, id)
    game.run()


if __name__ == '__main__':
    main()
