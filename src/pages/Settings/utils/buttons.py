from tkinter import messagebox
from tkinter import END
from components.NewColor.NewColor import NewColor
from components.StaticNames.StaticNames import StaticNames

from pages.Settings.components.colors import color_container
from utils.read_write import write_json


def button_diff(
    root,
    name,
    col,
    mat,
    frame_drop_but,
    frame_colors,
):
    if name == "Fetch":
        fetch(root, col, mat, frame_drop_but)
    elif name == "Add":
        add(
            root,
            col,
            mat,
            frame_drop_but,
            frame_colors,
        )
    elif name == "Reset":
        reset(root)
    elif name == "New":
        new(root, frame_colors)


def fetch(root, col, mat, frame_drop_but):
    arr = ["", "", "", "", "", ""]
    if col in root.set_holder and mat in root.set_holder[col]:
        for key, value in root.set_holder[col][mat].items():
            for i, val in enumerate(value.split(",")):
                if key == "LL":
                    arr[i * 2] = val
                else:
                    arr[(i + 1) * 2 - 1] = val
        for j, entry in enumerate(root.entry_hsv.values()):
            entry.delete(0, END)
            entry.insert(0, arr[j])
    else:
        messagebox.showerror(
            title="Option not selected",
            message=f"Please Select an Option",
            parent=frame_drop_but,
        )


def add(root, col, mat, frame_drop_but, frame_colors):
    # Color Container
    if col in root.set_holder and mat in root.set_holder[col]:
        ll_ul = {"LL": [], "UL": []}
        for txt, widget in root.entry_hsv.items():
            if "Low" in txt:
                ll_ul["LL"].append(widget.get())
            else:
                ll_ul["UL"].append(widget.get())

        for i in ll_ul.copy():
            ll_ul[i] = ",".join(ll_ul[i])

        root.set_holder[col][mat] = ll_ul

        for widget in frame_colors.winfo_children():
            widget.destroy()

        color_container(frame_colors, root)
    else:
        messagebox.showerror(
            title="Option not selected",
            message=f"Please Select an Option",
            parent=frame_drop_but,
        )


def reset(root):
    for i, txt in enumerate(root.entry_hsv.keys()):
        # Algo for 0 or 255 on Scale / Slider
        limit = 0 if i % 2 == 0 else 255
        root.entry_hsv[txt].delete(0, END)
        root.entry_hsv[txt].insert(0, limit)


def new(root, frame_colors):
    ll_ul = {"LL": [], "UL": []}
    for txt, widget in root.entry_hsv.items():
        if "Low" in txt:
            ll_ul["LL"].append(widget.get())
        else:
            ll_ul["UL"].append(widget.get())

    for i in ll_ul.copy():
        ll_ul[i] = ",".join(ll_ul[i])

    if NewColor(root, ll_ul).res:
        for widget in frame_colors.winfo_children():
            widget.destroy()

        color_container(frame_colors, root)


def save(root):
    # Write to Color Json File
    data_col = {"Colors": root.set_holder}
    write_json("json/colors.json", data_col)
    # Write to Settings Json File
    for k, v in root.tab_boxes.items():
        value = v.get()
        save_set(root.set_set, k.split("_"), value)
    data_set = {"Settings": root.set_set}
    write_json("json/settings.json", data_set)
    # Write to Static Names Json File
    root.res = True
    root.light.light_switch()
    root.cap.release()
    root.destroy()
    root.quit()
    messagebox.showinfo(title="Settings saved", message="Settings saved")


def staticnames(root):
    StaticNames()


def save_set(dict_set, key, value):
    if isinstance(dict_set[key[0]], dict):
        save_set(dict_set[key[0]], key[1:], value)
    else:
        dict_set[key[0]] = value


def no_change(root):
    root.res = False
    root.light.light_switch()
    root.cap.release()
    root.destroy()
    root.quit()
    messagebox.showinfo(title="No changes were made", message="No changes were made")
