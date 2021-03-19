import sys

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QLineEdit, QWidget

db = QSqlDatabase("QSQLITE")
db.setDatabaseName("./Database/chinook.sqlite")
db.open()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = QSqlTableModel(db=db)
        self.model.setTable("tracks")
        # Column Title
        self.model.setHeaderData(0, Qt.Horizontal, "Track (ID)")
        self.model.setHeaderData(2, Qt.Horizontal, "Album (ID)")
        self.model.setHeaderData(3, Qt.Horizontal, "Media Type (ID)")
        self.model.setHeaderData(4, Qt.Horizontal, "Genre (ID)")

        self.model.select()

        self.search = QLineEdit()
        self.search.textChanged.connect(self.update_filter)

        self.table = QTableView()
        self.table.setModel(self.model)

        layout = QVBoxLayout()        
        layout.addWidget(self.search)
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        
        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(container)

    def update_filter(self, s):
        filter_value = 'name like "%{}%"'.format(s)
        self.model.setFilter(filter_value)

app = QApplication(sys.argv)

windows = MainWindow()
windows.show()

app.exec_()