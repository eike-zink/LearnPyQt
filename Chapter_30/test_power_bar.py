import sys

from PyQt5 import QtWidgets, QtCore
from power_bar import PowerBar


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        layout = QtWidgets.QHBoxLayout()

        for col in range(0, 10):
            power_bar = PowerBar(10, self)
            layout.addWidget(power_bar)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setMinimumSize(QtCore.QSize(1000, 400))
        self.setCentralWidget(widget)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
