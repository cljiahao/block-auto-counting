import sys
import socket
from tkinter import messagebox

from core.logging import logger


class Lighting:
    """Class for Lighting Controls"""

    def __init__(self, settings):
        self.trouble = settings["Settings"]["Troubleshoot"]["Trouble"]
        self.initialize(settings)

    def initialize(self, settings):
        """Initialize variables"""
        if not self.trouble:
            lightipv4 = settings["Settings"]["Address"]["LightIPv4"]
            lightport = settings["Settings"]["Address"]["LightPORT"]
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logger.info("Connecting to %s at %s", lightipv4, lightport)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                self.s.connect(
                    (
                        lightipv4,
                        int(lightport),
                    )
                )
                logger.info("Connected to %s at %s", lightipv4, lightport)
                self.light_switch()
            except (ConnectionRefusedError, TimeoutError):
                messagebox.showerror(
                    "Connection Error",
                    "Connection to Lighting Controller Error. \nPlease Restart Controller",
                )
                logger.error(
                    "Error Connecting to %s at %s", lightipv4, lightport, exc_info=True
                )
                sys.exit()

    def close(self):
        """Shut off Lighting to reset"""
        if hasattr(self, "s"):
            self.s.close()

    def cvt_byte(self, code):
        "Convert str to byte"
        arr = []
        for i in code:
            arr.append(ord(i))
        b_arr = bytearray(arr)

        return b_arr

    def light_switch(self, on=False):
        """Light Switch function"""
        if not self.trouble:
            light_code = "@00L11D\r\n" if on else "@00L01C\r\n"
            b_light_arr = self.cvt_byte(light_code)
            self.s.send(b_light_arr)
            logger.info("%s sent. Light turned %s.", b_light_arr, "on" if on else "off")

    def light_intense(self, settings):
        """Update lighting intensity"""
        if not self.trouble:
            intensity = self.intense_util(settings["Settings"]["Config"]["Lighting"])

            pre_intense = f"@00F{intensity}"
            b_arr = self.cvt_byte(pre_intense)
            check_sum = hex(sum(b_arr))[-2:].upper()
            command = f"{pre_intense}{check_sum}\r\n"

            b_command = self.cvt_byte(command)
            self.s.send(b_command)
            logger.info("%s sent. Light intensity changed to %s.", b_command, intensity)

    def intense_util(self, value):
        """Convert value to standard of 000 format"""
        if len(value) == 2:
            value = f"0{value}"
        elif len(value) == 1:
            value = f"00{value}"
        else:
            value = "050"  # Default
        return value
