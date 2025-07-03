from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Accuracy import Accuracy


def on_done(parent: Accuracy) -> None:
    """Destroys the parent Accuracy component, indicating completion"""
    parent.destroy()


buttons_map = {
    "done": on_done,
}
