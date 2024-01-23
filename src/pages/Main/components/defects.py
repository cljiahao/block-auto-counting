from tkinter import Label, Button
from tkinter import RIDGE, W

from pages.Main.utils.routes import get_blade_data, get_num_input


def defect_list(frame_def, settings, wos_var, screen_size, excel_path):
    set_names = settings["Names"]
    def_var = {}
    for a, def_name in enumerate(set_names["Defect Code"]):
        # Algo for rows and columns
        b = 0 if a % 2 == 0 else 3
        c = int(a / 2)
        # Defect Code
        Label(frame_def, text=f"[{set_names['Defect Code'][def_name]}]").grid(
            row=c, column=b, padx=7, pady=5, sticky=W
        )
        # Defect Name
        if def_name in set_names["Defect Numpad"]:
            Button(
                frame_def,
                text=def_name,
                command=lambda def_name=def_name,: get_num_input(
                    settings,
                    screen_size,
                    def_var,
                    wos_var,
                    excel_path.get(),
                    def_name,
                ),
            ).grid(row=c, column=b + 1, pady=5, sticky=W)
        elif def_name == "BLADE DATA":
            Button(
                frame_def,
                text=def_name,
                command=lambda def_name=def_name: get_blade_data(
                    settings, def_var, wos_var, def_name
                ),
            ).grid(row=c, column=b + 1, pady=5, sticky=W)
        else:
            Label(frame_def, text=def_name).grid(row=c, column=b + 1, pady=5, sticky=W)
        # Defect Quantity
        def_var[def_name] = Label(frame_def, text="0", width=10, relief=RIDGE)
        def_var[def_name].grid(row=c, column=b + 2, pady=5, sticky=W)

    return def_var
