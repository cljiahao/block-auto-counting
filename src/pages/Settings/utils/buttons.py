from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings import Settings

from utils.debug import error_handler


@error_handler()
def on_return(parent: Settings):
    """Closes window upon button click"""
    parent.result = True
    parent.destroy()


buttons_map = {
    "return": on_return,
}
