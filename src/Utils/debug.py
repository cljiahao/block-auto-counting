import cv2
import numpy as np
import time
from datetime import timedelta
from typing import Callable

from core.logging import logger


def cvWin(image: np.ndarray, name: str = "image") -> None:
    """Display an image using OpenCV for debugging purposes.

    Args:
        image: The image to be displayed.
        name: The name of the window. Defaults to "image".
    """
    cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
    cv2.imshow(name, image)
    if cv2.waitKey(0) & 0xFF == ord("q"):
        cv2.destroyAllWindows()


def timer(print_message: str = "") -> Callable:
    """A decorator to log the time taken by a function.

    Args:
        print_message: An optional custom message to be logged along with the elapsed time.

    Returns:
        A decorator that takes a callable and returns a wrapped callable that logs its execution time.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: any, **kwargs: any) -> any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = timedelta(seconds=end_time - start_time)
            formatted_time = str(elapsed_time).split(".")[0]
            if print_message:
                logger.info(f"{print_message} took: {formatted_time}", stacklevel=2)
            else:
                logger.info(f"Total time taken: {formatted_time}", stacklevel=2)
            return result

        return wrapper

    return decorator


def error_handler() -> Callable:
    """A decorator to log exceptions that occur during the execution of a function.

    Returns:
        A decorator that takes a callable and returns a wrapped callable that logs any exceptions raised.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: any, **kwargs: any) -> any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"{type(e).__name__} occurred: {e}",
                    exc_info=True,
                    stacklevel=2,
                )
                raise

        return wrapper

    return decorator
