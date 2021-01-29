from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton
from pathlib import Path
from Cointraption.gui import predictions_window, trades_window, data_view_window


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\main_window.ui')


class MainWindow(BaseClass, FormClass):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.pr_win = predictions_window.PredictionsWindow()
        self.tr_win = trades_window.TradesWindow()
        self.dv_win = data_view_window.DataViewWindow()
        self.setupUi(self)

        self.predictions_button = self.findChild(QPushButton, 'predictionsButton')
        self.predictions_button.clicked.connect(self.pr_button_cb)

        self.trades_button = self.findChild(QPushButton, 'tradesButton')
        self.trades_button.clicked.connect(self.tr_button_cb)

        self.data_view_button = self.findChild(QPushButton, 'dataViewButton')
        self.data_view_button.clicked.connect(self.dv_button_cb)

    def pr_button_cb(self):
        self.pr_win.show()

    def tr_button_cb(self):
        self.tr_win.show()

    def dv_button_cb(self):
        self.dv_win.show()
