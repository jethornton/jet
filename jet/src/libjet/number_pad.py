import sys, os

from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class number_pad(QDialog):
	def __init__(self):
		super().__init__()

		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))

		# set the library path
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libjet'
			self.gui_path = '/usr/lib/libjet'
		else:
			self.lib_path = os.path.join(self.path, 'libjet')
			self.gui_path = self.path

		num_ui_path = os.path.join(self.gui_path, 'numbers.ui')
		loadUi(num_ui_path, self)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.dot_pb.clicked.connect(self.dot)
		self.dash_pb.clicked.connect(self.dash)
		for i in range(10):
			getattr(self, f'num_pb_{i}').clicked.connect(self.post)

	def post(self):
		txt = self.numbers_lb.text()
		self.numbers_lb.setText(f'{txt}{self.sender().objectName()[-1]}')

	def clear(self):
		self.numbers_lb.clear()

	def dot(self):
		txt = self.numbers_lb.text()
		self.numbers_lb.setText(f'{txt}.')

	def dash(self):
		txt = self.numbers_lb.text()
		self.numbers_lb.setText(f'-{txt}')

	def retval(self):
		try:
			return(float(self.numbers_lb.text()))
		except:
			return False

