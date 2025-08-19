
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit
from PyQt5.QtCore import QDate

class ConsultaView(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        self.setObjectName("ConsultaPage")

        title = QLabel("Consulta de Equipamentos"); 
        root.addWidget(title)
        title.setObjectName("pageTitle")

        # Filters
        fl = QHBoxLayout()
        self.input_termo = QLineEdit(); self.input_termo.setPlaceholderText("Tag, nome, cliente, modelo...")
        self.combo_status = QComboBox(); self.combo_status.addItems(["", "Recebido", "Em análise", "Em execução", "Pronto", "Entregue"])
        self.combo_prioridade = QComboBox(); self.combo_prioridade.addItems(["", "Baixa", "Média", "Alta", "Urgente"])
        self.btn_buscar = QPushButton("Buscar")
        self.btn_limpar = QPushButton("Limpar")
        fl.addWidget(QLabel("Pesquisar:")); fl.addWidget(self.input_termo, 1)
        fl.addWidget(QLabel("Status:")); fl.addWidget(self.combo_status)
        fl.addWidget(QLabel("Prioridade:")); fl.addWidget(self.combo_prioridade)
        fl.addWidget(self.btn_buscar); fl.addWidget(self.btn_limpar)
        root.addLayout(fl)

        # Table
        self.table_resultados = QTableWidget(0, 11)
        self.table_resultados.setHorizontalHeaderLabels([
            "ID","Tag","Nome","Cliente","Modelo","Descrição","Tipo","Status","Prioridade","Próx. Manut.","Data Cad."
        ])
        h = self.table_resultados.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.Stretch)
        h.setSectionResizeMode(4, QHeaderView.Stretch)
        h.setSectionResizeMode(5, QHeaderView.Stretch)
        h.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(9, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.table_resultados.setSelectionBehavior(self.table_resultados.SelectRows)
        self.table_resultados.setSelectionMode(self.table_resultados.SingleSelection)
        self.table_resultados.setEditTriggers(self.table_resultados.NoEditTriggers)
        self.table_resultados.setColumnHidden(0, True)
        root.addWidget(self.table_resultados, 1)

        # Bottom bar
        bar = QHBoxLayout()
        self.lbl_count = QLabel("0 resultados")
        self.btn_editar = QPushButton("Editar")
        self.btn_excluir = QPushButton("Excluir")
        self.btn_novo_servico = QPushButton("Novo Serviço")
        self.btn_voltar_consulta = QPushButton("Voltar")
        bar.addWidget(self.lbl_count); bar.addStretch(1)
        for b in [self.btn_novo_servico, self.btn_editar, self.btn_excluir, self.btn_voltar_consulta]:
            bar.addWidget(b)
        root.addLayout(bar)
