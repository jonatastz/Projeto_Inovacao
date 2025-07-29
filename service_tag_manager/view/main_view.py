from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        loaded_ui = uic.loadUi("view/ui_main.ui")  
        self.setCentralWidget(loaded_ui)
        self.setWindowTitle("Service Tag Manager")

        
        self.input_tag = loaded_ui.findChild(QWidget, "input_tag")
        self.input_name = loaded_ui.findChild(QWidget, "input_name")
        self.input_desc = loaded_ui.findChild(QWidget, "input_desc")
        self.btn_add = loaded_ui.findChild(QWidget, "btn_add")
        self.btn_consulta = loaded_ui.findChild(QWidget, "btn_consulta")
        self.btn_historico = loaded_ui.findChild(QWidget, "btn_historico")
        self.table = loaded_ui.findChild(QWidget, "table")

        
        self.btn_consulta.clicked.connect(self.abrir_pagina_consulta)
        self.btn_historico.clicked.connect(self.abrir_pagina_historico)

    def clear_inputs(self):
        self.input_tag.clear()
        self.input_name.clear()
        self.input_desc.clear()

    def populate_table(self, equipamentos):
        self.table.setRowCount(len(equipamentos))
        for i, eq in enumerate(equipamentos):
            for j, val in enumerate(eq):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


    def abrir_pagina_consulta(self):
        print("Abrindo página de consulta...") 

    def abrir_pagina_historico(self):
        print("Abrindo página de histórico...") 

    