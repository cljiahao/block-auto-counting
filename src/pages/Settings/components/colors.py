from tkinter import Label
from tkinter import E, W

from pages.Settings.components.scroll_cont import scroll_cont


def color_container(frame_colors, root):
    font = root.set_names["Font"]["S"]
    frame_canvas_colors = scroll_cont(frame_colors, "6c")

    # Color Header
    Label(frame_canvas_colors, text="Colors", font=font).grid(
        row=0, column=0, padx=5, pady=5
    )
    # LL Header
    Label(frame_canvas_colors, text="LL", font=font).grid(
        row=0, column=1, padx=5, pady=5
    )
    # UL Header
    Label(frame_canvas_colors, text="LL", font=font).grid(
        row=0, column=2, padx=5, pady=5
    )

    i = 1
    for col, value in root.set_holder.items():
        # Color Label
        Label(frame_canvas_colors, text=col, font=font).grid(
            row=i, column=0, padx=5, pady=5, sticky=W
        )
        i += 1
        for mat, val in value.items():
            # Material Label
            Label(frame_canvas_colors, text=mat, font=font).grid(
                row=i, column=0, padx=5, pady=5, sticky=E
            )
            for j, k in enumerate(val.keys()):
                # LL and UL Values
                hsv_val = Label(frame_canvas_colors, text=val[k], font=font)
                if col not in root.set_colors:
                    hsv_val.config(bg="#93D976")
                elif mat not in root.set_colors[col]:
                    hsv_val.config(bg="#FFFF80")
                elif val[k] != root.set_colors[col][mat][k]:
                    hsv_val.config(bg="#fa6464")
                hsv_val.grid(row=i, column=j + 1, padx=5, pady=5)

            i += 1
