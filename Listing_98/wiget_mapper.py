import sys

from PyQt5.QtCore import QSize
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFormLayout, QLabel, QSpinBox, QPushButton,
    QLineEdit, QComboBox, QDoubleSpinBox, QDataWidgetMapper, QWidget,
    QHBoxLayout, QVBoxLayout
)

db = QSqlDatabase("QSQLITE")
db.setDatabaseName("../Database/chinook.sqlite")
db.open()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.track_id = QSpinBox()
        self.track_id.setDisabled(True)
        self.name = QLineEdit()
        self.composer = QLineEdit()
        self.album = QComboBox()
        self.media_type = QComboBox()
        self.genre = QComboBox()

        self.milliseconds = QSpinBox()
        self.milliseconds.setRange(0, 2147483647)
        self.milliseconds.setSingleStep(1)

        self.bytes = QSpinBox()
        self.bytes.setRange(0, 2147483647)
        self.bytes.setSingleStep(1)

        self.unit_price = QDoubleSpinBox()
        self.unit_price.setRange(0, 999)
        self.unit_price.setSingleStep(0.01)
        self.unit_price.setPrefix("$")

        form = QFormLayout()
        form.addRow(QLabel("Track ID"), self.track_id)
        form.addRow(QLabel("Track name"), self.name)
        form.addRow(QLabel("Composer"), self.composer)
        form.addRow(QLabel("Album"), self.album)
        form.addRow(QLabel("Milliseconds"), self.milliseconds)
        form.addRow(QLabel("Bytes"), self.bytes)
        form.addRow(QLabel("Unit Price"), self.unit_price)

        self.model = QSqlTableModel(db=db)
        self.model.setTable("tracks")

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.track_id, 0)
        self.mapper.addMapping(self.name, 1)
        self.mapper.addMapping(self.composer, 5)
        self.mapper.addMapping(self.milliseconds, 6)
        self.mapper.addMapping(self.bytes, 7)
        self.mapper.addMapping(self.unit_price, 8)

        previous_row = QPushButton("Previous")
        previous_row.clicked.connect(self.mapper.toPrevious)
        next_row = QPushButton("Next")
        next_row.clicked.connect(self.mapper.toNext)
        save_row = QPushButton("Save")
        save_row.clicked.connect(self.mapper.submit)
        controls = QHBoxLayout()
        controls.addWidget(previous_row)
        controls.addWidget(save_row)
        controls.addWidget(next_row)

        self.model.select()
        self.mapper.toFirst()

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(controls)

        widget = QWidget()
        widget.setLayout(layout)
        self.setMinimumSize(QSize(400, 400))
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
