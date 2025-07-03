from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.numpad import NumPad

from utils.debug import error_handler


@error_handler()
def on_submit(parent: NumPad) -> None:
    """Retrieve NumPad entry, save entry to result state, and closes window"""
    parent.result = parent.widgets["label_entry"].entry.get()
    parent.destroy()
