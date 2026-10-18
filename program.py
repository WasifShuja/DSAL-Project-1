from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog
import pandas as pd
import sys
import sorting
import time
sys.setrecursionlimit(30000)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.btnLoadCsv.clicked.connect(self.load_csv_data)
        self.btnSort.clicked.connect(self.handle_sort)
        self.btnBenchmark.clicked.connect(self.handle_benchmark)
        self.btnMultiSort.clicked.connect(self.open_multisort_dialog)
        self.btnSearch.clicked.connect(self.handle_search)
        self.btnResetSearch.clicked.connect(self.handle_reset_search)

        self.df=None
        self.current_data=None


        self.algorithms_meta = {
            "Bubble Sort": {"func": sorting.BubbleSort, "complexity": "O(N^2)", "stability": "Stable"},
            "Selection Sort": {"func": sorting.SelectionSort, "complexity": "O(N^2)", "stability": "Unstable"},
            "Insertion Sort": {"func": sorting.InsertionSort, "complexity": "O(N^2)", "stability": "Stable"},
            "Merge Sort": {"func": sorting.MergeSort, "complexity": "O(N log N)", "stability": "Stable"},
            "Hybrid Merge Sort": {"func": sorting.HybridMergeSort, "complexity": "O(N log N)", "stability": "Stable"},
            "Quick Sort": {"func": sorting.quick_sort, "complexity": "O(N log N) avg", "stability": "Unstable"},
            "Shell Sort": {"func": sorting.shell_sort, "complexity": "O(N log^2 N)", "stability": "Unstable"},
            "Comb Sort": {"func": sorting.comb_sort, "complexity": "O(N^2)", "stability": "Unstable"},
            "Counting Sort": {"func": sorting.counting_sort, "complexity": "O(N + K)", "stability": "Stable"},
            "Radix Sort": {"func": sorting.radix_sort, "complexity": "O(NK)", "stability": "Stable"},
            "Bucket Sort": {"func": sorting.bucket_sort, "complexity": "O(N)", "stability": "Stable"}
        }
        self.comboSortAlgorithm.addItems(list(self.algorithms_meta.keys()))

    def handle_search(self):

        if self.df is None or self.df.empty:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please load a dataset first.")
            return

        col_name = self.comboSearchColumn.currentText()
        filter_rule = self.comboFilterType.currentText()
        query = self.txtSearchQuery.text().strip()
        composite_op = self.comboCompositeOp.currentText() 
        if not query:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a search query.")
            return

        fnmatch_df = lambda target_df: target_df[target_df[col_name].astype(str).str.contains(query, case=False, na=False, regex=False)]
        
        def apply_rule(df_target):
            c = df_target[col_name].astype(str)
            q = query
            if filter_rule == "Contains":
                return df_target[c.str.contains(q, case=False, na=False, regex=False)]
            elif filter_rule == "Starts With":
                return df_target[c.str.lower().str.startswith(q.lower(), na=False)]
            elif filter_rule == "Ends With":
                return df_target[c.str.lower().str.endswith(q.lower(), na=False)]
            elif filter_rule == "Exact Match":
                return df_target[c.str.lower() == q.lower()]
            return df_target


        new_filtered_df = apply_rule(self.df)


        if self.current_data is not None and not self.current_data.equals(self.df):
            if composite_op == "AND":

                indices = self.current_data.index.intersection(new_filtered_df.index)
                result_df = self.df.loc[indices]
            elif composite_op == "OR":

                indices = self.current_data.index.union(new_filtered_df.index)
                result_df = self.df.loc[indices]
            elif composite_op == "NOT":

                indices = self.current_data.index.difference(new_filtered_df.index)
                result_df = self.df.loc[indices]
            else:
                result_df = new_filtered_df
        else:
            result_df = new_filtered_df

        self.current_data = result_df
        self.populate_table(self.current_data)
        self.lblRecordCount.setText(f"Filtered: {len(self.current_data):,} rows")

    def handle_reset_search(self):

        if self.df is None:
            return
            
        self.current_data = self.df.copy()
        self.txtSearchQuery.clear()
        self.populate_table(self.current_data)
        rowCount, colCount = self.df.shape
        self.lblRecordCount.setText(f"Loaded: {rowCount:,} rows, {colCount} columns")

    def open_multisort_dialog(self):
 
        if self.current_data is None or self.current_data.empty:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please load a dataset first.")
            return
            
        dialog = MultiSortDialog(list(self.current_data.columns), self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            cols_to_sort = dialog.get_selected_columns()
            scope = self.comboSortScope.currentText()
            target_df = self.df if scope == "Full Dataset" else self.current_data
            
            data_list = target_df.values.tolist()
            
            col_indices = [list(target_df.columns).index(col) for col in cols_to_sort]
            
            start_time = time.perf_counter()
            
            try:
 
                sorting.MultiLevelMergeSort(data_list, 0, len(data_list) - 1, col_indices)
                
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                
                sorted_df = pd.DataFrame(data_list, columns=target_df.columns)
                if scope == "Full Dataset":
                    self.df = sorted_df
                    self.current_data = sorted_df
                else:
                    self.current_data = sorted_df
                    
                self.populate_table(self.current_data)
                
                self.lblTimeResult.setText(f"{elapsed_ms:.4f} ms")
                self.lblCompResult.setText("N/A")
                self.lblSwapResult.setText("N/A")
                self.lblComplexityResult.setText("O(N log N)")
                self.lblStabilityResult.setText("Stable")
                
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Multi-Sort Error", f"An error occurred: {str(e)}")

    def handle_benchmark(self):
        if self.current_data is None or self.current_data.empty:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please load a dataset first.")
            return

        col_name = self.comboSortColumn.currentText()
        scope = self.comboSortScope.currentText()
        target_df = self.df if scope == "Full Dataset" else self.current_data
        data_list = target_df.values.tolist()
        col_idx = list(target_df.columns).index(col_name)

        dialog = BenchmarkDialog(self.algorithms_meta, data_list, col_idx, col_name, self)
        dialog.exec()
    def handle_sort(self):
        if self.current_data is None or self.current_data.empty:
            print("The current data is none or empty`")
            return

        col_name=self.comboSortColumn.currentText()
        algo_name=self.comboSortAlgorithm.currentText()
        scope=self.comboSortScope.currentText()
        target_df=self.df if scope =="Full Dataset" else self.current_data
        data_list = target_df.values.tolist()
        col_idx = list(target_df.columns).index(col_name)
        

        start_time = time.perf_counter()
        

        algo_func = self.algorithms_meta[algo_name]["func"]
        
        try:
            if algo_name in ["Merge Sort", "Hybrid Merge Sort"]:
                comps, swaps = algo_func(data_list, 0, len(data_list) - 1, col_idx)
            elif algo_name in ["Insertion Sort", "Bubble Sort", "Selection Sort"]:
                comps, swaps = algo_func(data_list, 0, len(data_list) - 1, col_idx)
            else:
                comps, swaps = algo_func(data_list, col_idx)
                
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            sorted_df = pd.DataFrame(data_list, columns=target_df.columns)
            if scope == "Full Dataset":
                self.df = sorted_df
                self.current_data = sorted_df
            else:
                self.current_data = sorted_df
                
            self.populate_table(self.current_data)
            
            self.lblTimeResult.setText(f"{elapsed_ms:.4f} ms")
            self.lblCompResult.setText(f"{comps:,}")
            self.lblSwapResult.setText(f"{swaps:,}")
            self.lblComplexityResult.setText(self.algorithms_meta[algo_name]["complexity"])
            self.lblStabilityResult.setText(self.algorithms_meta[algo_name]["stability"])
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Sorting Error", f"Error during sorting: {str(e)}")
        

    def load_csv_data(self):

        file_open,_=QFileDialog.getOpenFileName(
            self,
            "Select a dataset",
            "",
            "CSV Files (*.csv)"
        )

        if file_open:
            self.df=pd.read_csv(file_open)
            self.current_data = self.df.copy()
            self.messaage="hello"
            rowCount,colCount=self.df.shape
            self.lblRecordCount.setText(f"Loaded: {rowCount} rows, {colCount} columns ")
            self.populate_table()
            self.populate_column_dropdowns()


        pass

    def populate_table(self,df_to_show=None):

        if df_to_show is None:
            df_to_show=self.df
        if df_to_show is None:
            return
        rowCount,colCount=df_to_show.shape
        self.tableWidget.setRowCount(rowCount)
        self.tableWidget.setColumnCount(colCount)
        self.tableWidget.setHorizontalHeaderLabels(list(df_to_show.columns))

        for row in range(rowCount):
            for col in range(colCount):
                val=str(df_to_show.iat[row,col])
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



class BenchmarkDialog(QtWidgets.QDialog):
    """Popup dialog that benchmarks all sorting algorithms and renders a comparison table[cite: 1]."""
    def __init__(self, algorithms_meta, data_list, col_idx, column_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Sorting Algorithm Benchmark (Column: {column_name})")
        self.resize(800, 450)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Info Label
        layout.addWidget(QtWidgets.QLabel("Executing all sorting algorithms on the dataset... Please wait."))
        
        # Results Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Algorithm", "Time (ms)", "Comparisons", "Swaps", "Time Complexity", "Stability"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # Close Button
        btn_close = QtWidgets.QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        # Run benchmarks immediately upon opening
        self.run_benchmarks(algorithms_meta, data_list, col_idx)

    def run_benchmarks(self, algorithms_meta, data_list, col_idx):
        results = []
        
        for algo_name, meta in algorithms_meta.items():
            # Create a fresh independent copy of the dataset for each algorithm
            test_data = [row[:] for row in data_list]
            algo_func = meta["func"]
            
            start_time = time.perf_counter()
            try:
                # Call algorithm based on its expected arguments
                if algo_name in ["Merge Sort", "Hybrid Merge Sort"]:
                    comps, swaps = algo_func(test_data, 0, len(test_data) - 1, col_idx)
                elif algo_name in ["Insertion Sort", "Bubble Sort", "Selection Sort"]:
                    comps, swaps = algo_func(test_data, 0, len(test_data) - 1, col_idx)
                else:
                    comps, swaps = algo_func(test_data, col_idx)
                
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                status_time = f"{elapsed_ms:.4f}"
                status_comps = f"{comps:,}"
                status_swaps = f"{swaps:,}"
            except Exception as e:
                status_time = "Error"
                status_comps = "N/A"
                status_swaps = "N/A"
                
            results.append({
                "name": algo_name,
                "time": status_time,
                "comps": status_comps,
                "swaps": status_swaps,
                "complexity": meta["complexity"],
                "stability": meta["stability"]
            })
            
        # Populate Benchmark Table
        self.table.setRowCount(len(results))
        for row_idx, res in enumerate(results):
            self.table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(res["name"]))
            self.table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(res["time"]))
            self.table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(res["comps"]))
            self.table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(res["swaps"]))
            self.table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(res["complexity"]))
            self.table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(res["stability"]))


class MultiSortDialog(QtWidgets.QDialog):
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Multi-Level Sorting")
        self.resize(380, 220)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Select columns in order of priority:"))
        

        layout.addWidget(QtWidgets.QLabel("1. Primary Sort Column:"))
        self.combo_primary = QtWidgets.QComboBox()
        self.combo_primary.addItems(columns)
        layout.addWidget(self.combo_primary)
        layout.addWidget(QtWidgets.QLabel("2. Secondary Sort Column:"))
        self.combo_secondary = QtWidgets.QComboBox()
        self.combo_secondary.addItem("-- None --")
        self.combo_secondary.addItems(columns)
        layout.addWidget(self.combo_secondary)
        

        btn_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | 
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        
    def get_selected_columns(self):
        cols = [self.combo_primary.currentText()]
        sec = self.combo_secondary.currentText()
        if sec != "-- None --" and sec != cols[0]:
            cols.append(sec)
        return cols

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




  