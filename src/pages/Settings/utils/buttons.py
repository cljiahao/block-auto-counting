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
    """Main Function for Slider Buttons"""
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
    """Fetch existing HSV ranges and update Slider-Entry"""
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
    """Add new HSV ranges from Slider-Entry to holder"""
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

        # Set value to holder
        root.set_holder[col][mat] = ll_ul

        # Refresh Colour Container
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
    """Reset HSV ranges from Slider-Entry to default"""
    for i, txt in enumerate(root.entry_hsv.keys()):
        # Algo for 0 or 255 on Scale / Slider
        limit = 0 if i % 2 == 0 else 255
        root.entry_hsv[txt].delete(0, END)
        root.entry_hsv[txt].insert(0, limit)


def new(root, frame_colors):
    """To open NewColor Window to add new or update HSV ranges from Slider-Entry, defect modes and accuracy"""
    ll_ul = {"LL": [], "UL": []}
    for txt, widget in root.entry_hsv.items():
        if "Low" in txt:
            ll_ul["LL"].append(widget.get())
        else:
            ll_ul["UL"].append(widget.get())

    for i in ll_ul.copy():
        ll_ul[i] = ",".join(ll_ul[i])

    # Refresh Colour Container
    if NewColor(root, ll_ul).res:
        for widget in frame_colors.winfo_children():
            widget.destroy()
        color_container(frame_colors, root)


def save(root):
    """Save and write to json for Settings, Colors and Accuracy"""
    # Write to Color Json File
    data_col = {"Colors": root.set_holder}
    write_json("core/json/colors.json", data_col)

    # Write to Settings Json File
    for k, v in root.tab_boxes.items():
        # TODO: Find a way to save the information in Accuracy tab_box
        if "Accuracy" in k:
            continue
        value = v.get()
        save_set(root.set_set, k.split("_"), value)
    data_set = {"Settings": root.set_set}
    write_json("core/json/settings.json", data_set)

    # Write to Static Names Json File
    data_names = {"Names": root.set_names}
    write_json("core/json/staticnames.json", data_names)

    root.res = True
    root.light.light_switch()
    root.cap.release()
    root.destroy()
    root.quit()
    messagebox.showinfo(title="Settings saved", message="Settings saved")


def staticnames(root):
    """To open StaticNames window to show defect name per colour"""
    StaticNames(root)


def save_set(dict_set, key, value):
    """Main Function to save settings"""
    if isinstance(dict_set[key[0]], dict):
        save_set(dict_set[key[0]], key[1:], value)
    else:
        dict_set[key[0]] = value


def no_change(root):
    """Main Function to cancel and not save"""
    root.res = False
    root.light.light_switch()
    root.cap.release()
    root.destroy()
    root.quit()
    messagebox.showinfo(title="No changes were made", message="No changes were made")
