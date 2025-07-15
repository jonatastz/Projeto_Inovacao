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

    # Stack para as views
    stacked_widget = QStackedWidget()

    # Instanciar as views
    main_view = MainView()
    consulta_view = ConsultaView()
    historico_view = HistoricoView()

    # Adicionar ao stack
    stacked_widget.addWidget(main_view)       # index 0
    stacked_widget.addWidget(consulta_view)   # index 1
    stacked_widget.addWidget(historico_view)  # index 2

    # Modelo e controlador
    model = EquipmentModel()
    controller = MainController(
        stacked_widget, main_view, consulta_view, historico_view, model
    )

    # Exibir
    stacked_widget.setCurrentIndex(0)
    stacked_widget.show()
    sys.exit(app.exec_())