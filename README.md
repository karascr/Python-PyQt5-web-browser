# Python-PyQt5-web-browser
A web browser coded with PyQt5 for my school project
PyQt5 library used in this project.
For viewing web sites, QtWebEngineWidgets form PyQt5 is used .
SQLite is used for storing history list in database, you can use DB Browser for SQLite (free) program for displaying database. [Download link](https://sqlitebrowser.org/dl/)
## .py files
### webBrowser.py
webBrowser.py is main code that contains web browser window.
![image-of-web-browser](https://muhammetkara.net/wp-content/uploads/2020/01/WebBrowser.png)
### baclist.py
backlist.py is a class that creates a window when back button is clicked. This window shows sites you have visited and allows to open the clicked one.
![image-of-backlist](https://muhammetkara.net/wp-content/uploads/2020/01/backlist.png)
### historyWindow.py
When clicked history botton (H), historyWindow class creates a window contains a QListWidget that contains history list.
![image-of-history](https://muhammetkara.net/wp-content/uploads/2020/01/history.png)
