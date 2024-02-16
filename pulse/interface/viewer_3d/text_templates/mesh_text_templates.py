from itertools import accumulate, count
from math import ceil, floor


def extract_line(strings, max_width, separator_size):
    line = []
    current_width = 0
    for string in strings:
        if len(string) + current_width + separator_size > max_width:
            break
        line.append(string)
        current_width += len(string) + separator_size
    return line

def format_long_sequence(sequence, max_width=30, max_lines=5, item_separator=", ", identation="  "):
    strings = [str(i) for i in sequence]

    initial_lines = []
    for _ in range(ceil(max_lines / 2)):
        new_line = extract_line(strings, max_width, len(item_separator))
        if not new_line:
            break
        initial_lines.append(new_line)
        strings = strings[len(new_line):]

    strings.reverse()
    final_lines = []
    for _ in range(floor(max_lines / 2)):
        new_line = extract_line(strings, max_width, len(item_separator))
        if not new_line:
            break
        final_lines.append(new_line)
        strings = strings[len(new_line):]
    final_lines.reverse()

    if strings and initial_lines and final_lines:
        lines = initial_lines + [["..."]] + final_lines
    else:
        lines = initial_lines + final_lines

    formated_lines = [item_separator.join(line) for line in lines]
    concatenated_lines = identation + f"\n{identation}".join(formated_lines)
    return concatenated_lines


MULTIPLE_NODES_SELECTION_TEMPLATE = (
    "{selection_size} NODES IN SELECTION\n"
    "{selection_ids}\n"
    "\n"
)


MULTIPLE_ELEMENTS_SELECTION_TEMPLATE = (
    "{selection_size} ELEMENTS IN SELECTION\n"
    "{selection_ids}\n"
    "\n"
)


MULTIPLE_ENTITIES_SELECTION_TEMPLATE = (
    "{selection_size} LINES IN SELECTION\n"
    "{selection_ids}\n"
    "\n"
)
