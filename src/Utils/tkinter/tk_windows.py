from tkinter import Tk, Toplevel


def window_size(root: Toplevel) -> dict[str, int | float]:
    """Returns the screen dimensions and aspect ratio of the root window"""

    win_size = {
        "w_screen": root.winfo_screenwidth(),
        "h_screen": root.winfo_screenheight(),
        "aspect": root.winfo_screenwidth() / root.winfo_screenheight(),
    }
    return win_size


def destroy_children(parent: Tk | Toplevel) -> None:
    for widget in parent.winfo_children():
        widget.destroy()


def terminate(root: Tk | Toplevel) -> None:
    """Terminates the Tkinter window"""

    root.destroy()
    root.quit()
