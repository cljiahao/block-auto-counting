import requests
from tkinter import END

from pages.Main.utils.error import Custom_Exception


def input_retrieve(address, lot_no, qty_entry, chip_type):
    url = address + lot_no
    res = requests.get(url)
    if not res.status_code == 200:
        raise Custom_Exception(
            {
                "title": "Lot not Found in Database",
                "message": "Lot not Found in Database",
            }
        )
    qty_entry.delete(0, END)
    qty_entry.insert(0, res.json()["sun0011"])
    chip_code = (
        ["Error!", "#fa6464"]
        if res.json()["cdc0163"] == None
        else [res.json()["cdc0163"][:5], "#a6eca8"]
    )
    chip_type.config(text=chip_code[0], bg=chip_code[1])


def check_entry(settings, wos_var, bool=False):
    for key in settings["Names"]["WOS ERR"].keys():
        if key == "Lot Number" and len(wos_var[key].get()) != 10:
            raise Custom_Exception(settings["Names"]["WOS ERR"][key])
        if bool:
            if len(wos_var[key].get()) == 0:
                raise Custom_Exception(settings["Names"]["WOS ERR"][key])

    return True
