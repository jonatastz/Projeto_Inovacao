from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHeaderView

class ConsultaView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ui_consulta.ui", self)

        t = self.table_resultados
        t.setColumnCount(11)
        t.setHorizontalHeaderLabels([
            "ID", "Tag", "Nome", "Cliente", "Modelo", "Descrição",
            "Tipo", "Status", "Prioridade", "Próx. Manut.", "Data Cad."
        ])
        h = t.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Tag
        h.setSectionResizeMode(2, QHeaderView.Stretch)           # Nome
        h.setSectionResizeMode(3, QHeaderView.Stretch)           # Cliente
        h.setSectionResizeMode(4, QHeaderView.Stretch)           # Modelo
        h.setSectionResizeMode(5, QHeaderView.Stretch)           # Descrição
        h.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Tipo
        h.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Status
        h.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Prioridade
        h.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Próx. Manut.
        h.setSectionResizeMode(10, QHeaderView.ResizeToContents) # Data Cad.

        t.setSortingEnabled(True)
        t.setSelectionBehavior(t.SelectRows)
        t.setSelectionMode(t.SingleSelection)
        t.setEditTriggers(t.NoEditTriggers)

        # Esconde a coluna ID na UI (mas fica disponível para recuperar)
        t.setColumnHidden(0, True)