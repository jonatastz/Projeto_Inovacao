
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox, QDialogButtonBox, QLabel, QDateEdit
from PyQt5.QtCore import QDate

class ServiceDialog(QDialog):
    def __init__(self, parent=None, equip_label:str=""):
        super().__init__(parent)
        self.showFullScreen()
        self.setWindowTitle(f"Novo serviço - {equip_label}")
        lay = QFormLayout(self)

        self.date = QDateEdit(); self.date.setCalendarPopup(True); self.date.setDate(QDate.currentDate())
        self.tipo = QLineEdit(); self.status = QLineEdit(); self.tecnico = QLineEdit()
        self.custo = QDoubleSpinBox(); self.custo.setMaximum(1e9); self.custo.setDecimals(2)
        self.garantia = QSpinBox(); self.garantia.setRange(0, 120)
        self.descricao = QTextEdit(); self.obs = QTextEdit()

        lay.addRow(QLabel("Data do serviço:"), self.date)
        lay.addRow(QLabel("Tipo de serviço:"), self.tipo)
        lay.addRow(QLabel("Status:"), self.status)
        lay.addRow(QLabel("Técnico:"), self.tecnico)
        lay.addRow(QLabel("Custo (R$):"), self.custo)
        lay.addRow(QLabel("Garantia (meses):"), self.garantia)
        lay.addRow(QLabel("Descrição:"), self.descricao)
        lay.addRow(QLabel("Observações:"), self.obs)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        btns.accepted.connect(self.accept); btns.rejected.connect(self.reject)
        lay.addRow(btns)

    def values(self):
        return dict(
            data_servico=self.date.date().toString("yyyy-MM-dd"),
            tipo=self.tipo.text().strip() or None,
            status=self.status.text().strip() or None,
            tecnico=self.tecnico.text().strip() or None,
            custo=float(self.custo.value()) if self.custo.value() else None,
            garantia_meses=int(self.garantia.value()) if self.garantia.value() else None,
            descricao=self.descricao.toPlainText().strip() or None,
            observacoes=self.obs.toPlainText().strip() or None,
        )
