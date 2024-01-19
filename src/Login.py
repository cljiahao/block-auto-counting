import json

from tkinter import *
from Settings import *

class Login():

    """
    Toplevel for Login Widget
    Parameters
    ----------
    cap : VideoCapture
        Passing VideoCap information to next Class.
    Wscreen : str
        Providing Screen Size (Width) to Class.
    Hscreen : str
        Providing Screen Size (Height) to Class.
    """

    def __init__(self,cap,Wscreen,Hscreen):

        with open('settings.json') as f:
            setData = json.load(f)
            self.credential = {setData['Credentials']['Username'] : setData['Credentials']['Password']}

        self.cap = cap
        self.Wscreen,self.Hscreen = Wscreen,Hscreen
        self.bgcolor = 'lightgrey'
        self.root = Toplevel()
        self.root.title("ME Login")
        self.root.config(bg=self.bgcolor,bd=50)
        self.root.geometry(f"{int(Wscreen/4)}x{int(Hscreen/4)}+{int(Wscreen*3/8)}+{int(Hscreen*3/8)}")
        self.root.rowconfigure(index=5,weight=1)
        self.root.columnconfigure(index=1, weight=1)
        self.root.columnconfigure(index=4, weight=1)
        self.windows()
        self.root.grab_set()
        # self.root.mainloop()

    def windows(self):

        # StringVars (used to retrieve input from entry)
        self.the_user = StringVar()
        self.the_pass = StringVar()

        # Creating Label Widget
        Label(self.root, text="Username :", background=self.bgcolor).grid(row=0, column=1)
        Label(self.root, text="Password :", background=self.bgcolor).grid(row=1, column=1)
        self.bad_pass = Label(self.root, bg='red')

        # Entry fields
        self.username_1 = Entry(self.root, textvariable=self.the_user)
        self.password_1 = Entry(self.root, show='*', textvariable=self.the_pass)

        # Entry field Locations
        self.username_1.grid(row=0, column=2, columnspan=2)
        self.password_1.grid(row=1, column=2, columnspan=2)

        # Login Button
        Button(self.root, text="Login", command=lambda: self.check_login()).grid(row=6, column=2, columnspan=2)

    # Check Login credentials
    def check_login(self):
        username = self.the_user.get()
        password = self.the_pass.get()

        if username in self.credential.keys():
            if password == self.credential[username]:
                self.root.destroy()
                Settings(self.cap,self.Wscreen,self.Hscreen)

            else:
                self.bad_pass.config(text="Password does not match")
                self.bad_pass.grid(row=2, column=2, columnspan=2)
                self.password_1.delete(0, 'end')

        else:
            self.bad_pass.config(text="Username does not exist")
            self.bad_pass.grid(row=2, column=2, columnspan=2)
            self.password_1.delete(0, 'end')
