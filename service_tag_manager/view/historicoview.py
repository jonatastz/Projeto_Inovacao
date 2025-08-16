from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QHeaderView

class HistoricoView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ui_historico.ui", self)

        t = self.table_historico
        t.setColumnCount(9)
        t.setHorizontalHeaderLabels([
            "ID","Tag","Nome","Cliente","Modelo","Status","Prioridade","Próx. Manut.","Data Cad."
        ])

        h = t.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents) # ID
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Tag
        h.setSectionResizeMode(2, QHeaderView.Stretch)          # Nome
        h.setSectionResizeMode(3, QHeaderView.Stretch)          # Cliente
        h.setSectionResizeMode(4, QHeaderView.Stretch)          # Modelo
        h.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Status
        h.setSectionResizeMode(6, QHeaderView.ResizeToContents) # Prioridade
        h.setSectionResizeMode(7, QHeaderView.ResizeToContents) # Próx. Manut.
        h.setSectionResizeMode(8, QHeaderView.ResizeToContents) # Data Cad.

        t.setSortingEnabled(True)
        t.setSelectionBehavior(t.SelectRows)
        t.setSelectionMode(t.SingleSelection)
        t.setEditTriggers(t.NoEditTriggers)
        t.setColumnHidden(0, True)