from collections import namedtuple, OrderedDict


TreeItem = namedtuple("TreeItem", ["name", "data", "unity"])
SEPARATOR = TreeItem("", "", "")


class TreeInfo:
    def __init__(self, name: str) -> None:
        self.name = name
        self.items = list()

    def add_separator(self):
        self.items.append(TreeItem("", "", ""))
        return TreeItem("", "", "")

    def add_item(self, name, data, unity="") -> TreeItem:
        item = TreeItem(name, data, unity)
        self.items.append(item)
        return item

    def items_without_extra_separators(self):
        extra_separators = 0
        for item in reversed(self.items):
            if item != SEPARATOR:
                break
            extra_separators += 1
        return self.items[:len(self.items) - extra_separators]

    def __str__(self):
        title = self.name.upper()
        longest_name = max(0, *[len(item.name) for item in self.items])
        longest_data = max(0, *[len(str(item.data)) for item in self.items])
        spaces = longest_name + longest_data + 3

        text = f"{title} \n"
        pruned_items = self.items_without_extra_separators()

        for item in pruned_items[:-1]:
            if item == SEPARATOR:
                text += "│\n"
                continue
            spacer = " " * (spaces - len(item.name) - len(str(item.data)))
            unity = f"[{item.unity}]" if item.unity else ""
            text += f"├─{item.name}: {spacer}{item.data} {unity}\n"

        # last item
        item = pruned_items[-1]
        spacer = " " * (spaces - len(item.name) - len(str(item.data)))
        unity = f"[{item.unity}]" if item.unity else ""
        text += f"└─{item.name}: {spacer}{item.data} {unity}\n"
        text += "\n"
        return text
