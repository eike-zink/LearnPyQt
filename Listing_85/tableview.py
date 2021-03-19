# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import QSize, Qt

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView

db = QSqlDatabase("QSQLITE")
# ACHTUNG: Der Aufruf des Programms in VSCode hat einen Einfluss auf
# das Verzeichnis, in dem die SQLite-Datenbank gesucht wird
db.setDatabaseName("./Database/chinook.sqlite")
db.open()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = QSqlTableModel(db=db)
        self.model.setTable('tracks')
        self.model.select()

        self.table = QTableView()
        self.table.setModel(self.model)

        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(self.table)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
