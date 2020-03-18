# Python-PyQt5-web-browser
A web browser coded with PyQt5 for my school project
PyQt5 library used in this project.
For viewing web sites, QtWebEngineWidgets form PyQt5 is used.
SQLite is used for storing the history list in the database, you can use the DB Browser for SQLite (free) program for displaying database. [Download link](https://sqlitebrowser.org/dl/)
## Installation
Create a new project and copy files into this project.

## .py files
### webBrowser.py
webBrowser.py is the main code that contains a web browser window.
![image-of-web-browser](https://muhammetkara.net/wp-content/uploads/2020/01/WebBrowser.png)
### baclist.py
backlist.py is a class that creates a window when the back button is clicked. This window shows sites you have visited and allows you to open the clicked one.
![image-of-backlist](https://muhammetkara.net/wp-content/uploads/2020/01/backlist.png)
### historyWindow.py
When clicked history button (H), history window class creates a window contains a QListWidget that contains a history list.
![image-of-history](https://muhammetkara.net/wp-content/uploads/2020/01/history.png)
