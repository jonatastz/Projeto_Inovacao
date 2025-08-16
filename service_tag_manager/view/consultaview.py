from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QHeaderView

class ConsultaView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ui_consulta.ui", self)

        # Garantir cabeçalhos e resize
        self.table_resultados.setColumnCount(4)
        self.table_resultados.setHorizontalHeaderLabels(["Tag", "Nome", "Descrição", "Data"])
        header = self.table_resultados.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
