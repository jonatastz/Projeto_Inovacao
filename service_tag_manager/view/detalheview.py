
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox, QTextEdit, QDialogButtonBox, QLabel
from PyQt5.QtCore import QDate

class DetalheView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.showFullScreen()
        self.setWindowTitle("Detalhe do Equipamento")
        lay = QFormLayout(self)

        self.fld_id = QLineEdit(); self.fld_id.setReadOnly(True)
        self.fld_tag = QLineEdit(); self.fld_tag.setReadOnly(True)
        self.fld_nome = QLineEdit(); self.fld_nome.setReadOnly(True)
        self.combo_status = QComboBox(); self.combo_status.addItems(["", "Recebido", "Em análise", "Em execução", "Pronto", "Entregue"])
        self.combo_prioridade = QComboBox(); self.combo_prioridade.addItems(["", "Baixa", "Média", "Alta", "Urgente"])
        self.date_prox = QDateEdit(); self.date_prox.setCalendarPopup(True); self.date_prox.setDate(QDate.currentDate())
        self.fld_custo = QDoubleSpinBox(); self.fld_custo.setMaximum(1e9); self.fld_custo.setDecimals(2)
        self.fld_garantia = QSpinBox(); self.fld_garantia.setRange(0, 120)
        self.txt_desc = QTextEdit(); self.txt_obs = QTextEdit()

        lay.addRow(QLabel("ID"), self.fld_id)
        lay.addRow(QLabel("Tag"), self.fld_tag)
        lay.addRow(QLabel("Nome"), self.fld_nome)
        lay.addRow(QLabel("Status"), self.combo_status)
        lay.addRow(QLabel("Prioridade"), self.combo_prioridade)
        lay.addRow(QLabel("Próx. Manutenção"), self.date_prox)
        lay.addRow(QLabel("Custo (R$)"), self.fld_custo)
        lay.addRow(QLabel("Garantia (meses)"), self.fld_garantia)
        lay.addRow(QLabel("Descrição"), self.txt_desc)
        lay.addRow(QLabel("Observações"), self.txt_obs)

        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=self)
        btns.accepted.connect(self.accept); btns.rejected.connect(self.reject)
        lay.addRow(btns)

        self._eid = None

    def load_from_record(self, rec):
        (eid, tag, nome, cliente, modelo, serial, desc, tipo, status, prioridade,
         proxima, custo, garantia, obs, data) = rec
        self._eid = eid
        self.fld_id.setText(str(eid)); self.fld_tag.setText(tag or ""); self.fld_nome.setText(nome or "")
        self.combo_status.setCurrentText(status or "")
        self.combo_prioridade.setCurrentText(prioridade or "")
        if proxima:
            y, m, d = map(int, (proxima.split("-") + ["1","1","1"])[:3])
            self.date_prox.setDate(QDate(y, m, d))
        self.fld_custo.setValue(float(custo or 0.0))
        self.fld_garantia.setValue(int(garantia or 0))
        self.txt_desc.setPlainText(desc or "")
        self.txt_obs.setPlainText(obs or "")

    def values(self):
        return dict(
            id=self._eid,
            status=self.combo_status.currentText(),
            prioridade=self.combo_prioridade.currentText(),
            proxima_manutencao=self.date_prox.date().toString("yyyy-MM-dd"),
            custo=float(self.fld_custo.value()),
            garantia_meses=int(self.fld_garantia.value()),
            descricao=self.txt_desc.toPlainText().strip(),
            observacoes=self.txt_obs.toPlainText().strip(),
        )
