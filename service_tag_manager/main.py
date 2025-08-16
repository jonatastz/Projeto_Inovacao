import sys
import os
from PyQt5.QtWidgets import QApplication, QStackedWidget
from model.equipment_model import EquipmentModel
from view.main_view import MainView
from view.consultaview import ConsultaView
from view.historicoview import HistoricoView
from controller.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    stacked_widget = QStackedWidget()

    main_view = MainView()
    consulta_view = ConsultaView()
    historico_view = HistoricoView()

    stacked_widget.addWidget(main_view)
    stacked_widget.addWidget(consulta_view)
    stacked_widget.addWidget(historico_view)

    model = EquipmentModel("equipamentos.db")
    controller = MainController(stacked_widget, main_view, consulta_view, historico_view, model)

    stacked_widget.setWindowTitle("Service Tag Manager")
    stacked_widget.setCurrentIndex(0)
    stacked_widget.show()

    sys.exit(app.exec_())