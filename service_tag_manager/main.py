
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from model.equipment_model import EquipmentModel
from view.main_view import MainView
from view.consultaview import ConsultaView
from view.historicoview import HistoricoView
from controller.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # === Global Style (verde + azulado) ===
    app.setStyleSheet("""
/* ===== Accessible Dark Theme (uniform across all screens) ===== */

/* Background base (dark) */
QWidget, QMainWindow, QDialog, QStackedWidget {
    background: #0b1220;
    color: #ffffff;
    font-family: "Segoe UI", "Ubuntu", "Arial";
    font-size: 11pt;
}

/* Titles and labels */
QLabel { color: #ffffff; font-weight: 700; }
QGroupBox::title { color: #ffffff; font-weight: 700; }

/* Buttons: solid green always; pressed slightly darker */
QPushButton {
    background-color: #22c55e;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 700;
    min-height: 36px;
}
QPushButton:hover { background-color: #22c55e; }
QPushButton:pressed { background-color: #16a34a; }
QPushButton:disabled { background-color: #9bd8b2; color: #e5e7eb; }

/* Inputs & Tables: white background, dark text */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDateEdit,
QDoubleSpinBox, QSpinBox, QTableWidget, QTableView {
    background: #ffffff;
    color: #111827;
    border: 1px solid #94a3b8;
    border-radius: 8px;
    padding: 6px 8px;
    selection-background-color: #d1fae5;
    selection-color: #0b1220;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QDateEdit:focus,
QDoubleSpinBox:focus, QSpinBox:focus {
    background: #ffffff;
    color: #111827;
    border: 1px solid #60a5fa;
}
QLineEdit::placeholder, QTextEdit::placeholder, QPlainTextEdit::placeholder {
    color: #6b7280;
}

/* Table headers high-contrast */
QHeaderView::section {
    background: #0f172a;
    color: #ffffff;
    padding: 8px;
    border: none;
    font-weight: 800;
}

/* Selected items inside tables */
QTableWidget::item:selected, QTableView::item:selected {
    background: #bbf7d0;
    color: #0b1220;
}
""")

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
    stacked_widget.showFullScreen()
    sys.exit(app.exec_())
