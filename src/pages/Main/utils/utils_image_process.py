import cv2
import numpy as np
from PIL import Image

from utils.image_process.blob_handler import BlobHandler


def find_calibration_pin(gray_image: np.ndarray) -> np.ndarray:
    width = gray_image.shape[0]
    blur = cv2.medianBlur(gray_image, 5)
    for i in range(20, 70, 5):
        circles = cv2.HoughCircles(
            blur, cv2.HOUGH_GRADIENT, 1, width / 16, param1=i, param2=int(i / 2)
        )
        if len(circles[0, :]) == 1:
            return np.uint16(np.around(circles[0][0]))
    raise ValueError("Unable to find Calibration pin. Please try again.")


def get_calibration_pin_area(
    gray_image: np.ndarray, center: tuple[int, int], radius: int
) -> float:
    pin_mask = np.zeros(gray_image.shape[:2], np.uint8)
    cv2.circle(pin_mask, center, radius, (255, 255, 255), -1)

    contours, _ = cv2.findContours(pin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return cv2.contourArea(contours[0])


def find_crop_block_image(image: np.ndarray, gray_image: np.ndarray) -> np.ndarray:
    blur = cv2.medianBlur(gray_image, 11)
    adapt_mask = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3
    )
    dilate = cv2.dilate(adapt_mask, BlobHandler.create_kernel(5))

    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=lambda x: cv2.contourArea(x))

    initial_block_mask = BlobHandler.draw_blob_mask_from_contour(image, largest_contour)
    open = cv2.morphologyEx(
        initial_block_mask, cv2.MORPH_OPEN, BlobHandler.create_kernel(15)
    )

    contours, _ = cv2.findContours(open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=lambda x: cv2.contourArea(x))

    ((x_center, y_center), (width, height), _) = cv2.minAreaRect(largest_contour)
    return BlobHandler.crop_roi(
        image, x_center, y_center, (width // 2 + 3, height // 2 + 3)
    )


def filter_block_mask_by_mean_color(image: np.ndarray) -> np.ndarray:
    # TODO: add limit_range in int or float?
    mean_bgr = np.uint16(cv2.mean(image)[:3])
    lower_limit = np.uint16(mean_bgr * 0.9)
    upper_limit = np.uint16(mean_bgr * 1.1)
    print(f"Lower Limit: {lower_limit}, Upper Limit: {upper_limit}")

    blur_image = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.inRange(blur_image, lower_limit, upper_limit)


def refine_block_mask(mask: np.ndarray) -> np.ndarray:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=lambda x: cv2.contourArea(x))

    rect = cv2.minAreaRect(largest_contour)
    box = np.intp(cv2.boxPoints(rect))
    min_area_rect_mask = BlobHandler.draw_blob_mask_from_contour(mask, box)
    return cv2.erode(min_area_rect_mask, np.ones((11, 11), np.uint8))


def crop_block_image(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    refined_block_image = cv2.bitwise_and(image, image, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=lambda x: cv2.contourArea(x))

    ((x_center, y_center), (width, height), theta) = cv2.minAreaRect(largest_contour)
    pre_crop_image = BlobHandler.crop_roi(
        refined_block_image, x_center, y_center, (width * 2, height * 2)
    )
    pil_image = Image.fromarray(pre_crop_image)
    rotated_image = np.asarray(pil_image.rotate(theta))

    return BlobHandler.crop_roi(rotated_image, width * 2, height * 2, (width, height))
