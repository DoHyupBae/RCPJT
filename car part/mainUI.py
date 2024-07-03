# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QShortcut)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 540)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.leftButton = QPushButton(self.centralwidget)
        self.leftButton.setObjectName(u"leftButton")
        self.leftButton.setGeometry(QRect(160, 380, 75, 51))
        self.logText = QPlainTextEdit(self.centralwidget)
        self.logText.setObjectName(u"logText")
        self.logText.setGeometry(QRect(70, 40, 441, 261))
        font = QFont()
        font.setFamilies([u"Consolas"])
        self.logText.setFont(font)
        self.sensingText = QPlainTextEdit(self.centralwidget)
        self.sensingText.setObjectName(u"sensingText")
        self.sensingText.setGeometry(QRect(530, 40, 441, 191))
        self.sensingText.setFont(font)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 10, 121, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(530, 10, 181, 16))
        self.midButton = QPushButton(self.centralwidget)
        self.midButton.setObjectName(u"midButton")
        self.midButton.setGeometry(QRect(250, 380, 75, 51))
        self.rightButton = QPushButton(self.centralwidget)
        self.rightButton.setObjectName(u"rightButton")
        self.rightButton.setGeometry(QRect(340, 380, 75, 51))
        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName(u"backButton")
        self.backButton.setGeometry(QRect(250, 440, 75, 51))
        self.goButton = QPushButton(self.centralwidget)
        self.goButton.setObjectName(u"goButton")
        self.goButton.setGeometry(QRect(250, 320, 75, 51))
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(790, 370, 111, 71))
        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(650, 370, 111, 71))
        self.statusText = QPlainTextEdit(self.centralwidget)
        self.statusText.setObjectName(u"statusText")
        self.statusText.setGeometry(QRect(530, 260, 441, 41))
        font1 = QFont()
        font1.setPointSize(14)
        self.statusText.setFont(font1)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(530, 235, 131, 21))
        font2 = QFont()
        font2.setPointSize(12)
        self.label_3.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.startButton.clicked.connect(MainWindow.start)
        self.stopButton.clicked.connect(MainWindow.stop)
        self.rightButton.clicked.connect(MainWindow.right)
        self.goButton.clicked.connect(MainWindow.go)
        self.midButton.clicked.connect(MainWindow.mid)
        self.backButton.clicked.connect(MainWindow.back)
        self.leftButton.clicked.connect(MainWindow.left)

        go_shortcut = QShortcut(QKeySequence.fromString('w'), self)
        go_shortcut.activated.connect(MainWindow.go)
        left_shortcut = QShortcut(QKeySequence.fromString('a'), self)
        left_shortcut.activated.connect(MainWindow.left)
        right_shortcut = QShortcut(QKeySequence.fromString('d'), self)
        right_shortcut.activated.connect(MainWindow.right)
        stop_shortcut = QShortcut(QKeySequence.fromString('space'), self)
        stop_shortcut.activated.connect(MainWindow.stop)
        mid_shortcut = QShortcut(QKeySequence.fromString('q'), self)
        mid_shortcut.activated.connect(MainWindow.mid)
        back_shortcut = QShortcut(QKeySequence.fromString('s'), self)
        back_shortcut.activated.connect(MainWindow.back)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.leftButton.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"command Table", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"sensing Table", None))
        self.midButton.setText(QCoreApplication.translate("MainWindow", u"Mid", None))
        self.rightButton.setText(QCoreApplication.translate("MainWindow", u"Right", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.goButton.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"driving status", None))
    # retranslateUi

