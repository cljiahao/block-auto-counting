import cv2
import time


def time_print(start, func_name) -> None:
    """
    Parameters
    ----------
    start : float
        Start time from previous recording
    func_name : string
        Description for previous recording
    """
    print(f"{func_name} took: {round(time.time()-start,2)} secs")

    return time.time()


def cvWin(img, name):
    """
    Parameters
    ----------
    img : MatLike
        Image to show
    name : string
        Window Name
    """
    cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
    cv2.imshow(name, img)
    cv2.waitKey(0)
