
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView

class HistoricoView(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        self.setObjectName("HistoricoPage")

        title = QLabel("Histórico - Equipamentos"); 
        root.addWidget(title)
        title.setObjectName("pageTitle")

        self.table_historico = QTableWidget(0, 9)
        self.table_historico.setHorizontalHeaderLabels([
            "ID","Tag","Nome","Cliente","Modelo","Status","Prioridade","Próx. Manut.","Data Cad."
        ])
        h = self.table_historico.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.Stretch)
        h.setSectionResizeMode(4, QHeaderView.Stretch)
        h.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.table_historico.setSelectionBehavior(self.table_historico.SelectRows)
        self.table_historico.setSelectionMode(self.table_historico.SingleSelection)
        self.table_historico.setEditTriggers(self.table_historico.NoEditTriggers)
        self.table_historico.setColumnHidden(0, True)
        root.addWidget(self.table_historico, 1)

        bar = QHBoxLayout()
        self.lbl_count_h = QLabel("0 resultados")
        self.btn_editar_h = QPushButton("Editar")
        self.btn_excluir_h = QPushButton("Excluir")
        self.btn_novo_servico_h = QPushButton("Novo Serviço")
        self.btn_voltar_historico = QPushButton("Voltar")
        bar.addWidget(self.lbl_count_h); bar.addStretch(1)
        for b in [self.btn_novo_servico_h, self.btn_editar_h, self.btn_excluir_h, self.btn_voltar_historico]:
            bar.addWidget(b)
        root.addLayout(bar)
