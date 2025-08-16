from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QDateEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit, QLineEdit

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        loaded_ui = uic.loadUi("view/ui_main.ui")
        self.setCentralWidget(loaded_ui)
        self.setWindowTitle("CADASTRO DE EQUIPAMENTOS")

        # Campos antigos
        self.input_tag = loaded_ui.findChild(QWidget, "input_tag")
        self.input_name = loaded_ui.findChild(QWidget, "input_name")
        self.input_desc = loaded_ui.findChild(QWidget, "input_desc")
        self.btn_add = loaded_ui.findChild(QWidget, "btn_add")
        self.btn_consulta = loaded_ui.findChild(QWidget, "btn_consulta")
        self.btn_historico = loaded_ui.findChild(QWidget, "btn_historico")

        # Novos campos
        self.input_cliente = loaded_ui.findChild(QLineEdit, "input_cliente")
        self.input_modelo = loaded_ui.findChild(QLineEdit, "input_modelo")
        self.input_serial = loaded_ui.findChild(QLineEdit, "input_serial")
        self.combo_tipo_servico = loaded_ui.findChild(QComboBox, "combo_tipo_servico")
        self.combo_status = loaded_ui.findChild(QComboBox, "combo_status")
        self.combo_prioridade = loaded_ui.findChild(QComboBox, "combo_prioridade")
        self.date_proxima = loaded_ui.findChild(QDateEdit, "date_proxima")
        self.input_custo = loaded_ui.findChild(QDoubleSpinBox, "input_custo")
        self.input_garantia_meses = loaded_ui.findChild(QSpinBox, "input_garantia_meses")
        self.input_observacoes = loaded_ui.findChild(QTextEdit, "input_observacoes")

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
        self.date_proxima.setDate(self.date_proxima.minimumDate())
        self.input_custo.setValue(0.0)
        self.input_garantia_meses.setValue(0)