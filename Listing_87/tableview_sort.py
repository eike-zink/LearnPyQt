import sys

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView

db = QSqlDatabase("QSQLITE")
db.setDatabaseName("./Database/chinook.sqlite")
db.open()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = QSqlTableModel(db=db)
        self.model.setTable("tracks")
        # Column Title
        column_titles = {
            "TrackId": "Track (ID)",
            "AlbumId": "Album (ID)",
            "MediaTypeId": "Media Type (ID)",
            "GenreId": "Genre (ID)"
        }
        for column_name, column_title in column_titles.items():
            idx = self.model.fieldIndex(column_name)
            self.model.setHeaderData(idx, Qt.Horizontal, column_title)
            
        # Sort Table
        idx = self.model.fieldIndex("Milliseconds")
        self.model.setSort(idx, Qt.DescendingOrder)
        self.model.select()

        self.table = QTableView()
        self.table.setModel(self.model)

        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(self.table)

app = QApplication(sys.argv)

windows = MainWindow()
windows.show()

app.exec_()