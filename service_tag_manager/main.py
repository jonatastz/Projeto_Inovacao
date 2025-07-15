import sys
import os
from PyQt5.QtWidgets import QApplication
from model.equipment_model import EquipmentModel
from view.main_view import MainView
from controller.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    view = MainView()
    model = EquipmentModel()
    controller = MainController(view, model)
    view.show()
    sys.exit(app.exec_())