from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Config:
    """Configuration object.

    Args:
        r (int): Vertical length of plane.
        c (int): Horizontal length of plane.
        x1 (np.ndarray): The x-coordinates of the start points of the lines.
        y1 (np.ndarray): The y-coordinates of the start points of the lines.
        x2 (np.ndarray): The x-coordinates of the end points of the lines.
        y2 (np.ndarray): The y-coordinates of the end points of the lines.
    """

    r: int
    c: int
    x1: np.ndarray
    y1: np.ndarray
    x2: np.ndarray
    y2: np.ndarray
