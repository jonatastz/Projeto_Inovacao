from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QHeaderView

class HistoricoView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ui_historico.ui", self)

        # Garantir cabeçalhos e resize
        self.table_historico.setColumnCount(4)
        self.table_historico.setHorizontalHeaderLabels(["Tag", "Nome", "Descrição", "Data"])
        header = self.table_historico.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
