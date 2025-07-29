from PyQt5.QtWidgets import QTableWidgetItem

class MainController:
    def __init__(self, stacked_widget, main_view, consulta_view, historico_view, model):
        self.stacked_widget = stacked_widget
        self.main_view = main_view
        self.consulta_view = consulta_view
        self.historico_view = historico_view
        self.model = model

        self.main_view.btn_add.clicked.connect(self.adicionar_equipamento)
        self.main_view.btn_consulta.clicked.connect(self.mostrar_consulta)
        self.main_view.btn_historico.clicked.connect(self.mostrar_historico)


        self.consulta_view.btn_voltar_consulta.clicked.connect(self.voltar)
        self.consulta_view.input_busca.returnPressed.connect(self.buscar_equipamentos)
        self.historico_view.btn_voltar_historico.clicked.connect(self.voltar)


    def adicionar_equipamento(self):
        tag = self.main_view.input_tag.text()
        nome = self.main_view.input_name.text()
        desc = self.main_view.input_desc.toPlainText()
        self.model.adicionar_equipamento(tag, nome, desc)
        self.main_view.clear_inputs()
        self.main_view.populate_table(self.model.listar_equipamentos())

    def mostrar_consulta(self):
        self.stacked_widget.setCurrentIndex(1)


    def buscar_equipamentos(self):
        termo = self.consulta_view.input_busca.text()
        resultados = self.model.buscar_por_tag_ou_nome(termo)
        tabela = self.consulta_view.table_resultados
        tabela.setRowCount(len(resultados))
        for i, (tag, nome, desc) in enumerate(resultados):
            tabela.setItem(i, 0, QTableWidgetItem(tag))
            tabela.setItem(i, 1, QTableWidgetItem(nome))
            tabela.setItem(i, 2, QTableWidgetItem(desc))

    def mostrar_historico(self):
        historico = self.model.listar_equipamentos()
        tabela = self.historico_view.table_historico
        tabela.setRowCount(len(historico))
        for i, (tag, nome, desc) in enumerate(historico):
            tabela.setItem(i, 0, QTableWidgetItem(tag))
            tabela.setItem(i, 1, QTableWidgetItem(nome))
            tabela.setItem(i, 2, QTableWidgetItem(desc))
        self.stacked_widget.setCurrentIndex(2)

    def voltar(self):
        self.stacked_widget.setCurrentIndex(0)