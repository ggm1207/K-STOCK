def change_format(data):
    strip_data = data.lstrip("-0")
    if strip_data == "" or strip_data == ".00":
        strip_data = "0"

    format_data = format(int(strip_data), ",d")
    if data.startswith("-"):
        format_data = "-" + format_data

    return format_data
