import cv2
import numpy as np

from constants.colors import BGRColors
from core.logging import logger
from utils.debug import error_handler


class BlobHandler:
    """A utility class for processing blobs (regions of interest) found from contours in images."""

    @error_handler()
    @staticmethod
    def create_kernel(kernel_size: int) -> np.ndarray:
        """Creates a square kernel of ones for morphological operations.

        Args:
            kernel_size: The size (width and height) of the square kernel.

        Returns:
            A NumPy ndarray representing the square kernel with uint8 data type.
        """
        return np.ones((kernel_size, kernel_size), dtype=np.uint8)

    @error_handler()
    @staticmethod
    def crop_roi(
        image: np.ndarray,
        x_center: float,
        y_center: float,
        padding: int | tuple[int, int],
    ) -> np.ndarray:
        """Crops a region of interest (ROI) from the given image.

        Args:
            image: The input image.
            x_center: The x-coordinate of the center of the ROI.
            y_center: The y-coordinate of the center of the ROI.
            padding: The padding around the center for the ROI.
                - if an integer is provided: same padding on all 4 sides.
                - if an two-element integer tuple is provided: padding applied to x and y respective.

        Returns:
            The cropped ROI.
        """
        if isinstance(padding, tuple):
            x_padding, y_padding = padding
        else:
            y_padding = x_padding = padding

        y_min = int(max(0, y_center - y_padding))
        y_max = int(min(image.shape[0], y_center + y_padding))
        x_min = int(max(0, x_center - x_padding))
        x_max = int(min(image.shape[1], x_center + x_padding))

        return image[y_min:y_max, x_min:x_max]

    @error_handler()
    @staticmethod
    def draw_blob_mask_from_contour(
        image: np.ndarray, contour: np.ndarray
    ) -> np.ndarray:
        """Draws a white filled mask on a black background based on the given contours.

        Args:
            image: The input image (used for shape).
            contours: A single contour to draw mask.

        Returns:
            A binary mask with the drawn contours filled with white.
        """
        blank_mask = np.zeros(image.shape[:2], np.uint8)
        cv2.drawContours(
            blank_mask,
            [contour],
            -1,
            BGRColors.WHITE.value,
            -1,
        )
        return blank_mask

    @error_handler()
    @staticmethod
    def draw_border_and_add_center_text(
        image: np.ndarray, contour: np.ndarray, text: str
    ) -> np.ndarray:
        """
        Draws a border around contours and adds text at their approximate center.

        Args:
            image: The input image to draw on (modified in place).
            contours: A single contour to draw border.
            text: The text string to be placed at the center of the contour's minimum area rectangle.

        Returns:
            The modified image with borders drawn and text added.
        """
        cv2.drawContours(image, [contour], -1, BGRColors.WHITE.value, 1)

        ((x_center, y_center), _, _) = cv2.minAreaRect(contour)
        origin = (int(x_center - 10), int(y_center))
        cv2.putText(
            image,
            str(text),
            origin,
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            BGRColors.YELLOW.value,
            1,
        )
        return image

    @error_handler()
    @staticmethod
    def create_mask_by_mean_color(
        image: np.ndarray, mask: np.ndarray, limit_range: int | float
    ) -> np.ndarray:
        """
        Creates a binary mask based on the mean color within a masked region of an image.

        Args:
            image: Input BGR image (H, W, 3).
            mask: Binary mask (H, W) or (H, W, 1) defining the region of interest.
            limit_range: Percentage (0-1.0 or 0-100) to extend color limits.

        Returns:
            New binary mask (H, W) based on the calculated color range.
        """
        if limit_range < 0:
            raise ValueError("Limit range cannot be negative number.")

        percentage_range = limit_range / 100.0 if 1 < limit_range else limit_range

        mean_bgr = cv2.mean(image, mask=mask)[:3]
        mean_bgr_np = np.array(mean_bgr, dtype=np.uint16)

        lower_limit = np.clip(mean_bgr_np * (1 - percentage_range), 0, 255).astype(
            np.uint8
        )
        upper_limit = np.clip(mean_bgr_np * (1 + percentage_range), 0, 255).astype(
            np.uint8
        )
        logger.debug(f"Lower Limit: {lower_limit}, Upper Limit: {upper_limit}")

        blur_image = cv2.GaussianBlur(image, (5, 5), 0)
        block = cv2.bitwise_and(blur_image, blur_image, mask=mask)

        return cv2.inRange(block, lower_limit, upper_limit)
