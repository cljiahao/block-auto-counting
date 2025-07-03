import cv2
import numpy as np
from fastapi import UploadFile
from pathlib import Path

from core.logging import logger
from core.exceptions import ImageProcessError
from utils.debug import error_handler


class ImageManager:
    """A utility class for managing image-related operations."""

    @error_handler()
    @staticmethod
    def archive_existing_file(folder_path: Path, file_name: str) -> None:
        """Archives an existing file in the specified folder by renaming it with an index.

        Args:
            folder_path: The path to the folder containing the file.
            file_name: The name of the file to archive.
        """
        files_in_dir = list(folder_path.glob("*"))
        file_path = folder_path / file_name
        if files_in_dir and file_path.exists():
            archive_name = file_path.stem + f"_{len(files_in_dir)}" + file_path.suffix
            archived_file_path = folder_path / archive_name
            file_path.rename(archived_file_path)
            logger.info(f"Archived file: {file_path} to {archived_file_path}")

    @error_handler()
    @staticmethod
    def file_to_image(file: UploadFile) -> np.ndarray:
        """Converts an uploaded file to an OpenCV image.

        Args:
            file: The uploaded file.

        Returns:
            The OpenCV image as a NumPy array.
        """
        file_content = file.file.read()
        np_image = np.frombuffer(file_content, dtype=np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        if image is None:
            raise ImageProcessError("cv2.imdecode failed to decode image data.")
        return image

    @error_handler()
    @staticmethod
    def path_to_image(path: Path) -> np.ndarray:
        """Reads an image from a file path into an OpenCV image.

        Args:
            path: The path to the image file.

        Returns:
            The OpenCV image as a NumPy array.
        """
        image = cv2.imread(str(path))
        if image is None:
            raise ImageProcessError(f"cv2.imread failed to read image from {path}")
        return image

    @error_handler()
    @staticmethod
    def save_image(file_path: str | Path, image: np.ndarray) -> None:
        """Saves a NumPy array as an image file.

        Args:
            file_path: The path to save the image file.
            image: The image as a NumPy array.
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)
        if not cv2.imwrite(file_path, image):
            raise ImageProcessError(f"cv2.imwrite failed to save image to {file_path}")
