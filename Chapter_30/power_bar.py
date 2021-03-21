import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class _Bar(QtWidgets.QWidget):

    clickedValue = QtCore.pyqtSignal(int)

    def __init__(self, steps: [str]):
        super().__init__()
        self.steps = steps
        self.background_color = QtGui.QColor("black")
        self.padding = 4

        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

    def _calculate_clicked_value(self, e):
        max_value = self.parent().maximum()
        min_value = self.parent().minimum()
        dev_height = self.size().height() + (self.padding + 2)
        step_size = dev_height / len(self.steps)
        y_pos = e.y() - self.padding - step_size / 2
        percent = (dev_height - y_pos) / dev_height
        new_value = int(min_value + percent * (max_value - min_value))
        self.clickedValue.emit(new_value)

    def sizeHint(self):
        return QtCore.QSize(40, 120)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor("black"))
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        # Define canvas
        dev_height = painter.device().height() - (self.padding * 2)
        dev_width = painter.device().width() - (self.padding * 2)

        # Get Values from Dial
        max_value = self.parent().maximum()
        min_value = self.parent().minimum()
        current_value = self.parent().value()

        percent = (current_value - min_value) / (max_value - min_value)
        steps_to_draw = int(percent * len(self.steps))
        step_size = dev_height / len(self.steps)
        bar_height = step_size * 0.6

        for step in range(steps_to_draw):
            brush.setColor(QtGui.QColor(self.steps[step]))
            y_pos = (1 + step) * step_size
            rect = QtCore.QRect(self.padding, self.padding + dev_height - int(y_pos), dev_width, int(bar_height))
            painter.fillRect(rect, brush)
        painter.end()

    def mouseMoveEvent(self, e):
        self._calculate_clicked_value(e)

    def mousePressEvent(self, e):
        self._calculate_clicked_value(e)

    def update_bar(self):
        self.update()


class PowerBar(QtWidgets.QWidget):
    """
    Custom Qt Widget to show a power bar and a dial.
    """
    def __init__(self, steps, parent=None):
        super().__init__(parent)

        if isinstance(steps, list):
            self._steps = steps
        elif isinstance(steps, int):
            self._steps = ["red"] * steps
        else:
            raise TypeError("Steps mus be a list (of colors) or int")

        self._dial = QtWidgets.QDial()
        self._bar = _Bar(self._steps)
        self._bar.clickedValue.connect(self._dial.setValue)
        self._dial.valueChanged.connect(self._bar.update_bar)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._bar)
        layout.addWidget(self._dial)

        self.setLayout(layout)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self[item]

        try:
            return getattr(self._dial, item)
        except AttributeError:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")

    def set_color(self, color: str):
        self._bar._steps = [color] * len(self._bar._steps)
        self._bar.update_bar()

    def set_colors(self, colors: [str]):
        self._bar._steps = colors
        self._bar.update_bar()

    def set_background_color(self, color):
        self._bar._background_color = QtGui.QColor(color)
        self._bar.update_bar()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # volume = PowerBar()
    volume = PowerBar(["#a63603", "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2", "#feedde"])
    volume.setNotchesVisible(True)
    volume.show()
    app.exec_()
