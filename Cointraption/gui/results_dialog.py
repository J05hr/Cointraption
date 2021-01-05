from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\results_dialog.ui')


class ResultsDialog(BaseClass, FormClass):
    def __init__(self, results):
        super(ResultsDialog, self).__init__()
        self.results = results
        self.setupUi(self)

        self.outcomeRangeLabel = self.findChild(QLabel, 'outcomeRangeLabel')
        self.outcomeRangeLabel.setText(str(results.outcome_range))

        self.trainPercentLabel = self.findChild(QLabel, 'trainPercentLabel')
        self.trainPercentLabel.setText(str(results.train_percent) + '%')

        self.movingAvgLabel = self.findChild(QLabel, 'movingAvgLabel')
        self.movingAvgLabel.setText(str(results.moving_avg) + ' day(s)')

        self.predAccurLabel = self.findChild(QLabel, 'predAccurLabel')
        self.predAccurLabel.setText(str(round(results.p_accuracy, 2)) + '%')

        self.profitLabel = self.findChild(QLabel, 'profitLabel')
        self.profitLabel.setText('$' + str(round(results.profit, 2)))

        self.totalBuyInLabel = self.findChild(QLabel, 'totalBuyInLabel')
        self.totalBuyInLabel.setText('$' + str(round(results.buy_in, 2)))

        self.profitOverControl = self.findChild(QLabel, 'profitOverControl')
        self.profitOverControl.setText('$' + str(round(results.profit_over_control, 2)))

        self.finalPrediction = self.findChild(QLabel, 'finalPrediction')
        self.finalPrediction.setText('buy: ' + str(round(results.final_prediction[0] * 100, 2)) + '%, ' +
                                     'sell: ' + str(round(results.final_prediction[1] * 100, 2)) + '%, ' +
                                     'hold: ' + str(round(results.final_prediction[2] * 100, 2)) + '%')

        self.resultsTableWidget = self.findChild(QTableWidget, 'resultsTableWidget')
        self.updateTableView()

    def updateTableView(self):
        if self.results:
            self.resultsTableWidget.setRowCount(len(self.results.classification_list))
            self.resultsTableWidget.setColumnCount(5)
            self.resultsTableWidget.setItem(0, 0, QTableWidgetItem("Date"))
            self.resultsTableWidget.setItem(0, 1, QTableWidgetItem("P(buy|data)"))
            self.resultsTableWidget.setItem(0, 2, QTableWidgetItem("P(sell|data)"))
            self.resultsTableWidget.setItem(0, 3, QTableWidgetItem("P(hold|data)"))
            self.resultsTableWidget.setItem(0, 4, QTableWidgetItem("Test Results"))
            for resIdx in range(len(self.results.classification_list)):
                self.resultsTableWidget.setItem(resIdx + 1, 0, QTableWidgetItem(self.results.classification_list[resIdx][0]))
                self.resultsTableWidget.setItem(resIdx + 1, 1, QTableWidgetItem(str(round(self.results.classification_list[resIdx][1] * 100, 2)) + '%'))
                self.resultsTableWidget.setItem(resIdx + 1, 2, QTableWidgetItem(str(round(self.results.classification_list[resIdx][2] * 100, 2)) + '%'))
                self.resultsTableWidget.setItem(resIdx + 1, 3, QTableWidgetItem(str(round(self.results.classification_list[resIdx][3] * 100, 2)) + '%'))
                self.resultsTableWidget.setItem(resIdx + 1, 4, QTableWidgetItem(self.results.classification_list[resIdx][4]))
