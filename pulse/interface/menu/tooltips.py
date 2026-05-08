from pulse.interface.menu.tooltips_dict import tooltips


def get_tooltip(property_name: str) -> str:
    if property_name not in tooltips:
        return ""

    text = tooltips[property_name]
    if not text:
        return ""

    return text