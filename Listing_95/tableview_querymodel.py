import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView

db = QSqlDatabase("QSQLITE")
db.setDatabaseName("./Database/chinook.sqlite")
db.open()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = QSqlQueryModel()

        query = QSqlQuery(db=db)
        query.prepare(
            """
            select 
                tracks.name, 
                tracks.composer, 
                albums.title as Album,
                genres.name as Genres
            from 
                tracks
                inner join albums using (albumid)
                inner join genres using (genreid)
            where
                albums.title like ('%'||:album_title||'%')
            """)
        query.bindValue(":album_title", "Ones")
        query.exec()

        self.model.setQuery(query)

        self.table = QTableView()
        self.table.setModel(self.model)

        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(self.table)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()