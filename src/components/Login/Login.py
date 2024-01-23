import subprocess
from tkinter import Toplevel, StringVar, Entry, Label, Button
from tkinter import END


class Login(Toplevel):
    """
    Tkinter Component with Simple Login Page
    Parameters
    ----------
    settings: dict
        Settings
    screen_size : dict
        Providing Screen Size (Width and Height) to Class.
    cap : VideoCapture
        Returns a tuple (success, frame)
    light : Lighting Component
        Instantiate Lighting Component to pass to next Class
    """

    def __init__(self, settings, screen_size):
        Toplevel.__init__(self)
        self.initialize(settings)
        self.win_config(screen_size)
        self.widgets()
        self.grab_set()
        self.mainloop()

    def initialize(self, settings):
        self.set_set = settings["Settings"]
        self.res = [False, False]
        subprocess.Popen("osk", stdout=subprocess.PIPE, shell=True)

    def check_login(self, string_var, log_entry):
        for cred in self.set_set["Credentials"].values():
            if cred["Username"] == string_var["Username"].get():
                if cred["Password"] == string_var["Password"].get():
                    self.res = [True, cred["Superuser"]]
                    self.destroy()
                    self.quit()
                    return
                else:
                    self.bad_pass.config(text="Password does not exist")
                    self.bad_pass.grid(row=2, column=2, columnspan=2)
                    log_entry["Password"].delete(0, END)
                    return
        self.bad_pass.config(text="Username does not exist")
        self.bad_pass.grid(row=2, column=2, columnspan=2)
        for i, cred in enumerate(log_entry):
            if i == 0:
                log_entry[cred].focus()
            log_entry[cred].delete(0, END)
        return

    def win_config(self, screen_size):
        self.title("ME Login")
        self.config(bg="lightgrey", bd=50)
        self.geometry(
            f"{int(screen_size['w_screen']/4)}x{int(screen_size['h_screen']/4)}+{int(screen_size['w_screen']*3/8)}+{int(screen_size['h_screen']*1/8)}"
        )
        self.rowconfigure(5, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(4, weight=1)

    def widgets(self):
        self.bad_pass = Label(self, bg="#fa6464")
        credentials = list(self.set_set["Credentials"].values())[0]
        string_var = {}
        entry_log = {}
        for i, cred in enumerate(credentials):
            if i == 2:
                break
            Label(self, text=cred + " :", background="lightgrey").grid(row=i, column=1)
            string_var[cred] = StringVar()
            entry_log[cred] = Entry(self, textvariable=string_var[cred])
            if cred.lower() == "password":
                entry_log[cred].config(show="*")
            entry_log[cred].grid(row=i, column=2, columnspan=2)

        Button(
            self, text="Login", command=lambda: self.check_login(string_var, entry_log)
        ).grid(row=6, column=2, columnspan=2)
