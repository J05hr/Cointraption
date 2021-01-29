from PyQt5 import uic
from pathlib import Path


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\trades_window.ui')


class TradesWindow(BaseClass, FormClass):
    def __init__(self):
        super(TradesWindow, self).__init__()
        self.setupUi(self)
