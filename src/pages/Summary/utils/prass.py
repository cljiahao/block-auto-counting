import os
import requests
import pandas as pd
from tkinter import messagebox
from datetime import datetime as dt

from utils.directory import dire


def send_PRASS(settings, wos_var, df, blade):
    """Send to PRASS after cleanup and txt creation"""
    new_df = df_cleanup(wos_var, df)
    file_path = create_PRASS_txt(settings, wos_var, new_df, blade)

    # Can't send to PRASS in Trouble Mode
    if settings["Settings"]["Troubleshoot"]["Trouble"]:
        messagebox.showerror(
            title="Can't send to PRASS",
            message="Troubleshooting mode cannot send to PRASS",
        )
        return "", False

    # To send via FTP
    """
    with FTP("163.50.33.28","s8pc","prasspc") as ftp:
    ftp.cwd('/fa/thermal_release/')
    file = open(os.path.join(file_path),'rb')
    ftp.storbinary(f'STOR {os.path.basename(file_path)}.txt',file)
    file.close()
    ftp.quit()
    """

    # To Send via HTTP
    files = {"file": open(file_path, "rb")}
    resp = requests.post(settings["Settings"]["Address"]["fileServer"], files=files)

    print(f"fileSize: {int(resp.content)}")
    # Request OK, bring up website and final quantity for final cross check
    return new_df, int(resp.content) == os.stat(file_path).st_size


def create_PRASS_txt(settings, wos_var, new_df, blade):
    """Create txt to send to PRASS"""
    lot_no = wos_var["Lot Number"].get()
    pay_roll = wos_var["Payroll Number"].get()
    mc_no = wos_var["M/C Number"].get()
    in_qty = wos_var["Input Quantity"].get()

    date = dt.now().strftime("%Y/%m/%d")
    time = dt.now().strftime("%H:%M:%S")

    # Blade Data convert to String
    blade_str = "|".join(list(blade.values()))

    # Consolidate retrieved defects
    loop_df = new_df.loc[(new_df != 0).any(axis=1)]
    prass_def = ""
    for i, dataQty in enumerate(loop_df["Total"][:-2]):
        if i < len(loop_df["Total"]) - 1:
            prass_def += (
                f"{settings['Names']['Defect Code'][loop_df.index[i]]}|{dataQty}|"
            )

    # Range predetermined (Can be changed to increase [Currently 10])
    for j in range(10 - (len(loop_df["Total"]) - 1)):
        if j != range(10 - (len(loop_df["Total"]) - 1))[-1]:
            prass_def += "||"
        else:
            prass_def += "|"

    # String data to write to txt
    p_data = f"{lot_no}|{mc_no}|{pay_roll}|{date}|{time}|{in_qty}|{new_df.loc['Output','Total']}|{blade_str}|{prass_def}"

    # Make month year folder to save txt in
    folder_path = os.path.join(dire.path_prass, dt.today().strftime("%b%y"))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{lot_no}.txt")
    with open(file_path, "w") as f:
        f.write(p_data)

    return file_path


def df_cleanup(wos_var, base):
    """Dataframe data clean up"""
    df = base.iloc[:-1, :]
    df = df[:].reset_index(drop=True).set_index(df.columns[0])
    df = df.apply(pd.to_numeric)
    df["Total"] = df.sum(axis=1, skipna=True)
    df.loc["Total Defects"] = df.sum(axis=0, skipna=True)
    df = df.iloc[:, -1:]
    df.loc["Output"] = int(wos_var["Input Quantity"].get()) - int(
        df.loc["Total Defects", "Total"]
    )

    return df
