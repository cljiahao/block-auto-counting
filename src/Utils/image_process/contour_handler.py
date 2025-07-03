import cv2
import numpy as np

from core.logging import logger
from schemas.contours import ContourInfo, ContourInfoList
from utils.debug import error_handler


class ContourHandler:
    """A utility class for processing and analyzing image contours."""

    @error_handler()
    @staticmethod
    def get_median_area(contours: list[np.ndarray]) -> float:
        """Calculate the median area of the contours in the list.

        Args:
            contours: A list of NumPy arrays representing contours.

        Returns:
            The median area of the contours.

        Raises:
            ValueError: If the input list is empty.
        """
        if not contours:
            raise ValueError("No contours available to calculate median area.")
        contour_areas = np.array([cv2.contourArea(contour) for contour in contours])
        average_area = np.median(contour_areas)
        logger.debug(f"Average Chip Area is {average_area}")

        return average_area

    @error_handler()
    @staticmethod
    def filter_and_build_contour_info(
        contours: list[np.ndarray],
        denoise_threshold: int = 0,
    ) -> ContourInfoList:
        """Filters contours based on area and builds a ContourInfoList.

        Args:
            contours: A list of NumPy arrays representing contours.
            denoise_threshold: The minimum area for a contour to be included.

        Returns:
            A ContourInfoList object containing filtered ContourInfo objects.
        """
        clean_contours = [
            ContourInfo(
                contour=contour,
                rect=cv2.minAreaRect(contour),
                area=blob_area,
            )
            for contour in contours
            if (blob_area := cv2.contourArea(contour)) > denoise_threshold
        ]

        logger.debug(
            f"Filtered {len(clean_contours)} contours based on area threshold.",
            stacklevel=2,
        )

        return ContourInfoList(contours=clean_contours)

    @error_handler()
    @staticmethod
    def rotate_contour_upright(contours: ContourInfoList):
        """Rotate contours upright based on width and height.

        Args:
            contours: A list of NumPy arrays representing contours or ContourInfoList.

        Returns:
            A ContourInfoList object containing filtered ContourInfo objects.
        """
        processed_contours = []
        for contour_info in contours:
            center, (width, height), angle = contour_info.rect
            if height < width:
                contour_info.rect = (center, (height, width), angle - 90)
            processed_contours.append(contour_info)

        return ContourInfoList(contours=processed_contours)
