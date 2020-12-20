from PyQt5.QtWidgets import QApplication
from Cointraption.gui import main_window
from Cointraption.utils import utils
from pathlib import Path
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stylePath = str(Path.cwd()) + '\\layouts\\stylesheets\\light.qss'
    utils.toggle_stylesheet(stylePath)
    win = main_window.MainWindow()
    win.show()
    sys.exit(app.exec())


