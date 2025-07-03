defect_info = {
    "U1": {
        "name": "LOUT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "U2": {
        "name": "WOUT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "U3": {
        "name": "DEFORMED",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "U4": {
        "name": "BLUNTCUT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "U5": {
        "name": "ROUGHCUT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "U6": {
        "name": "SLANTCUT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "U7": {
        "name": "LSHIFT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "U8": {
        "name": "WSHIFT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "U9": {
        "name": "STEPSHIFT",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "UA": {
        "name": "VPDENT",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UB": {
        "name": "SMEARING",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UC": {
        "name": "PARTIALPRINT",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UD": {
        "name": "SHEETNG",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UE": {
        "name": "RIDGENDENT",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UF": {
        "name": "BROKENBLADE",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UK": {
        "name": "PATTERNDENT",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UL": {
        "name": "LINE",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UR": {
        "name": "DRAGGING",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "US": {
        "name": "ELECTRODEHORN",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "UT": {
        "name": "CUTDEBRIS",
        "value": "0",
        "type": "label",
        "for_tape": False,
    },
    "O1": {
        "name": "OTHERS",
        "value": "0",
        "type": "label",
        "for_tape": True,
    },
    "I1": {
        "name": "DROPCHIP",
        "value": "0",
        "type": "button",
        "button_key": "num_pad",
        "for_tape": False,
    },
    "L1": {
        "name": "SAMPLE",
        "value": "0",
        "type": "button",
        "button_key": "num_pad",
        "for_tape": False,
    },
    "BD": {
        "name": "BLADEDATA",
        "value": "None",
        "type": "button",
        "button_key": "blade_data",
        "for_tape": False,
    },
}

defect_names = [
    defect["name"] for defect in defect_info.values() if defect["type"] == "label"
]

tape_defect_names = [
    defect["name"] for defect in defect_info.values() if defect["for_tape"]
]

reverse_defect_mapping = {value["name"]: key for key, value in defect_info.items()}
