from typing import Tuple, List

from turing_machine import TuringMachine, L, R
from turing_machine import is_all_a
from itertools import combinations_with_replacement


def get_all_turing_elem_right(n, v='ab'):
    rights: List[Tuple] = []
    for q_out in range(-1, n):
        for l_out in v:
            for d in L, R:
                rights.append((q_out, l_out, d))
    return rights


def create_turing_by_func(func, v='ab') -> TuringMachine:
    n = 5

    rights = get_all_turing_elem_right(n)
    # print(rights)
    combs = combinations_with_replacement(rights, n * len(v) + 2)
    for comb in combs:
        tm = TuringMachine()
        # print(comb)
        # for com in comb:
        #     tm.add(com)
        # if tm.is_behave_func(func):
        #     print('Yay')
        #     return tm
    print(':(')


def main():
    create_turing_by_func(is_all_a)


if __name__ == "__main__":
    main()
