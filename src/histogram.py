from dataclasses import dataclass
from typing import List, Optional

import numpy as np


@dataclass(frozen=True)
class Rectangle:
    height: int
    pos: int

    def calculate_bottom(self, pos: int, cum_d: np.ndarray) -> int:
        """Calculate the length of the bottom edge of the rectangle.

        Args:
            pos (np.ndarray): The position of the rectangle.
            cum_d (np.ndarray): The cumulative delta array.

        Returns:
            int: The length of the bottom edge of the rectangle.
        """
        return cum_d[pos + 1] - cum_d[self.pos]

    def calculate_area(self, pos: int, cum_d: np.ndarray) -> int:
        """Calculate the area of a rectangle with the given position, height, and cumulative delta.

        Args:
            pos (int): The position of the rectangle.
            cum_d (np.ndarray): The cumulative delta array.

        Returns:
            int: The area of the rectangle.
        """
        bottom = self.calculate_bottom(pos, cum_d)
        return self.height * bottom


class Histogram:
    def __init__(self, values: np.ndarray, d: Optional[np.ndarray] = None):
        """Initializes a histogram object.

        Args:
            values (np.ndarray): The height array of the histogram.
            d (Optional[np.ndarray]): The delta array of the histogram.
        """
        if d is None:
            d = np.ones_like(values, dtype=np.int64)

        self._check_len(values, d)
        self.values = np.append(values, 0)
        self.d = np.append(d, 0)

        # cumsum, used to calculate the length of the bottom edge.
        cum_d = np.cumsum(self.d)
        self.cum_d = np.insert(cum_d, 0, 0)

    def calculate_max_area(self) -> int:
        """Calculate the maximum area of the rectangle that can be created in the histogram with the given height and delta-y arrays. [1]

        Returns:
            int: The maximum area of the histogram.

        Note:
            [1]: http://algorithms.blog55.fc2.com/blog-entry-132.html
        """
        max_area = 0
        stack: List[Rectangle] = []

        for pos, height in enumerate(self.values):
            rect = Rectangle(height, pos)
            if len(stack) == 0:
                stack.append(rect)
            else:
                if stack[-1].height < rect.height:
                    stack.append(rect)

                elif stack[-1].height > rect.height:
                    target = pos
                    while len(stack) > 0 and stack[-1].height >= rect.height:
                        prev_rect = stack.pop()
                        area = prev_rect.calculate_area(pos, self.cum_d)
                        max_area = max(max_area, area)
                        target = prev_rect.pos

                    new_rect = Rectangle(height, target)
                    stack.append(new_rect)

        return max_area

    def set_values(self, values):
        """Sets the values of the histogram.

        Args:
            values (np.ndarray): The values of the histogram.
        """
        values = np.append(values, 0)
        self._check_len(values, self.d)
        self.values = values

    def _check_len(self, values, d):
        """Checks the length of the values and d arrays.

        Args:
            values (np.ndarray): The values of the histogram.
            d (np.ndarray): The delta array of the histogram.
        """
        assert len(values) == len(
            d
        ), f"The length of values and d must be the same. length of values={len(values)}, length of d={len(d)}"
