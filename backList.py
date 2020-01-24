# Coded by Muhammet Kara 2019

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *

class BackList(QWidget):
    def __init__(self, webBrowser):
        super().__init__()
        self.visitedPageList = webBrowser.getVisitedPageList()

        self.backList = QListWidget()

        self.loadBackList()

        self.backList.itemClicked.connect(self.goClickedLink)


        layout = QHBoxLayout()
        layout.addWidget(self.backList)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.webBrowser = webBrowser

    def loadBackList(self):
        if len(self.visitedPageList) > 0:
            for i in range(len(self.visitedPageList) - 1,-1,-1):
                siteTitle = self.visitedPageList[i][0]
                siteUrl = self.visitedPageList[i][1]
                self.backList.addItem(siteTitle+" - "+ siteUrl)

    def goClickedLink(self, item):
        siteInfo = item.text()
        urlStartingIndex = siteInfo.find("http")
        url = siteInfo[urlStartingIndex:]
        self.webBrowser.page.load(QUrl(url)) # open selected url
        self.webBrowser.forwardPageList.clear() # clear forward page list
        self.webBrowser.forwardBtn.setEnabled(0) # disable forward button
        self.close()

