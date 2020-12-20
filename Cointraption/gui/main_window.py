from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton
from pathlib import Path
from Cointraption.gui import manual_classify_window, auto_classify_window, data_view_window


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\main_window.ui')


class MainWindow(BaseClass, FormClass):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.mc_win = manual_classify_window.ManualCWindow()
        self.ac_win = auto_classify_window.AutoCWindow()
        self.dv_win = data_view_window.DataViewWindow()
        self.setupUi(self)

        self.manual_classify_button = self.findChild(QPushButton, 'manualCbutton')
        self.manual_classify_button.clicked.connect(self.mc_button_cb)

        self.auto_classify_button = self.findChild(QPushButton, 'autoCbutton')
        self.auto_classify_button.clicked.connect(self.ac_button_cb)

        self.data_view_button = self.findChild(QPushButton, 'dataViewButton')
        self.data_view_button.clicked.connect(self.dv_button_cb)

    def mc_button_cb(self):
        self.mc_win.show()

    def ac_button_cb(self):
        self.ac_win.show()

    def dv_button_cb(self):
        self.dv_win.show()
