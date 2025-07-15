from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class ConsultaView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ui_consulta.ui", self)
