from typing import List, Tuple, Callable, Dict, Any
from itertools import combinations_with_replacement, product


def is_all_a(s: str):
    is_turing_str(s)
    s = s[1:-1]
    if len(s) == 0:
        return "*# "
    if set(s) == {'a'}:
        return "*1 "
    return "*0 "


def is_length_more_k(s: str, k):
    is_turing_str(s)
    s = s[1:-1]
    if len(s) > k:
        return '*' + s[:k] + '$' + s[k:] + ' '
    return '*' + s + ' '


class TuringElem:

    def __init__(self, q_in, l_in, q_out, l_out, dir, label=''):
        self.q_in = q_in
        self.l_in = l_in
        self.q_out = q_out
        self.l_out = l_out
        self.dir = dir
        self.label = label

    def __repr__(self):
        return f'(q{self.q_in}, {self.l_in}) -> (q{self.q_out}, {self.l_out}, {self.dir})'


def is_turing_str(s: str):
    if s[0] != '*':
        raise Exception("Дорожка должна начинаться на *")
    if s[-1] != ' ':
        raise Exception("Дорожка должна заканчиваться пробелом")


turing_stats = dict[TuringElem, int]

R = 'R'
L = 'L'
Q_END = 'f'


class TuringMachine:
    def __init__(self, lang):
        self.commands: List[TuringElem] = []
        self.lang = lang

    def add(self, elem: TuringElem | Tuple[int | str, str, int | str, str, str] |
                        Tuple[int | str, str, int | str, str, str, str]):
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

    def run(self, s: str, verbose=False, _stats: turing_stats = None) -> str:

        def now_state() -> str:
            line_output = "".join(line).rstrip()

            left = line_output[:i]
            if not left:
                left = 'λ'
            right = line_output[i:] + '☐'

            return f'(q{q}, {left}, {right})'

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
                        print(now_state())
                        print(f'Output: [{result}]')
                    return result
                if com.q_in == q and com.l_in == line[i]:
                    if _stats is not None:
                        _stats[com] += 1
                    if verbose:
                        # print(com)
                        print(now_state(), '->', f'({com.label})')

                    q = com.q_out
                    line[i] = com.l_out
                    if com.dir == R:
                        i += 1
                    else:
                        i -= 1
                    break
            else:
                raise Exception(f'Нет команд для выполнения! Сейчас: ({q}, {line[i]})')

    def is_behave_func(self, func: Callable[[str], str], l_max=10):
        stats: turing_stats = {}
        for com in self.commands:
            stats[com] = 0
        for l in range(l_max + 1):
            for word in product(self.lang, repeat=l):
                s = '*' + ''.join(word) + ' '
                try:
                    if self.run(s, _stats=stats) != func(s):
                        print(f'Вывод не совпадает на {s}')
                        return False
                except Exception as ex:
                    print(f'Вызвана ошибка {ex} на {s}')
                    return False

        for key, value in stats.items():
            print(f'{key}: {value}')
        return True


def tm_all_a() -> TuringMachine:
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

    return tm


def tm_length_more(k, v='ab'):
    tm = TuringMachine(v)
    for i in range(0, k):
        for a in v:
            tm.add((i, a, i + 1, a, R, '3'))

    tm.add((0, ' ', Q_END, ' ', L, '2'))

    for i in range(1, k + 1):
        tm.add((i, ' ', 'back', ' ', L, '4'))

    for a in v:
        tm.add(('back', a, 'back', a, L, '5'))

    tm.add(('back', '$', 'back', '$', L, '6'))

    for a in v:
        tm.add((k, a, f'{k}{a}', '$', R, '7'))

    for a in v:
        for b in v:
            tm.add((f'{k}{a}', b, f'{k}{b}', a, R, '8'))

    for a in v:
        tm.add((f'{k}{a}', ' ', 'back', a, L, '9'))

    tm.add(('back', '*', 'pf', '*', R, '10'))

    for a in v:
        tm.add(('pf', a, Q_END, a, R, '11'))

    return tm


def main():
    k = 3
    tm = tm_length_more(k, 'abc')
    tm.run("*abcabc ", verbose=True)

    # print(tm.is_behave_func(lambda s: is_length_more_k(s, k)))


if __name__ == "__main__":
    main()
