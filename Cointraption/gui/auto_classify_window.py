from PyQt5 import uic
from pathlib import Path


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\auto__classify_window.ui')


class AutoCWindow(BaseClass, FormClass):
    def __init__(self):
        super(AutoCWindow, self).__init__()
        self.setupUi(self)
