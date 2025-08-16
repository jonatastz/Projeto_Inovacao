from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class DetalheView(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ui_detalhe.ui", self)

    def load_from_record(self, rec):
        # rec:
        # (id, tag, nome, cliente, modelo, serial, descricao, tipo, status, prioridade,
        #  proxima_manutencao, custo, garantia_meses, observacoes, data_cadastro)
        (eid, tag, nome, cliente, modelo, serial, desc, tipo, status, prioridade,
         proxima, custo, garantia, obs, data) = rec

        self._id = eid
        self.fld_tag.setText(tag or "")
        self.fld_nome.setText(nome or "")
        self.fld_cliente.setText(cliente or "")
        self.fld_modelo.setText(modelo or "")
        self.fld_serial.setText(serial or "")
        self.fld_tipo.setText(tipo or "")
        self.combo_status.setCurrentText(status or "Recebido")
        self.combo_prioridade.setCurrentText(prioridade or "Baixa")
        if proxima:
            from PyQt5.QtCore import QDate
            try:
                y, m, d = map(int, proxima.split("-"))
                self.date_prox.setDate(QDate(y, m, d))
            except Exception:
                pass
        self.fld_data.setText(data or "")
        self.txt_desc.setPlainText(desc or "")
        self.txt_obs.setPlainText(obs or "")

    def values(self):
        return dict(
            id=self._id,
            status=self.combo_status.currentText(),
            prioridade=self.combo_prioridade.currentText(),
            proxima=self.date_prox.date().toString("yyyy-MM-dd"),
            observacoes=self.txt_obs.toPlainText()
        )