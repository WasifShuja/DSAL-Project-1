from PyQt6 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.btnLoadCsv.clicked.connect(self.load_csv_data)

    def load_csv_data(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




  