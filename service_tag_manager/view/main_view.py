from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        loaded_ui = uic.loadUi("view/ui_main.ui")  # Carrega o widget
        self.setCentralWidget(loaded_ui)  # Define como widget central
        self.setWindowTitle("Service Tag Manager")

        # Agora precisamos acessar os elementos da UI através do `loaded_ui`
        self.input_tag = loaded_ui.findChild(QWidget, "input_tag")
        self.input_name = loaded_ui.findChild(QWidget, "input_name")
        self.input_desc = loaded_ui.findChild(QWidget, "input_desc")
        self.btn_add = loaded_ui.findChild(QWidget, "btn_add")
        self.table = loaded_ui.findChild(QWidget, "table")

    def clear_inputs(self):
        self.input_tag.clear()
        self.input_name.clear()
        self.input_desc.clear()

    def populate_table(self, equipments):
        self.table.setRowCount(len(equipments))
        for i, eq in enumerate(equipments):
            for j, val in enumerate(eq):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))