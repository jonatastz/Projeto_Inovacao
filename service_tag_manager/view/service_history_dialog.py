
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView

class ServiceHistoryDialog(QDialog):
    def __init__(self, parent=None, equip_label:str="Histórico", rows=None):
        super().__init__(parent)
        self.showFullScreen()
        self.setWindowTitle(f"Histórico de serviços - {equip_label}")
        lay = QVBoxLayout(self)
        t = QTableWidget(0, 9, self)
        t.setHorizontalHeaderLabels(["ID","Data","Tipo","Status","Técnico","Custo","Garantia (m)","Descrição","Observações"])
        h = t.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(7, QHeaderView.Stretch)
        h.setSectionResizeMode(8, QHeaderView.Stretch)
        lay.addWidget(QLabel(equip_label))
        lay.addWidget(t)
        self.table = t
        self.load(rows or [])

    def load(self, rows):
        self.table.setRowCount(0)
        for r in rows:
            # r: (id, equipamento_id, data, tipo, desc, tecnico, status, custo, garantia, obs)
            row = self.table.rowCount(); self.table.insertRow(row)
            vals = [r[0], r[2], r[3], r[6], r[5], f"{r[7]:.2f}", r[8], r[4], r[9]]
            for c, v in enumerate(vals):
                self.table.setItem(row, c, QTableWidgetItem(str(v if v is not None else "")))
