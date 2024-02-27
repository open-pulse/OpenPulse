from math import ceil, floor


def format_long_sequence(sequence, max_width=30, max_lines=3, item_separator=", ", identation="► "):
    strings = [str(i) for i in sequence]

    initial_lines = []
    for _ in range(ceil(max_lines / 2)):
        new_line = _extract_line(strings, max_width, len(item_separator))
        if not new_line:
            break
        initial_lines.append(new_line)
        strings = strings[len(new_line):]

    strings.reverse()
    final_lines = []
    for _ in range(floor(max_lines / 2)):
        new_line = _extract_line(strings, max_width, len(item_separator))
        if not new_line:
            break
        final_lines.append(new_line)
        strings = strings[len(new_line):]
    final_lines.reverse()

    if strings and initial_lines:
        initial_lines[-1] = ["..."]
    lines = initial_lines + final_lines

    formated_lines = [item_separator.join(line) for line in lines]
    concatenated_lines = identation + f"\n{identation}".join(formated_lines)
    return concatenated_lines

def _extract_line(strings, max_width, separator_size):
    line = []
    current_width = 0
    for string in strings:
        if len(string) + current_width + separator_size > max_width:
            break
        line.append(string)
        current_width += len(string) + separator_size
    return line
