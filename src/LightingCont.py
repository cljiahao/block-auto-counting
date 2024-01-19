import sys
import json
import socket
from tkinter import messagebox

with open('settings.json') as f:
    setData = json.load(f)
    config = setData['Config']
    misc = setData['Misc']
    trouble = misc['Trouble']
    light = misc['Lighting']
    HOST = config['LightIPv4']
    PORT = int(config['LightPORT'])

# Turn on lighting controller
def lightingOn():
   
    if not trouble:
        lightOn = "@00L11D\r\n"
        lightOnarr = []
        for i in lightOn:
            lightOnarr.append(ord(i))
        bLightOnarr = bytearray(lightOnarr)
        s.send(bLightOnarr)
        print(bLightOnarr,"sent")

# Turn off lighting controller
def lightingOff():

    if not trouble:
        lightOff = "@00L01C\r\n"
        lightOffarr = []
        for i in lightOff:
            lightOffarr.append(ord(i))
        bLightOffarr = bytearray(lightOffarr)
        print(bLightOffarr)
        s.send(bLightOffarr)
        print("sent")

# Light Intensity Based from Excel Sheet
def Checksum(ComForm):

    Comarr = []
    for i in ComForm:
        Comarr.append(ord(i))
    ComCheck = bytearray(Comarr)
    CheckSum = hex(sum(ComCheck))[-2:].upper()

    return CheckSum

# Standardise the lighting intensity digit
def intenseUtil(check):

    if len(check) == 0 or check == 0:
        check = "100"   # Default
    elif len(check) == 1:
        check = "00" + check
    elif len(check) == 2:
        check = "0" + check

    return check

# Update new Light Intensity
def lightIntense():
    if not trouble:
        intensity = intenseUtil(light)
        
        preinten = "@00F"+intensity
        checksum = Checksum(preinten)
        Command = preinten + checksum+"\r\n"

        arrComm = []
        for i in Command:
            arrComm.append(ord(i))
        byteCommand = bytearray(arrComm)
        print(byteCommand)
        s.send(byteCommand)
        print("sent")

if trouble:
    pass
else:
    # Establish Connection with controller 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting ",HOST)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.connect((HOST, PORT))
        print("connected to ",HOST)
        lightingOff()
    except (ConnectionRefusedError, TimeoutError):
        messagebox.showerror("Connection Error","Connection to Lighting Controller Error. \nPlease Restart Controller.")
        print("Error Connecting to ",HOST)
        sys.exit()