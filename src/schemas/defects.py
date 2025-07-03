import numpy as np
from dataclasses import dataclass
from typing import Iterator


@dataclass
class ColorInfo:
    color_name: str
    is_tape: bool


@dataclass
class NPColorSpec(ColorInfo):
    lower_limit: np.ndarray
    upper_limit: np.ndarray


@dataclass
class DefectsInfo(ColorInfo):
    contour: np.ndarray
    mm_area: float


@dataclass
class DefectsInfoList:
    image: np.ndarray
    defects: list[DefectsInfo]

    def __len__(self) -> int:
        return len(self.defects)

    def __iter__(self) -> Iterator[DefectsInfo]:
        return iter(self.defects)
