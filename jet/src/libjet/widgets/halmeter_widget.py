"""
 Example Widget for JT.

 This is a modular widget which can be a drag and drop widget in QT Designer.
"""
import random

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtProperty

import hal

class HalMeterWidget(QtWidgets.QWidget):
	def __init__(self, parent=None, sim=False):
		super().__init__(parent)

		self.h = hal.component(f"halmeter-{random.randint(0, 1000)}")
		self._value = 0.0
		self._min = 0.0
		self._max = 0.0
		self._label = "Value"

		self.setupUi(parent)

		self.font = QtGui.QFont()

		# Designer, Don't run the widget
		if not sim:
			self.cyclic_timer = QtCore.QTimer(self)
			self.cyclic_timer.timeout.connect(self.periodic)
			self.cyclic_timer.start(100)

		self.h.ready()

	def setupUi(self, parent):
		self.setMinimumSize(100, 100)
		self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

		self.mainlayout = QtWidgets.QVBoxLayout(parent)
		self.setLayout(self.mainlayout)

		self.pin_label = QtWidgets.QLineEdit("Enter Pin")
		self.mainlayout.addWidget(self.pin_label)
		
		self.pin_actual = QtWidgets.QLabel("")
		self.mainlayout.addWidget(self.pin_actual)

		self.value_label = QtWidgets.QLabel("0.0000")
		self.value_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.mainlayout.addWidget(self.value_label)

		self.min_label = QtWidgets.QLabel("Min")
		self.min_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.mainlayout.addWidget(self.min_label)

		self.min_value = QtWidgets.QLabel("0.0000")
		self.min_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.mainlayout.addWidget(self.min_value)

		self.max_label = QtWidgets.QLabel("Max")
		self.max_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.mainlayout.addWidget(self.max_label)

		self.max_value = QtWidgets.QLabel("0.0000")
		self.max_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.mainlayout.addWidget(self.max_value)

		self.reset_button = QtWidgets.QPushButton("Reset")
		self.reset_button.clicked.connect(self.reset)
		self.mainlayout.addWidget(self.reset_button)

	def reset(self):
		self._min = self._value
		self._max = self._value

	def periodic(self):
		"""Update the display every 100 ms"""
		current_dict = hal.get_info_pins()
		for pin in current_dict:
			if self.pin_label.text() in pin["NAME"]:
				try:
					# Reset Min and Max if the label changes
					if pin["NAME"] != self._label:
						self._label = pin["NAME"]
						self._min = float(pin["VALUE"])
						self._max = float(pin["VALUE"])
						self.pin_actual.setText(pin["NAME"])
					self._value = float(pin["VALUE"])
					break
				except ValueError:
					pass

		self.value_label.setText(f"{self._value:.4f}")
		self._min = min(self._min, self._value)
		self._max = max(self._max, self._value)
		self.min_value.setText(f"{self._min:.4f}")
		self.max_value.setText(f"{self._max:.4f}")

	def set_font(self, font):
		# Example Pyqt Property
		self.font = font
		self.value_label.setFont(font)
		self.min_label.setFont(font)
		self.min_value.setFont(font)
		self.max_label.setFont(font)
		self.max_value.setFont(font)
		self.reset_button.setFont(font)

	def get_font(self):
		return self.font

	axis_font = pyqtProperty(QtGui.QFont, get_font, set_font)


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	widget = HalMeterWidget()
	widget.show()
	sys.exit(app.exec())

