# Coded by Muhammet Kara 2019

import sqlite3

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

connection = sqlite3.connect("webBrowserDB.db")
cursor = connection.cursor()
textFont = QFont("Century Gothic", 16)

class HistoryWindow(QWidget):
    def __init__(self, webBrowser):
        super().__init__()

        titleFont = QFont("Century Gothic", 32)
        titleLbl = QLabel("History")
        titleLbl.setFont(titleFont)

        clearBtn = QPushButton("Clear")
        clearBtn.setFont(textFont)
        clearBtn.clicked.connect(self.clearHistory)

        self.historyList = QListWidget()

        self.fillHistoryList()

        self.historyList.itemClicked.connect(self.goClickedLink)


        layout = QVBoxLayout()
        layout.addWidget(self.historyList)
        layout.addWidget(clearBtn)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.webBrowser = webBrowser

    def fillHistoryList(self):
        data = cursor.execute("SELECT * FROM history")
        siteInfoList = data.fetchall()
        for i in range(len(siteInfoList)-1,-1,-1):
            siteInfo = siteInfoList[i][1] + " - " + siteInfoList[i][3]
            self.historyList.addItem(siteInfo)

    def goClickedLink(self, item):
        siteInfo = item.text()
        visitDate = siteInfo[len(siteInfo)-19:] # veritabanında seçilen sitenin linkini bulmak için ziyaret edilme tarihini arıyoruz
        siteInfoFromDB = cursor.execute("SELECT * FROM history WHERE date = ?", [visitDate])
        url = siteInfoFromDB.fetchall()[0][2]
        self.webBrowser.page.load(QUrl(url)) # open selected url
        self.webBrowser.forwardPageList.clear() # clear forward page list
        self.webBrowser.forwardBtn.setEnabled(0) # disable forward button
        self.close()

    def clearHistory(self):
        self.historyList.clear()
        cursor.execute("DELETE FROM history")
        connection.commit()

