base_font_size = {
    "default": ("Segoe UI", "9"),
    "xs": ("Calibri", "12"),
    "s": ("Calibri", "14"),
    "m": ("Calibri", "16"),
    "l": ("Calibri", "18"),
    "xl": ("Calibri", "20"),
    "2xl": ("Calibri", "22"),
    "3xl": ("Calibri", "24"),
}

font_size = {
    **base_font_size,
    **{k.upper(): (*v, "bold") for k, v in base_font_size.items()},
}
