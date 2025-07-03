chip_size_tab = {
    "headers": {
        "length": {"name": "Length"},
        "width": {"name": "Width"},
        "factor": {"name": "Factor"},
    },
    "widgets": {
        "02": {"name": "KEM 02"},
        "03": {"name": "KEM 03"},
        "15": {"name": "KEM 15"},
    },
}

settings_tab = {
    "widgets": {
        "troubleshoot": {
            "name": "Troubleshoot Mode",
            "type": "radio",
            "value": "true",
        },
        "light_intensity": {
            "name": "Light Intensity / 255",
            "type": "entry",
            "value": "20",
        },
        "camera_res_width": {
            "name": "Camera Res Width (px)",
            "type": "entry",
            "value": "1920",
        },
        "camera_res_height": {
            "name": "Camera Res Height (px)",
            "type": "entry",
            "value": "1080",
        },
        "cali_pin_size": {
            "name": "Calibration Pin Diameter (mm)",
            "type": "entry",
            "value": "5",
        },
        "tolerance": {
            "name": "Accuracy tolerance (%)",
            "type": "entry",
            "value": "10",
        },
    },
}

credentials_tab = {
    "headers": {
        "username": {"name": "Username"},
        "password": {"name": "Password"},
        "superuser": {"name": "Superuser"},
    }
}
