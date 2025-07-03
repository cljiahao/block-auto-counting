from dataclasses import dataclass
from enum import Enum


class BGRColors(Enum):
    """Enum for BGR color values."""

    BACKGROUND = (192, 192, 192)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    CYAN = (255, 255, 0)
    GREEN = (0, 255, 0)
    LIME = (0, 255, 192)
    ORANGE = (0, 191, 255)
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)


@dataclass(frozen=True)
class ColorInfo:
    """Dataclass for color information."""

    name: str
    bgr: tuple[int, int, int]


class CSAMcolor(Enum):
    """Enum for CSAM colors."""

    BLACK = ColorInfo(name="Black", bgr=BGRColors.BLACK.value)
    BLUE = ColorInfo(name="Blue", bgr=BGRColors.BLUE.value)
    CYAN = ColorInfo(name="Cyan", bgr=BGRColors.CYAN.value)
    GREEN = ColorInfo(name="Green", bgr=BGRColors.GREEN.value)
    LIME = ColorInfo(name="Lime", bgr=BGRColors.LIME.value)
    ORANGE = ColorInfo(name="Orange", bgr=BGRColors.ORANGE.value)
    YELLOW = ColorInfo(name="Yellow", bgr=BGRColors.YELLOW.value)

    def get_name(self) -> str:
        """Returns the BGR name value for the CSAM color."""
        return self.value.name

    def get_bgr(self) -> tuple[int, int, int]:
        """Returns the BGR color value for the CSAM color."""
        return self.value.bgr
