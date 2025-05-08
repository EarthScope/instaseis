#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Originally from https://gist.github.com/jdreaver/0be2e44981159d0854f5
Modified for PySide6 compatibility
"""

from PySide6 import QtGui, QtWidgets
import numpy as np
import re

# Regular expression to find floats. Match groups are the whole string, the
# whole coefficient, the decimal part of the coefficient, and the exponent
# part.
_float_re = re.compile(r"(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)")


def valid_float_string(string):
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False


class FloatValidator(QtGui.QValidator):
    def validate(self, string, position):
        string = str(string)
        if valid_float_string(string):
            return (self.Acceptable, string, position)
        if string == "" or string[position - 1] in "e.-+":
            return (self.Intermediate, string, position)
        return (self.Invalid, string, position)

    def fixup(self, text):
        match = _float_re.search(text)
        return match.groups()[0] if match else ""


class ScientificDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        super(ScientificDoubleSpinBox, self).__init__(*args, **kwargs)
        self.setMinimum(-np.inf)
        self.setMaximum(np.inf)
        # self.validator = FloatValidator()
        self.setDecimals(1000)

    def validate(self, text, position):
        return
        return self.validator.validate(text, position)

    def fixup(self, text):
        return
        return self.validator.fixup(text)

    def valueFromText(self, text):
        return float(text)

    def textFromValue(self, value):
        return format_float(value)

    def stepBy(self, steps):
        text = self.cleanText()
        groups = _float_re.search(text).groups()
        decimal = float(groups[1])
        decimal += steps
        new_string = "{:g}".format(decimal) + (groups[3] if groups[3] else "")
        self.lineEdit().setText(new_string)


def format_float(value):
    """Modified form of the 'g' format specifier."""
    string = "{:g}".format(value).replace("e+", "e")
    string = re.sub(r"e(-?)0*(\d+)", r"e\1\2", string)
    return string


# Example usage:
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)

    label = QtWidgets.QLabel("Scientific Double Spin Box:")
    spin_box = ScientificDoubleSpinBox()
    spin_box.setValue(123.456)

    layout.addWidget(label)
    layout.addWidget(spin_box)

    window.setWindowTitle("Scientific Spin Box Demo")
    window.resize(300, 100)
    window.show()

    sys.exit(app.exec())
