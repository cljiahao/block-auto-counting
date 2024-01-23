from tkinter import Label, Entry
from tkinter import LEFT, CENTER, E, W


def wos_entry(frame_wos, set_names, wos_var, reg_entry):
    for d, wos_name in enumerate(set_names["WOS ERR"].keys()):
        # Algo for rows and columns
        e = int(d / 2)
        f = 0 if d % 2 == 0 else 4
        # WOS Name
        Label(frame_wos, text=wos_name, wraplength=50, justify=LEFT).grid(
            row=e, column=f, pady=5, padx=3, sticky=W
        )
        # WOS Entry Box
        wos_var[wos_name] = Entry(
            frame_wos,
            name=wos_name.lower(),
            font=set_names["Font"]["L"],
            width=13,
            justify=CENTER,
            validate="key",
            validatecommand=reg_entry,
        )

        wos_var[wos_name].grid(row=e, column=f + 1, columnspan=2, pady=3, sticky=E)
