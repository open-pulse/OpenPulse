from PySide6.QtGui import QDoubleValidator

class StrictDoubleValidator(QDoubleValidator):
    def validate(self, string, pos):
        # if the string contains a comma, we reject (Invalid)
        if "," in string:
            return QDoubleValidator.State.Invalid, string, pos

        # let the QDoubleValidator work normally, otherwise
        return super().validate(string, pos)