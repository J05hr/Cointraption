from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from Cointraption.gui import results_dialog
from Cointraption.core import run_classfication
from Cointraption.objs.settings import Settings


rel_dir = str(Path.cwd())
base_data_dir = '\\data'
FormClass, BaseClass = uic.loadUiType(rel_dir + '\\layouts\\predictions_window.ui')


class PredictionsWindow(BaseClass, FormClass):
    def __init__(self):
        super(PredictionsWindow, self).__init__()
        self.browse_dialog = None
        self.results_dialog = None
        self.data_filename = None
        self.training_data = None
        self.testing_data = None
        self.training_model = None
        self.setupUi(self)

        self.current_dir_label = self.findChild(QLabel, 'curDirLabel')
        self.current_dir_label.setText('\\..' + base_data_dir)

        self.c_algo_combo = self.findChild(QComboBox, 'cAlgoComboBox')
        self.train_percent_spin = self.findChild(QSpinBox, 'trainPercentSpin')
        self.sell_below_spin = self.findChild(QDoubleSpinBox, 'sellBelowSpin')
        self.buy_above_spin = self.findChild(QDoubleSpinBox, 'buyAboveSpin')
        self.moving_avg_spin = self.findChild(QSpinBox, 'movingAvgSpin')

        self.browse_button = self.findChild(QPushButton, 'browseButton')
        self.browse_button.clicked.connect(self.browse_button_cb)

        self.run_c_button = self.findChild(QPushButton, 'runCButton')
        self.run_c_button.clicked.connect(self.run_c_button_cb)

        self.data_list_widget = self.findChild(QListWidget, 'dataListWidget')
        self.data_list_widget.clicked.connect(self.data_selected_cb)
        self.data_dir = rel_dir + base_data_dir
        self.update_list_view()

    def update_list_view(self):
        if self.data_dir:
            pobj = Path(self.data_dir)
            for fname in pobj.iterdir():
                self.data_list_widget.addItem(str(fname.name))

    def browse_button_cb(self):
        self.data_list_widget.clear()
        self.browse_dialog = QFileDialog()
        self.data_dir = self.browse_dialog.getExistingDirectory(self, "Choose Data Directory", self.data_dir, self.browse_dialog.ShowDirsOnly)
        self.update_list_view()

    def run_c_button_cb(self):
        self.run_c_button.setEnabled(False)
        self.run_c_button.setText("Running...")
        outcome_range = (-1 * self.sell_below_spin.value(), self.buy_above_spin.value())
        settings = Settings(self.data_filename, self.moving_avg_spin.value(), outcome_range,
                            self.train_percent_spin.value(), self.c_algo_combo.currentText())
        res = run_classfication.run(settings)
        self.results_dialog = results_dialog.ResultsDialog(res)
        self.results_dialog.show()
        self.results_dialog.finished.connect(self.results_dialog_finished_cb)

    def results_dialog_finished_cb(self):
        self.run_c_button.setEnabled(True)
        self.run_c_button.setText("Run Classification")

    def data_selected_cb(self):
        self.data_filename = self.data_dir + '\\' + self.data_list_widget.selectedItems()[0].text()
        self.run_c_button.setEnabled(True)
