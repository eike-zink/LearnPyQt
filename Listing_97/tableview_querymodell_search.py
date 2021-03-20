import sys

from PyQt5.QtCore import QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QTableView, QWidget
)

db = QSqlDatabase("QSQLITE")
db.setDatabaseName("../Database/chinook.sqlite")
db.open()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.model = QSqlQueryModel()
        self.query = QSqlQuery(db=db)
        self.query.prepare(
            """
            select tracks.name, tracks.composer, albums.title
            from   tracks 
                   join albums using (albumid)
            where  tracks.name like '%'||:track_name||'%'
                   and tracks.composer like '%'||:track_composer||'%'
                   and albums.title like '%'||:album_title||'%'
            """
        )

        self.table = QTableView()
        self.table.setModel(self.model)

        self.track = QLineEdit()
        self.track.setPlaceholderText("Track name...")
        self.track.textChanged.connect(self.execute_query)

        self.composer = QLineEdit()
        self.composer.setPlaceholderText("Artist name...")
        self.composer.textChanged.connect(self.execute_query)

        self.album = QLineEdit()
        self.album.setPlaceholderText("Album name...")
        self.album.textChanged.connect(self.execute_query)

        self.execute_query()

        layout_search = QHBoxLayout()
        layout_search.addWidget(self.track)
        layout_search.addWidget(self.composer)
        layout_search.addWidget(self.album)

        layout_view = QVBoxLayout()
        layout_view.addLayout(layout_search)
        layout_view.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout_view)

        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(container)

    def execute_query(self):
        # Get the text from the widgets
        track_name = self.track.text()
        track_composer = self.composer.text()
        album_title = self.album.text()

        # Bind Variable
        self.query.bindValue(":track_name", track_name)
        self.query.bindValue(":track_composer", track_composer)
        self.query.bindValue(":album_title", album_title)

        self.query.exec_()
        self.model.setQuery(self.query)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
