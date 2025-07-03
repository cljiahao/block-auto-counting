import socket
import sys
from tkinter import Toplevel

from components.messagebox import CustomMessageBox
from core.config import service_settings
from core.logging import logger


class LightingControl:
    def __init__(self, parent: Toplevel) -> None:
        self.parent = parent
        logger.info(
            f"Connecting to {service_settings.LIGHT_IPV4} at {service_settings.LIGHT_PORT}"
        )
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.connect(
                (service_settings.LIGHT_IPV4, int(service_settings.LIGHT_PORT))
            )
            logger.info(
                f"Connected to {service_settings.LIGHT_IPV4} at {service_settings.LIGHT_PORT}"
            )
            self.light_switch()
        except (ConnectionRefusedError, TimeoutError):
            CustomMessageBox(
                parent,
                "Connection to Light Error",
                "Conection to Lighting Controller Error. Please Restart Controller.",
                "showerror",
            )
            # TODO: check if sys.exit or self.close is better
            sys.exit()

    def close(self) -> None:
        """Shut off Lighting to reset"""
        if hasattr(self, "s"):
            self.s.close()

    def _cvt_byte(self, code: str) -> bytearray:
        "Convert str to byte"
        arr = [ord(i) for i in code]
        return bytearray(arr)

    def light_switch(self, on: bool = False) -> None:
        """Light Switch function"""
        light_code = "@00L11D\r\n" if on else "@00L01C\r\n"
        b_light_arr = self._cvt_byte(light_code)
        self.s.send(b_light_arr)
        logger.info(f"{b_light_arr} sent. Light turned {'on' if on else 'off'}.")

    def _intense_util(self, value: str):
        """Convert value to standard of 000 format"""
        if len(value) == 2:
            value = f"0{value}"
        elif len(value) == 1:
            value = f"00{value}"
        else:
            value = "050"  # Default
        return value

    def light_intense(self, settings):
        """Update lighting intensity"""
        intensity = self._intense_util(settings["Settings"]["Config"]["Lighting"])

        pre_intense = f"@00F{intensity}"
        b_arr = self._cvt_byte(pre_intense)
        check_sum = hex(sum(b_arr))[-2:].upper()
        command = f"{pre_intense}{check_sum}\r\n"

        b_command = self._cvt_byte(command)
        self.s.send(b_command)
        logger.info(f"{b_command} sent. Light intensity changed to {intensity}.")
