import numpy as np

from main import solve
from src.config_interface import Config


def parse_input_str(input_str):
    lines = input_str.splitlines()
    r, c = map(int, lines[0].split())
    x1, y1, x2, y2 = [], [], [], []
    for line in lines[2:]:
        x1_, y1_, x2_, y2_ = map(int, line.split())
        x1.append(x1_)
        y1.append(y1_)
        x2.append(x2_)
        y2.append(y2_)
    return Config(
        r=r,
        c=c,
        x1=np.array(x1),
        y1=np.array(y1),
        x2=np.array(x2),
        y2=np.array(y2),
    )


def test_sample_1():
    cfg = parse_input_str(
        """3 5
3
1 0 1 2
0 1 2 1
2 3 2 5"""
    )
    assert solve(cfg) == 6


def test_sample_2():
    cfg = parse_input_str(
        """4 4
4
1 0 1 2
0 3 2 3
2 1 4 1
3 2 3 4"""
    )
    assert solve(cfg) == 4


def test_sample_3():
    cfg = parse_input_str(
        """1000000000 1000000000
1
0 0 0 1000000000
"""
    )
    assert solve(cfg) == 1000000000000000000
