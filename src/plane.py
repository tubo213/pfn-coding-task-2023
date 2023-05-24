from typing import Tuple

import numpy as np

from src.config_interface import Config
from src.histogram import Histogram


class CompressedPlane:
    def __init__(
        self,
        cfg: Config,
    ):
        """Initializes a compressed plane object.

        Args:
            cfg (Config): The configuration object.
        """
        self.cfg = cfg
        x1, y1, x2, y2 = self._set_side_line(cfg)
        self._compress(x1, y1, x2, y2)

    def calculate_max_area(self) -> int:
        """Calculates the maximum area of a rectangle that can be formed in a 2D plane.

        Returns:
            int: The maximum area of a rectangle that can be formed within the plane.
        """
        assert self.hists is not None, "Please run compute_hists() first."

        max_area = 0
        h = Histogram(self.hists[0], self.dy)
        for hist_i in self.hists[1::2]:
            h.set_values(hist_i)
            area = h.calculate_max_area()
            max_area = max(max_area, area)

        return max_area

    def compute_hists(self):
        """Compute the length that can be extended up for each element in the plane.

        Note:
            This method should be called before calculate_max_area().
        """
        hists = self.values.copy()

        for i in range(1, self.h * 2 - 1):
            for j in range(self.w * 2 - 1):
                if self.values[i, j] == -1:
                    continue
                elif self.values[i - 1, j] == -1:
                    hists[i, j] = self.dx[i]
                else:
                    hists[i, j] = hists[i - 1, j] + self.dx[i]

        self.hists = hists

    def _set_side_line(
        self,
        cfg: Config,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Sets the side lines of the plane.

        Args:
            cfg (Config): The configuration object.

        Returns:
        - A tuple of the modified x1, y1, x2, and y2 arrays.
        """
        x1 = np.concatenate([cfg.x1, [0, 0, 0, cfg.r]])
        y1 = np.concatenate([cfg.y1, [0, cfg.c, 0, 0]])
        x2 = np.concatenate([cfg.x2, [cfg.r, cfg.r, 0, cfg.r]])
        y2 = np.concatenate([cfg.y2, [0, cfg.c, cfg.c, cfg.c]])

        return x1, y1, x2, y2

    def _compress(self, x1: np.ndarray, y1: np.ndarray, x2: np.ndarray, y2: np.ndarray):
        """Compress the coordinates.
        The plane is represented by an array of squares with even rows and even columns representing points,
        and odd rows and odd columns representing cells.
        For simplicity, the width of a point is assumed to be zero.

        Args:
            x1 (np.ndarray): The x-coordinates of the start points of the lines.
            y1 (np.ndarray): The y-coordinates of the start points of the lines.
            x2 (np.ndarray): The x-coordinates of the end points of the lines.
            y2 (np.ndarray): The y-coordinates of the end points of the lines.
        """
        # compress coordinates
        self.x = np.unique(np.concatenate([x1, x2]))
        self.y = np.unique(np.concatenate([y1, y2]))
        self.x1 = np.searchsorted(self.x, x1)
        self.x2 = np.searchsorted(self.x, x2)
        self.y1 = np.searchsorted(self.y, y1)
        self.y2 = np.searchsorted(self.y, y2)

        # initialize plane
        self.h = len(self.x)
        self.w = len(self.y)
        self.values = np.zeros(
            (self.h * 2 - 1, self.w * 2 - 1), dtype=np.int64
        )  # even rows and even columns are points, odd rows and odd columns are cells

        # set width of points and cells
        cell_dx = (self.x[1:] - self.x[:-1]).reshape(-1, 1)
        cell_dy = (self.y[1:] - self.y[:-1]).reshape(-1, 1)
        # assume the width of a point is zero
        line_dx = np.zeros_like(cell_dx, dtype=np.int64)
        line_dy = np.zeros_like(cell_dy, dtype=np.int64)
        dx = np.concatenate([line_dx, cell_dx], axis=1).flatten()
        dy = np.concatenate([line_dy, cell_dy], axis=1).flatten()
        self.dx = np.append(dx, 0)
        self.dy = np.append(dy, 0)

        # set the line in the compressed plane by marking the corresponding values as -1.
        for x1_i, y1_i, x2_i, y2_i in zip(
            self.x1 * 2, self.y1 * 2, self.x2 * 2, self.y2 * 2
        ):
            self.values[x1_i : x2_i + 1, y1_i : y2_i + 1] = -1
