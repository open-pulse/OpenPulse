from PySide6.QtGui import QDoubleValidator


class StrictDoubleValidator(QDoubleValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_acceptable = None

    def fixup(self, string: str):
        if self._last_acceptable is None:
            return str(self.bottom())

        if is_numeric(string):
            value = float(string)
            if value < self.bottom():
                return str(self.bottom())
            elif value > self.top():
                return str(self.top())

        return self._last_acceptable

    def validate(self, string: str, pos: int):
        string = string.replace(",", ".")

        if not string:
            return QDoubleValidator.State.Intermediate, string, pos

        if string.count(".") > 1:
            return QDoubleValidator.State.Invalid, string, pos

        return_value = super().validate(string, pos)
        if return_value[0] == QDoubleValidator.State.Acceptable:
            self._last_acceptable = string

        return return_value


def is_numeric(value: str):
    try:
        float(value)
        return True
    except Exception:
        return False
