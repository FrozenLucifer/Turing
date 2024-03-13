from typing import List, Tuple, Callable
from itertools import combinations_with_replacement


def is_all_a(s: str):
    is_turing_str(s)
    s = s[1:-1]
    if len(s) == 0:
        return "*# "
    if set(s) == {'a'}:
        return "*1 "
    return "*0 "


class TuringElem:
    def __init__(self, q_in, l_in, q_out, l_out, dir):
        self.q_in = q_in
        self.l_in = l_in
        self.q_out = q_out
        self.l_out = l_out
        self.dir = dir

    def __repr__(self):
        return f'(q{self.q_in}, {self.l_in}) -> (q{self.q_out}, {self.q_out}, {self.dir})'


def is_turing_str(s: str):
    if s[0] != '*':
        raise Exception("Дорожка должна начинаться на *")
    if s[-1] != ' ':
        raise Exception("Дорожка должна заканчиваться пробелом")


R = 'R'
L = 'L'
Q_END = -1


class TuringMachine:
    def __init__(self):
        self.commands: List[TuringElem] = []
        self.add(TuringElem(0, '*', 0, '*', R))

    def add(self, elem: TuringElem | Tuple[int, str, int, str, str]):
        if isinstance(elem, tuple):
            elem = TuringElem(*elem)
        for com in self.commands:
            if com.q_in == elem.q_in and com.l_in == elem.l_in:
                raise Exception(
                    f'Машина Тюринга должна быть детерменизированной! Переход (q{com.q_in},  {com.l_in}) уже есть!')
        self.commands.append(elem)

    def print(self, sort=False):
        print(f'COMMANDS: {len(self.commands)}')
        if sort:
            commands = sorted(self.commands, key=lambda x: (x.q_in, x.l_in))
        else:
            commands = self.commands
        for com in commands:
            print(com)

    def run(self, s: str, verbose=False) -> str:
        is_turing_str(s)
        if verbose:
            print(f'Input: [{s}]')
        line = list(s) + [' '] * 100
        q = 0
        i = 0
        while True:
            for com in self.commands:
                if q == Q_END:
                    while line[-1] == ' ' and line[-2] == ' ':
                        line = line[:-1]
                    result = "".join(line)
                    if verbose:
                        print(f'Output: [{result}]')
                    return result
                if com.q_in == q and com.l_in == line[i]:
                    if verbose:
                        print(com)
                    q = com.q_out
                    line[i] = com.l_out
                    if com.dir == R:
                        i += 1
                    else:
                        i -= 1
                    break
            else:
                raise Exception('Нет команд для выполнения!')

    def is_behave_func(self, func: Callable[[str], str], l_max=10):

        for l in range(l_max):
            for word in combinations_with_replacement('ab', l):
                s = '*' + ''.join(word) + ' '
                if self.run(s) != func(s):
                    print(f'Error on {s}')
                    return False
        return True


def main():
    tm = TuringMachine()
    tm.add((0, ' ', -1, '#', L))
    tm.add((0, 'a', 1, 'a', R))  # *a
    tm.add((0, 'b', 2, 'b', R))  # *b

    tm.add((1, 'a', 1, 'a', R))  # a...a
    tm.add((1, 'b', 2, 'b', R))  # a...ab

    tm.add((2, 'a', 2, 'a', R))  # идем до конца после b
    tm.add((2, 'b', 2, 'b', R))  #

    tm.add((1, ' ', 3, ' ', L))  # успешно - стираем
    tm.add((2, ' ', 4, ' ', L))  # неуспех - стираем
    for i in (3, 4):
        for l in ('a', 'b'):
            tm.add((i, l, i, ' ', L))
    tm.add((3, '*', 5, '*', R))
    tm.add((5, ' ', Q_END, '1', R))
    tm.add((4, '*', 6, '*', R))
    tm.add((6, ' ', Q_END, '0', R))

    tm.print()

    # print(tm.is_behave_func(is_all_a))


if __name__ == "__main__":
    main()
