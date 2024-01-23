import sys
import socket
from tkinter import messagebox


class Lighting:
    def __init__(self, settings):
        self.trouble = settings["Settings"]["Troubleshoot"]["Trouble"]
        self.initialize(settings)

    def initialize(self, settings):
        if not self.trouble:
            lightipv4 = settings["Settings"]["Address"]["LightIPv4"]
            lightport = settings["Settings"]["Address"]["LightPORT"]
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connecting to {lightipv4} at {lightport}")
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                self.s.connect(
                    (
                        lightipv4,
                        int(lightport),
                    )
                )
                print(f"Connected to {lightipv4} at {lightport}")
                self.light_switch()
            except (ConnectionRefusedError, TimeoutError):
                messagebox.showerror(
                    "Connection Error",
                    "Connection to Lighting Controller Error. \nPlease Restart Controller",
                )
                print(f"Error Connecting to {lightipv4} at {lightport}")
                sys.exit()

    def close(self):
        if hasattr(self,"s"):
            self.s.close()

    def cvt_byte(self, code):
        arr = []
        for i in code:
            arr.append(ord(i))
        b_arr = bytearray(arr)

        return b_arr

    def light_switch(self, on=False):
        if not self.trouble:
            light_code = "@00L11D\r\n" if on else "@00L01C\r\n"
            b_light_arr = self.cvt_byte(light_code)
            self.s.send(b_light_arr)
            print(f"{b_light_arr} sent. Light turned {'on' if on else 'off'}.")

    def light_intense(self, settings):
        if not self.trouble:
            intensity = self.intense_util(settings["Settings"]["Config"]["Lighting"])

            pre_intense = f"@00F{intensity}"
            b_arr = self.cvt_byte(pre_intense)
            check_sum = hex(sum(b_arr))[-2:].upper()
            command = f"{pre_intense}{check_sum}\r\n"

            b_command = self.cvt_byte(command)
            self.s.send(b_command)
            print(f"{b_command} sent. Light intensity changed to {intensity}.")

    def intense_util(self, value):
        if len(value) == 2:
            value = f"0{value}"
        elif len(value) == 1:
            value = f"00{value}"
        else:
            value = "050"  # Default
        return value
