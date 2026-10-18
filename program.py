from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog
import pandas as pd
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.btnLoadCsv.clicked.connect(self.load_csv_data)

    def load_csv_data(self):

        file_open,_=QFileDialog.getOpenFileName(
            self,
            "Select a dataset",
            "",
            "CSV Files (*.csv)"
        )

        if file_open:
            self.df=pd.read_csv(file_open)
            self.messaage="hello"
            rowCount,colCount=self.df.shape
            self.lblRecordCount.setText(f"Loaded: {rowCount} rows, {colCount} columns ")
            self.populate_table()
            self.populate_column_dropdowns()


        pass

    def populate_table(self):
        if self.df is None:
            return
        rowCount,colCount=self.df.shape
        self.tableWidget.setRowCount(rowCount)
        self.tableWidget.setColumnCount(colCount)
        self.tableWidget.setHorizontalHeaderLabels(list(self.df.columns))

        for row in range(rowCount):
            for col in range(colCount):
                val=str(self.df.iat[row,col])
                self.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(val))

        self.tableWidget.resizeColumnsToContents()

        pass

    def populate_column_dropdowns(self):
        if self.df is None:
            return

        columns=list(self.df.columns)
        self.comboSearchColumn.clear()
        self.comboSearchColumn.addItems(columns)

        self.comboSortColumn.clear()
        self.comboSortColumn.addItems(columns)
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




  