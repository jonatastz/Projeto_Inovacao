
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QTextEdit,
                             QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox, QPushButton, QHBoxLayout)
from PyQt5.QtCore import QDate

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CADASTRO DE EQUIPAMENTOS")
        cw = QWidget(); self.setCentralWidget(cw)
        root = QVBoxLayout(cw)

        title = QLabel("Cadastro de Equipamentos"); 
        root.addWidget(title)
        title.setObjectName("pageTitle")

        grid = QGridLayout()
        row = 0
        grid.addWidget(QLabel("Service Tag"), row,0); self.input_tag = QLineEdit(); grid.addWidget(self.input_tag, row,1)
        grid.addWidget(QLabel("Nome"), row,2); self.input_name = QLineEdit(); grid.addWidget(self.input_name, row,3)
        row += 1
        grid.addWidget(QLabel("Cliente"), row,0); self.input_cliente = QLineEdit(); grid.addWidget(self.input_cliente, row,1)
        grid.addWidget(QLabel("Modelo"), row,2); self.input_modelo = QLineEdit(); grid.addWidget(self.input_modelo, row,3)
        row += 1
        grid.addWidget(QLabel("Serial"), row,0); self.input_serial = QLineEdit(); grid.addWidget(self.input_serial, row,1)
        grid.addWidget(QLabel("Tipo de Serviço"), row,2); self.combo_tipo_servico = QComboBox(); 
        self.combo_tipo_servico.addItems(["", "Diagnóstico", "Formatação", "Troca de Peça", "Limpeza", "Outros"])
        grid.addWidget(self.combo_tipo_servico, row,3)
        row += 1
        grid.addWidget(QLabel("Status"), row,0); self.combo_status = QComboBox(); 
        self.combo_status.addItems(["", "Recebido", "Em análise", "Em execução", "Pronto", "Entregue"])
        grid.addWidget(self.combo_status, row,1)
        grid.addWidget(QLabel("Prioridade"), row,2); self.combo_prioridade = QComboBox(); 
        self.combo_prioridade.addItems(["", "Baixa", "Média", "Alta", "Urgente"])
        grid.addWidget(self.combo_prioridade, row,3)
        row += 1
        grid.addWidget(QLabel("Próx. Manutenção"), row,0); self.date_proxima = QDateEdit(); self.date_proxima.setCalendarPopup(True)
        self.date_proxima.setDate(QDate.currentDate()); grid.addWidget(self.date_proxima, row,1)
        grid.addWidget(QLabel("Custo (R$)"), row,2); self.input_custo = QDoubleSpinBox(); self.input_custo.setMaximum(1e9); self.input_custo.setDecimals(2)
        grid.addWidget(self.input_custo, row,3)
        row += 1
        grid.addWidget(QLabel("Garantia (meses)"), row,0); self.input_garantia_meses = QSpinBox(); self.input_garantia_meses.setRange(0, 120)
        grid.addWidget(self.input_garantia_meses, row,1)
        row += 1
        grid.addWidget(QLabel("Descrição"), row,0); self.input_desc = QTextEdit(); grid.addWidget(self.input_desc, row,1,1,3)
        row += 1
        grid.addWidget(QLabel("Observações"), row,0); self.input_observacoes = QTextEdit(); grid.addWidget(self.input_observacoes, row,1,1,3)

        root.addLayout(grid)
        # === Forçar labels de formulário (Cadastro) a branco + negrito ===
        try:
            alvo = {
                'service tag','cliente','serial','status','modelo','prioridade','garantia',
                'técnico','tecnico','data','descrição','descricao','observações','observacoes',
                'nome do equipamento','nome','cliente (responsável)','telefone','e-mail','email'
            }
            for lbl in self.findChildren(QLabel):
                t = (lbl.text() or "").strip().lower()
                if t in alvo:
                    lbl.setStyleSheet("color: white; font-weight: 700;")
        except Exception:
            pass


        # Buttons
        bar = QHBoxLayout()
        self.btn_add = QPushButton("Salvar Cadastro")
        self.btn_consulta = QPushButton("Consulta")
        self.btn_historico = QPushButton("Histórico")
        bar.addStretch(1); bar.addWidget(self.btn_consulta); bar.addWidget(self.btn_historico); bar.addWidget(self.btn_add)
        root.addLayout(bar)

    def clear_inputs(self):
        self.input_tag.clear()
        self.input_name.clear()
        self.input_desc.clear()
        self.input_cliente.clear()
        self.input_modelo.clear()
        self.input_serial.clear()
        self.input_observacoes.clear()
        self.combo_tipo_servico.setCurrentIndex(0)
        self.combo_status.setCurrentIndex(0)
        self.combo_prioridade.setCurrentIndex(0)
        self.input_custo.setValue(0.0)
        self.input_garantia_meses.setValue(0)