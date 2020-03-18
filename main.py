# Coded by Muhammet Kara 2019

import datetime
import sys

from PyQt5 import QtWebEngineWidgets
from HistoryWindow import *
from backList import *

textFont = QFont("Century Gothic", 16)
buttonFont = QFont("Century Gothic", 24)
urlBarFont = QFont("Century Gothic", 16)





class WebBrowser(QWidget):
    def __init__(self):
        super().__init__()

        self.connection = sqlite3.connect("webBrowserDB.db")
        self.cursor = self.connection.cursor()

        # create history table
        cursor.execute("""CREATE TABLE IF NOT EXISTS "history" (
                   "id"	INTEGER,
                   "title"	TEXT,
                   "url"	TEXT,
                   "date"	TEXT,
               	PRIMARY KEY("id")
               	)""")


        verticalLayout = QVBoxLayout()

        self.visitedPageList = []
        self.forwardPageList = []

        self.setWindowTitle("Web Browser")

        self.backBtn = QPushButton()
        self.backBtn.setIcon(QIcon("./back.png"))
        self.backBtn.setIconSize(QSize(32, 32))
        self.backBtn.setStyleSheet("background: transparent;")
        self.backBtn.setEnabled(0) # Back button is disabled initially
        self.backBtn.clicked.connect(self.backBtnClicked)

        self.backListBtn = QPushButton("|")
        self.backListBtn.setFixedSize(10, 40)
        self.backListBtn.setEnabled(0) # button is disabled initially
        self.backListBtn.clicked.connect(self.showBackList)

        self.forwardBtn = QPushButton()
        self.forwardBtn.setIcon(QIcon("./forward.png"))
        self.forwardBtn.setIconSize(QSize(32, 32))
        self.forwardBtn.setStyleSheet("background: transparent;")
        self.forwardBtn.setEnabled(0) # Forward button is disabled initially
        self.forwardBtn.clicked.connect(self.forwardBtnClicked)

        self.reloadBtn = QPushButton()
        self.reloadBtn.setIcon(QIcon("./reload.png"))
        self.reloadBtn.setIconSize(QSize(32, 32))
        self.reloadBtn.setStyleSheet("background: transparent;")
        self.reloadBtn.setEnabled(0)# reload button is disabled initially
        self.reloadBtn.clicked.connect(self.reloadPage)

        self.urlBar = QLineEdit()
        self.urlBar.setAlignment(Qt.AlignLeft)
        self.urlBar.setFont(urlBarFont)
        self.urlBar.setPlaceholderText("Enter a url")
        self.urlBar.returnPressed.connect(self.goUrlMethod)

        goBtn = QPushButton()
        goBtn.setIcon(QIcon("./go2.png"))
        goBtn.setIconSize(QSize(32, 32))
        goBtn.setStyleSheet("background: transparent;")
        goBtn.clicked.connect(self.goUrlMethod)

        historyBtn = QPushButton("H")
        historyBtn.clicked.connect(self.openHistory)

        urlBarLayout = QHBoxLayout()

        urlBarLayout.addWidget(self.backBtn)
        urlBarLayout.addWidget(self.backListBtn)
        urlBarLayout.addWidget(self.forwardBtn)
        urlBarLayout.addWidget(self.reloadBtn)
        urlBarLayout.addWidget(self.urlBar)
        urlBarLayout.addWidget(goBtn)
        urlBarLayout.addWidget(historyBtn)

        self.page = QtWebEngineWidgets.QWebEngineView()
        self.page.loadFinished.connect(self.add_new_url_to_visited_page_list)
        self.page.loadFinished.connect(self.updateUrlBarTextAndTitle)
        self.page.loadFinished.connect(self.updateHistory)
        self.page.loadFinished.connect(self.setReloadBtnEnabled)

        verticalLayout.addLayout(urlBarLayout)
        verticalLayout.addWidget(self.page)

        self.setLayout(verticalLayout)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.showMaximized()

    def goUrlMethod(self):
        url = self.urlBar.text()
        if "http" in url:
            self.page.load(QUrl(url))
        else:
            self.page.load(QUrl("https://"+url))


        self.forwardPageList.clear()
        self.forwardBtn.setEnabled(0)

    def backBtnClicked(self):
        # First, adding current page's url to forward page list
        currentPageUrl = self.visitedPageList[-1][1]
        self.forwardPageList.append(currentPageUrl)

        previousPageUrl = self.visitedPageList[-2][1]

        self.visitedPageList.pop(-1)
        self.visitedPageList.pop(-1)

        self.page.load(QUrl(previousPageUrl))

        if len(self.visitedPageList) < 2:# if there is only 1 url remains in the list, set back button disabled
            self.backBtn.setEnabled(0)
            self.backListBtn.setEnabled(0)

        if len(self.forwardPageList) > 0:# if there is an url in forward page list, set forward button enabled
            self.forwardBtn.setEnabled(1)

    def showBackList(self):
        self.backListWindow = BackList(self)
        self.backListWindow.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint |Qt.FramelessWindowHint)
        self.backListWindow.setGeometry(65, 87, 300, 200)
        self.backListWindow.show()

    def forwardBtnClicked(self):
        targetUrl = self.forwardPageList[-1]
        self.page.load(QUrl(targetUrl))
        self.forwardPageList.pop(-1)

        if len(self.forwardPageList) == 0:# if there is no url in forward page list, set forward button disabled
            self.forwardBtn.setEnabled(0)

    def reloadPage(self):

        self.reloadBtn.setEnabled(0)

        currentPageUrl = self.visitedPageList[-1]
        self.visitedPageList.pop(-1) # Remove last url because it is going to add the same again.
        self.page.load(QUrl(currentPageUrl))
        self.page.loadFinished.connect(self.setReloadBtnEnabled)

    def setReloadBtnEnabled(self):
        self.reloadBtn.setEnabled(1)


    def add_new_url_to_visited_page_list(self):
        url = str(self.page.url())
        url = url[19:len(url) - 2]
        siteName = self.page.title()
        siteInfo = (siteName, url)
        for i in self.visitedPageList:
            if i == siteInfo:
                self.visitedPageList.remove(i)
        self.visitedPageList.append(siteInfo)

        if len(self.visitedPageList) > 1: #if there is two urls in the list, set back button enabled
            self.backBtn.setEnabled(1)
            self.backListBtn.setEnabled(1)

    def updateUrlBarTextAndTitle(self):
        url = str(self.page.url())
        url = url[19:len(url) - 2]
        self.urlBar.setText(url)
        self.setWindowTitle(self.page.title())


    def getForwardPageList(self):
        return self.forwardPageList

    def getVisitedPageList(self):
        return self.visitedPageList

    def updateHistory(self):
        title = self.page.title()
        url = str(self.page.url())
        url = url[19:len(url) - 2]
        hour = datetime.datetime.now().strftime("%X")
        day = datetime.datetime.now().strftime("%x")
        date = hour + " - " + day
        #eğer url geçmişte varsa öncekini silip yenisini en sona ekliyoruz
        data = self.cursor.execute("SELECT * FROM history")
        siteInfoList = data.fetchall()

        for i in range(len(siteInfoList)):
            if url == siteInfoList[i][2]: #url ler eşleşirse eski urlyi sil
                self.cursor.execute("DELETE FROM history WHERE url = ?", [url])

        self.cursor.execute("INSERT INTO history (title,url,date) VALUES (?,?,?)", (title,url,date))
        self.connection.commit()

    def openHistory(self):
        self.historyWindow = HistoryWindow(self)
        self.historyWindow.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.historyWindow.setGeometry(self.page.frameGeometry().width()-500-10, 87, 500, 500)
        self.historyWindow.show()




app = QApplication(sys.argv)
browser = WebBrowser()
sys.exit(app.exec_())