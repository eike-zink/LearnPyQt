import sys

from PyQt5.QtSql import QSqlDatabase, QSqlRelation, QSqlRelationalTableModel, QSqlRelationalDelegate
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QLineEdit, QWidget

db = QSqlDatabase("QSQLITE")
db.setDatabaseName("./Database/chinook.sqlite")
db.open()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = QSqlRelationalTableModel(db=db)
        self.model.setTable("tracks")
        self.model.setRelation(2, QSqlRelation("Albums", "AlbumId", "Title"))
        self.model.setRelation(3, QSqlRelation("Media_Types", "MediaTypeId", "Name"))
        self.model.setRelation(4, QSqlRelation("Genres", "GenreId", "Name"))
        # Column Title
        self.model.setHeaderData(0, Qt.Horizontal, "Track (ID)")
        self.model.setHeaderData(2, Qt.Horizontal, "Album")
        self.model.setHeaderData(3, Qt.Horizontal, "Media Type")
        self.model.setHeaderData(4, Qt.Horizontal, "Genre")

        self.model.select()

        self.search = QLineEdit()
        self.search.textChanged.connect(self.update_filter)

        self.table = QTableView()
        self.table.setModel(self.model)
        delegate = QSqlRelationalDelegate(self.table)
        self.table.setItemDelegate(delegate)

        layout = QVBoxLayout()        
        layout.addWidget(self.search)
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        
        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(container)

    def update_filter(self, s):
        filter_value = 'tracks.name like "%{}%"'.format(s)
        self.model.setFilter(filter_value)

app = QApplication(sys.argv)

windows = MainWindow()
windows.show()

app.exec_()