import numpy as np

from src.config_interface import Config
from src.plane import CompressedPlane


def parse_input() -> Config:
    """Parses input and returns required parameters.

    Returns:
        Config: The configuration object.
    """
    R, C = map(int, input().split())
    N = int(input())
    lines = np.array(
        [list(map(int, input().split())) for _ in range(N)], dtype=np.int64
    )
    X1, Y1, X2, Y2 = lines.T
    cfg = Config(R, C, X1, Y1, X2, Y2)

    return cfg


def solve(cfg) -> int:
    """This function calculates the maximum area of a rectangle that can be formed in a 2D plane. It performs two steps to achieve this:

    1. It uses coordinate compression [1] to efficiently process the input data.
    2. It applies the maximum area algorithm [2] to find the largest rectangle that can be formed within a histogram.

    Args:
        cfg (Config): The configuration object.

    Returns:
    int: The maximum area of a rectangle that can be formed within the plane.

    Note:
        [1] https://algo-logic.info/coordinate-compress/
        [2] http://algorithms.blog55.fc2.com/blog-entry-133.html
    """
    # 1. Coordinate compression
    cp = CompressedPlane(cfg)

    # 1.1. Compute the histogram of the compressed plane
    cp.compute_hists()

    # 2. Using an algorithm that searches for the largest rectangle that can be made in the histogram,
    # the area of the largest rectangle that can be made in the plane is used.
    ans = cp.calculate_max_area()

    return ans


if __name__ == "__main__":
    cfg = parse_input()
    ans = solve(cfg)
    print(ans)
