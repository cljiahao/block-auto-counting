import os
import math
import time
from copy import deepcopy
from tkinter import messagebox

from components.BladeData.BladeData import BladeData
from components.Login.Login import Login
from components.Selection.Selection import Selection
from components.UserInput.InputBox import InputBox
from pages.Accuracy.Accuracy import Accuracy
from pages.Main.utils.camera import process_img
from pages.Main.utils.check import check_entry
from pages.Main.utils.error import Custom_Exception
from pages.Main.utils.utils import def_reset, draw_img, save_excel, time_print
from pages.Settings.Settings import Settings
from pages.Summary.Summary import Summary
from utils.directory import dire
from utils.features import cvt_image


def get_num_input(settings, screen_size, def_var, wos_var, excel_path, text):
    """Show Numpad and get data from user input"""
    try:
        check_entry(settings, wos_var, False)
        input_val = InputBox(settings, screen_size, text).input_val.get()

        if input_val == "":
            input_val = 0
        def_var[text].config(text=input_val)

        save_excel(excel_path, def_var, text)

    # TODO: Create logging method
    except Custom_Exception as e:
        messagebox.showerror(**eval(str(e)))
    except Exception as e:
        print(
            f"Error in '{os.path.relpath(__file__,os.getcwd())}' at line {e.__traceback__.tb_lineno} \nError Message: \n'{e}'"
        )
        messagebox.showerror(title="Exception Error", message=str(e))


def get_blade_data(settings, def_var, wos_var, def_name):
    try:
        check_entry(settings, wos_var, False)

        BladeData(settings, wos_var["Lot Number"].get(), def_var[def_name])

    except Custom_Exception as e:
        messagebox.showerror(**eval(str(e)))
    except Exception as e:
        print(
            f"Error in '{os.path.relpath(__file__,os.getcwd())}' at line {e.__traceack__.tb_lineno} \nError Message: \n'{e}'"
        )
        messagebox.showerror(title="Exception Error", message=str(e))


def show_summary(settings, screen_size, wos_var, excel_path):
    """Show Summary Page"""
    try:
        check_entry(settings, wos_var, True)

        Summary(settings, screen_size, wos_var, excel_path)

    # TODO: Create logging method
    except Custom_Exception as e:
        messagebox.showerror(**eval(str(e)))
    except Exception as e:
        print(
            f"Error in '{os.path.relpath(__file__,os.getcwd())}' at line {e.__traceback__.tb_lineno} \nError Message: \n'{e}'"
        )
        messagebox.showerror(title="Exception Error", message=str(e))


def show_accuracy(settings, screen_size, light, mat):
    """Show Accuracy Page"""
    try:
        set_set = settings["Settings"]
        troubleshoot = set_set["Troubleshoot"]
        chip_type = "02"
        new_start = time_print(time.time(), "Initialize")

        defects, block = process_img(
            settings, light, mat, chip_type, troubleshoot, dire.path_acc
        )
        new_start = time_print(new_start, "Processing Image")

        calc_accuracy = deepcopy(set_set["Accuracy"][mat])
        drawn_img = block.copy()
        for col, arr in list(defects.items()):
            if col in calc_accuracy:
                calc_accuracy[col]["Num"] = len(arr)
                calc_accuracy[col]["Area"] = math.ceil(
                    sum([sum(list(x.keys())) for x in arr])
                )
                drawn_img = draw_img(
                    drawn_img,
                    [list(x.values())[0] for x in arr],
                    [list(x.keys())[0] for x in arr],
                )

        new_start = time_print(new_start, "Processing Data and Draw Image")

        Accuracy(settings, screen_size, drawn_img, calc_accuracy, mat)

    # TODO: Create logging method
    except Custom_Exception as e:
        messagebox.showerror(**eval(str(e)))
        if not troubleshoot["Trouble"]:
            light.light_switch()
    except Exception as e:
        print(
            f"Error in '{os.path.relpath(__file__,os.getcwd())}' at line {e.__traceback__.tb_lineno} \nError Message: \n'{e}'"
        )
        messagebox.showerror(title="Exception Error", message=str(e))
        if not troubleshoot["Trouble"]:
            light.light_switch()


def show_settings(self, settings, screen_size, light, mode, refresh):
    """Show Settings Page"""
    try:
        login, superuser = Login(settings, screen_size).res
        if login:
            res = Settings(mode, light, superuser).res
            if res:
                self.light.close()
                self.destroy()
                refresh()

    # TODO: Create logging method
    except Custom_Exception as e:
        messagebox.showerror(**eval(str(e)))
    except Exception as e:
        print(
            f"Error in '{os.path.relpath(__file__,os.getcwd())}' at line {e.__traceback__.tb_lineno} \nError Message: \n'{e}'"
        )
        messagebox.showerror(title="Exception Error", message=str(e))


def snap(
    settings,
    screen_size,
    wos_var,
    def_var,
    excel_path,
    light,
    chip_type_var,
    mat,
    capture,
):
    """Snap image and process"""
    try:
        set_set = settings["Settings"]
        set_names = settings["Names"]
        troubleshoot = set_set["Troubleshoot"]
        capture.config(image="")
        def_reset(def_var)
        check_entry(settings, wos_var, True)

        chip_type = "02" if troubleshoot else chip_type_var.cget("text")[-2:]
        chip_area = float(set_set["Chip"][chip_type]["L"]) * float(
            set_set["Chip"][chip_type]["W"]
        )
        new_start = time_print(time.time(), "Initialize")

        defects, block = process_img(
            settings, light, mat, chip_type, troubleshoot, dire.path_block
        )
        new_start = time_print(new_start, "Processing Image")

        selected = {}
        to_select = {}
        drawn_img = block.copy()
        for col, arr in list(defects.items()):
            if col in set_names["Defect Sticker"][chip_type]:
                def_mode = set_names["Defect Sticker"][chip_type][col]
                selected[def_mode] = sum(
                    [math.ceil(sum(list(k.keys())) / chip_area) for k in arr]
                )
            else:
                to_select[col] = defects.pop(col)
                drawn_img = draw_img(drawn_img, [list(x.values())[0] for x in arr])

        new_start = time_print(new_start, "Processing Data and Draw Image")

        Selection(settings, screen_size, chip_area, drawn_img, to_select, selected)

        for def_mode, quantity in selected.items():
            def_var[def_mode].config(text=quantity)

        imgtk = cvt_image(block)
        capture.imgtk = imgtk
        capture.config(image=imgtk)

        save_excel(excel_path, def_var)

    # TODO: Create logging method
    except Custom_Exception as e:
        messagebox.showerror(**eval(str(e)))
        if not troubleshoot["Trouble"]:
            light.light_switch()
    except Exception as e:
        print(
            f"Error in '{os.path.relpath(__file__,os.getcwd())}' at line {e.__traceback__.tb_lineno} \nError Message: \n'{e}'"
        )
        messagebox.showerror(title="Exception Error", message=str(e))
        if not troubleshoot["Trouble"]:
            light.light_switch()
