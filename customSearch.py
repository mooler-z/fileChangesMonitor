import sys, os, time, sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from customThread import SearchQueue
import subprocess

video_extensions = ['.264', '.3g2', '.3gp', '.arf', '.asf', '.asx', '.avi', '.bik', '.dash', 
'.dat', '.dvr', '.flv', '.h264', '.m2t', '.m2ts', '.m4v', '.mkv', '.mod', '.mov', '.mp4',
 '.mpeg', '.mpg', '.mts', '.ogv', '.proproj', '.rec', '.rmvb', '.swf', '.tod', '.tp', '.ts',
'.vob', '.webm', '.wlmp', '.wmv']

audio_extensions = ['.pcm', '.wav', '.aiff', '.mp3', '.aac', '.ogg', 
'.wma', '.flac', '.alac', '.cda', '.mid', '.midi', '.wpl', '.m4a']

picture_extensions = ['.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg',
 '.png', '.ps', '.psd', '.svg', '.tif', '.tiff']

word_extensions = ['.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt', 
'.wks', '.wps', '.wpd', '.ods', '.xlr', '.xls', '.xlsx', '.key', '.odp', 
'.pps', '.ppt', '.pptx', '.epub', '.log']

pl_extensions = ['.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift',
 '.vb', '.css', '.html', '.htm', '.js', '.jsp', '.php', '.py', '.rss', '.rb',
  '.xhtml', '.db', '.sql', '.xml', '.jar', '.md', '.cfg', '.csv', '.json']

zip_extensions = ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.gz', '.z', '.zip', '.xz']

general_extensions = {
    "Pictures": [picture_extensions, "images/image-x-generic.svg",],
    "Videos": [video_extensions, "images/video-x-theora+ogg.svg",],
    "Audios": [audio_extensions, "images/audio-x-wav.svg",],
    "ProgLangs": [pl_extensions, "images/text-x-python.svg",],
    "Compressed": [zip_extensions, "images/application-x-tar.svg",],
    "Words": [word_extensions, "images/application-pdf.svg",],
}

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def openItem(self, item):
        item = item.text()
        os.system("xdg-open '{}'".format(item))
        
    def searchResult(self):
        if self.lineEdit.text() and len(self.lineEdit.text())>1:
            self.queue = SearchQueue(self.lineEdit.text())
            self.queue.updateListSignal.connect(self.updateListWidget)
            self.queue.start()
        
    def updateListWidget(self, searchItem):
        self.listWidget.clear()
        count = 0
        for i in searchItem:
            if os.path.exists(os.path.join(i[1], i[0])):
                item = QtWidgets.QListWidgetItem(f"{i[0]}\n{i[1]}")
                if i[3]:
                    item.setIcon(QtGui.QIcon("images/folder.svg"))
                else:
                    for k, j in general_extensions.items():
                        if os.path.splitext(i[0])[1].lower() in j[0]:
                            item.setIcon(QtGui.QIcon(j[1]))
                item.setWhatsThis(os.path.join(i[1], i[0]))
                self.listWidget.addItem(item)
                count += 1
        if count == 1:
            self.label.setText("Found - {} item".format(count))
        else:
            self.label.setText("Found - {} items".format(count))
            
    def activeItem(self, item):
        # # print("clicked")
        abspath = item.text().split("\n")
        self.activatedItem = os.path.join(abspath[1], abspath[0])
        self.triggeredAction()
    
    def triggeredAction(self):
        os.system('xdg-open "{}" &'.format(self.activatedItem))
        
    def contextMenuEvent(self, event):
        action = QtWidgets.QAction("Open")
        action.triggered.connect(self.triggeredAction)
        context_menu = QtWidgets.QMenu()
        context_menu.addAction(action)
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: #EAE4DB;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("QLineEdit {\n"
"    background-color: #EAE4DB;\n"
"    padding: 14px;\n"
"    font-size: 14px;"
"}")
        self.lineEdit.editingFinished.connect(self.searchResult)
        self.refresh = QtWidgets.QPushButton(self.centralwidget)
        self.refresh.setText("Refresh")
        self.refresh.setStyleSheet("QPushButton {\n"
"    padding: 16px 14;\n"
"    font-size: 16px;"
"}")
        self.refresh.clicked.connect(self.updateIndex)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addWidget(self.refresh)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        # self.listWidget.itemDoubleClicked.connect(self.doubleClicked)
        self.listWidget.itemClicked.connect(self.activeItem)
        # self.listWidget.itemDoubleClicked.connect(self.activeItem)
        self.verticalLayout.addWidget(self.listWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "-"))
        
    def updateIndex(self):
        os.system("python updateIndexV2.py music_22.db pic &")

if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)
   window = Ui_MainWindow()
   window.show()
   app.exec_()
