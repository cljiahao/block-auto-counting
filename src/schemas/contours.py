import numpy as np
from cv2.typing import RotatedRect
from dataclasses import dataclass
from typing import Iterator

from core.logging import logger


@dataclass
class ContourInfo:
    contour: np.ndarray
    rect: RotatedRect
    area: float


@dataclass
class ContourInfoList:
    contours: list[ContourInfo]

    def __len__(self) -> int:
        return len(self.contours)

    def __iter__(self) -> Iterator[ContourInfo]:
        return iter(self.contours)

    def get_median_area(self) -> float:
        """Calculate the median area of the contours in the list."""
        if not self.contours:
            raise ValueError("No contours available to calculate median area.")
        contour_areas = np.array([contour_info.area for contour_info in self.contours])
        average_area = np.median(contour_areas)
        logger.info(f"Average Chip Area is {average_area}")

        return average_area

    def get_average_length(self) -> float:
        """Calculate the average length of the contours in the list."""
        if not self.contours:
            raise ValueError("No contours available to calculate average length.")
        longest_side_value = np.array(
            [max(contour_info.rect[1]) for contour_info in self.contours]
        )
        average_length = np.median(longest_side_value)
        logger.info(f"Average Chip Length found is {average_length}")

        return average_length
