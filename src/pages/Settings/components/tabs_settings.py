from tkinter import ttk
from tkinter import BooleanVar, OptionMenu, StringVar
from tkinter import ACTIVE, DISABLED, NS, EW

from pages.Settings.components.scroll_cont import scroll_cont


def tabs_settings(frame_tab, set_names, set_set, superuser):
    """Return Tabs Container with Settings"""
    # Create Edit container with tabs
    state = ACTIVE if superuser else DISABLED
    tab_dict = {}
    tab_boxes = {}
    tab_cont = ttk.Notebook(frame_tab)
    for key, value in set_set.items():
        # Create Tabs
        tab_dict[key] = ttk.Label(tab_cont)
        tab_cont.add(tab_dict[key], text=key)
        # For Non Nested Dict
        for i, ke in enumerate(value):
            # For Nested Dict
            if isinstance(value[ke], dict):
                tab_dict[key].columnconfigure(0, weight=1)
                # For "Accuracy" tab which is special with multi nested dicts
                if key == "Accuracy":
                    # Scrollbar container
                    frame_canvas_tab = scroll_cont(tab_dict[key])

                    acc_val = list(set_set["Accuracy"].keys())[0]
                    tab_sel_mat = StringVar(value=acc_val)
                    tab_drop_mat = OptionMenu(
                        frame_canvas_tab,
                        tab_sel_mat,
                        *set_set["Accuracy"],
                        command=lambda event: refresh(
                            frame_canvas_tab,
                            tab_boxes,
                            f"{key}_{event}",
                            set_names["Font"]["S"],
                            value[event],
                            state,
                        ),
                    )
                    tab_drop_mat.grid(row=0, column=0, padx=5, pady=5)
                    refresh(
                        frame_canvas_tab,
                        tab_boxes,
                        f"{key}_{acc_val}",
                        set_names["Font"]["S"],
                        value[acc_val],
                        state,
                    )
                else:
                    # Target Row Label
                    ttk.Label(tab_dict[key], text=ke, font=set_names["Font"]["S"]).grid(
                        row=i + 1, column=0, padx=5, pady=5
                    )
                    for j, k in enumerate(value[ke]):
                        tab_dict[key].columnconfigure(j + 1, weight=2)
                        label_input(
                            tab_dict[key],
                            tab_boxes,
                            f"{key}_{ke}_{k}",
                            set_names["Font"]["S"],
                            k,
                            value[ke][k],
                            state,
                            [0, j + 1],
                            [i + 1, j + 1, 1],
                            True,
                        )
            else:
                tab_dict[key].columnconfigure(0, weight=1)
                tab_dict[key].columnconfigure(1, weight=3)
                tab_dict[key].columnconfigure(2, weight=3)
                label_input(
                    tab_dict[key],
                    tab_boxes,
                    f"{key}_{ke}",
                    set_names["Font"]["S"],
                    ke,
                    value[ke],
                    state,
                    [i, 0],
                    [i, 1, 2],
                )

    tab_cont.grid(row=0, column=0, sticky=NS + EW)

    return tab_boxes


def label_input(
    root,
    tab_boxes,
    name,
    font,
    label,
    value,
    state,
    l_row_col,
    e_row_col,
    hasCheck=False,
):
    """Return Label-Input (Check,Radio,Entry) Widgets"""
    # Target Label
    ttk.Label(root, text=label, font=font).grid(
        row=l_row_col[0], column=l_row_col[1], padx=5, pady=5
    )
    if isinstance(value, bool):
        if hasCheck:
            tab_boxes[name] = BooleanVar(value=value)
            ttk.Checkbutton(
                root,
                text="Super",
                style="TCheckbutton",
                variable=tab_boxes[name],
                onvalue=True,
                offvalue=False,
            ).grid(row=e_row_col[0], column=e_row_col[1], padx=10, pady=5)
        else:
            tab_boxes[name] = BooleanVar(value=value)
            ttk.Radiobutton(
                root,
                text="True",
                value=1,
                variable=tab_boxes[name],
                style="Radio.TRadiobutton",
                state=state,
            ).grid(row=l_row_col[0], column=e_row_col[1], padx=10, pady=5)
            ttk.Radiobutton(
                root,
                text="False",
                value=0,
                variable=tab_boxes[name],
                style="Radio.TRadiobutton",
                state=state,
            ).grid(row=l_row_col[0], column=e_row_col[1] + 1, padx=10, pady=5)
    else:
        # Entry Box for Target
        tab_boxes[name] = ttk.Entry(root, font=font, state=state)
        tab_boxes[name].insert(0, value)
        # tab_boxes[name].config(state=DISABLED)
        tab_boxes[name].grid(
            row=e_row_col[0],
            column=e_row_col[1],
            columnspan=e_row_col[2],
            padx=10,
            pady=5,
            sticky=EW,
        )


def refresh(root, tab_boxes, name, font, value, state):
    for widget in root.winfo_children():
        if not str(widget).split("!")[-1] == "optionmenu":
            widget.destroy()
    for i, key in enumerate(value):
        if len(value[key]) < 1:
            continue
        # Target Row Label
        ttk.Label(root, text=key, font=font).grid(
            row=i + 1, column=0, padx=5, pady=5, sticky=EW
        )
        if isinstance(value[key], dict):
            for j, k in enumerate(value[key]):
                root.columnconfigure(j + 1, weight=1)
                label_input(
                    root,
                    tab_boxes,
                    f"{name}_{key}_{k}",
                    font,
                    k,
                    value[key][k],
                    state,
                    [0, j + 1],
                    [i + 1, j + 1, 1],
                )
        else:
            label_input(
                root,
                tab_boxes,
                f"{name}_{key}",
                font,
                key,
                value[key],
                state,
                [1, i + 1],
                [1, i + 1, 2],
            )
