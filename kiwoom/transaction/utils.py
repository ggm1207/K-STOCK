def change_format(data):
    strip_data = data.lstrip("-0")

    try:
        format_data = format(int(strip_data), ",d")
    except ValueError:
        print(f"strip_data: {strip_data}")
        format_data = format(int("0"), ",d")

    if data.startswith("-"):
        format_data = "-" + format_data

    return format_data
