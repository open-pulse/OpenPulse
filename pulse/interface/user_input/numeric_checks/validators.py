from PySide6.QtGui import QDoubleValidator

class StrictDoubleValidator(QDoubleValidator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, string: str, pos: int):

        # if the string contains a comma, we reject
        if "," in string:
            return QDoubleValidator.State.Invalid, string, pos

        # if the string contains more than one point, we reject
        if "." in string:
            if string.count(".") > 1:
                return QDoubleValidator.State.Invalid, string, pos

        if is_numeric(string):
            # check minimum value
            if float(string) < self.bottom():
                return QDoubleValidator.State.Invalid, string, pos

            # check maximum value
            if float(string) > self.top():
                return QDoubleValidator.State.Invalid, string, pos

        # let the QDoubleValidator work normally, otherwise
        return super().validate(string, pos)


def is_numeric(value: str):
    try:
        float(value)
        return True
    except Exception:
        return False