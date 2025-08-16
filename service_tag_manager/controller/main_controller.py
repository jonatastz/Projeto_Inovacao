from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QMenu
from PyQt5.QtCore import Qt, QPoint, QDate
from view.detalheview import DetalheView

class MainController:
    def __init__(self, stacked_widget, main_view, consulta_view, historico_view, model):
        self.stacked_widget = stacked_widget
        self.main_view = main_view
        self.consulta_view = consulta_view
        self.historico_view = historico_view
        self.model = model

        # Main
        self.main_view.btn_add.clicked.connect(self.adicionar_equipamento)
        self.main_view.btn_consulta.clicked.connect(self.mostrar_consulta)
        self.main_view.btn_historico.clicked.connect(self.mostrar_historico)

        # Consulta
        v = self.consulta_view
        v.btn_voltar_consulta.clicked.connect(self.voltar)
        v.input_busca.returnPressed.connect(self._consulta_buscar)
        v.input_busca.textChanged.connect(self._consulta_buscar)
        v.table_resultados.itemDoubleClicked.connect(self._abrir_detalhe_selecionado)
        v.table_resultados.setContextMenuPolicy(Qt.CustomContextMenu)
        v.table_resultados.customContextMenuRequested.connect(self._consulta_context_menu)

        # Histórico
        h = self.historico_view
        h.btn_voltar_historico.clicked.connect(self.voltar)
        h.table_historico.itemDoubleClicked.connect(self._abrir_detalhe_selecionado_hist)
        h.table_historico.setContextMenuPolicy(Qt.CustomContextMenu)
        h.table_historico.customContextMenuRequested.connect(self._historico_context_menu)

    # -------- UX helpers ----------
    def _msg_info(self, titulo, texto):
        QMessageBox.information(self.main_view, titulo, texto)

    def _msg_erro(self, titulo, texto):
        QMessageBox.critical(self.main_view, titulo, texto)

    def _linha_para_id(self, table, row):
        # ID está na coluna 0 (oculta)
        item = table.item(row, 0)
        if not item: return None
        try:
            return int(item.text())
        except Exception:
            return None

    def _pintar_linha_por_status(self, table, row, status, prox):
        # Badge básico via cor de fundo por status
        cor = None
        s = (status or "").lower()
        if "aguardando" in s:
            cor = Qt.yellow
        elif "reparo" in s:
            cor = Qt.magenta
        elif "pronto" in s:
            cor = Qt.green
        elif "entregue" in s:
            cor = Qt.cyan
        elif "análise" in s or "analise" in s:
            cor = Qt.lightGray

        # Vencido (próx manutenção < hoje) = vermelho suave
        try:
            if prox:
                today = QDate.currentDate()
                y, m, d = map(int, prox.split("-"))
                if QDate(y, m, d) < today:
                    cor = Qt.red
        except Exception:
            pass

        if cor:
            for c in range(table.columnCount()):
                item = table.item(row, c)
                if item:
                    item.setBackground(cor)

    # -------- CADASTRO ----------
    def adicionar_equipamento(self):
        mv = self.main_view
        tag = (mv.input_tag.text() or "").strip()
        nome = (mv.input_name.text() or "").strip()
        desc = (mv.input_desc.toPlainText() or "").strip()
        cliente = (mv.input_cliente.text() or "").strip()
        modelo = (mv.input_modelo.text() or "").strip()
        serial = (mv.input_serial.text() or "").strip()
        tipo_servico = mv.combo_tipo_servico.currentText()
        status = mv.combo_status.currentText()
        prioridade = mv.combo_prioridade.currentText()
        proxima_manutencao = mv.date_proxima.date().toString("yyyy-MM-dd") if mv.date_proxima.date().isValid() else ""
        custo = float(mv.input_custo.value())
        garantia_meses = int(mv.input_garantia_meses.value())
        observacoes = (mv.input_observacoes.toPlainText() or "").strip()

        if not tag or not nome or not cliente:
            self._msg_erro("Falha ao adicionar", "Preencha os campos obrigatórios: Tag, Nome e Cliente.")
            return

        try:
            self.model.adicionar_equipamento(
                tag, nome, desc, cliente, modelo, serial, tipo_servico,
                status, prioridade, proxima_manutencao, custo, garantia_meses, observacoes
            )
        except Exception as e:
            msg = str(e)
            if "UNIQUE" in msg or "unique" in msg:
                self._msg_erro("Falha ao adicionar", f"TAG '{tag}' já cadastrada. Não é permitido duplicar.")
            else:
                self._msg_erro("Falha ao adicionar", f"Ocorreu um erro ao salvar: {msg}")
            return

        self._msg_info("Sucesso", f"Equipamento '{nome}' (TAG {tag}) adicionado com sucesso!")
        mv.clear_inputs()

    # -------- CONSULTA ----------
    def mostrar_consulta(self):
        self.consulta_view.input_busca.clear()
        self.consulta_view.table_resultados.setRowCount(0)
        self.stacked_widget.setCurrentIndex(1)

    def _consulta_buscar(self):
        termo = (self.consulta_view.input_busca.text() or "").strip()
        resultados = self.model.buscar_simples(termo)
        t = self.consulta_view.table_resultados
        t.setRowCount(len(resultados))
        for i, row in enumerate(resultados):
            # (id, tag, nome, cliente, modelo, descricao, tipo, status, prioridade, prox, data)
            eid, tag, nome, cliente, modelo, desc, tipo, status, prioridade, prox, data = row
            for col, val in enumerate([eid, tag, nome, cliente, modelo, desc, tipo, status, prioridade, prox, data]):
                item = QTableWidgetItem(str(val or ""))
                if col == 0:  # ID
                    item.setData(Qt.UserRole, eid)
                t.setItem(i, col, item)
            self._pintar_linha_por_status(t, i, status, prox)

    def _consulta_context_menu(self, pos:QPoint):
        t = self.consulta_view.table_resultados
        row = t.currentRow()
        if row < 0: return
        menu = QMenu(t)
        act_edit = menu.addAction("Editar")
        act_del  = menu.addAction("Excluir")
        action = menu.exec_(t.mapToGlobal(pos))
        if action == act_edit:
            self._abrir_detalhe_selecionado()
        elif action == act_del:
            self._excluir_selecionado()

    def _abrir_detalhe_selecionado(self):
        t = self.consulta_view.table_resultados
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        self._abrir_dialogo_detalhe(equip_id)

    # -------- HISTÓRICO ----------
    def mostrar_historico(self):
        resultados = self.model.buscar_avancado(termo="")
        t = self.historico_view.table_historico
        t.setRowCount(len(resultados))
        for i, row in enumerate(resultados):
            # (id, tag, nome, cliente, modelo, status, prioridade, prox, data)
            eid, tag, nome, cliente, modelo, status, prioridade, prox, data = row
            for col, val in enumerate([eid, tag, nome, cliente, modelo, status, prioridade, prox, data]):
                item = QTableWidgetItem(str(val or ""))
                if col == 0:
                    item.setData(Qt.UserRole, eid)
                t.setItem(i, col, item)
            self._pintar_linha_por_status(t, i, status, prox)
        self.stacked_widget.setCurrentIndex(2)

    def _historico_context_menu(self, pos:QPoint):
        t = self.historico_view.table_historico
        row = t.currentRow()
        if row < 0: return
        menu = QMenu(t)
        act_edit = menu.addAction("Editar")
        act_del  = menu.addAction("Excluir")
        action = menu.exec_(t.mapToGlobal(pos))
        if action == act_edit:
            self._abrir_detalhe_selecionado_hist()
        elif action == act_del:
            self._excluir_selecionado_hist()

    def _abrir_detalhe_selecionado_hist(self):
        t = self.historico_view.table_historico
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        self._abrir_dialogo_detalhe(equip_id)

    # -------- DIÁLOGO DETALHE ----------
    def _abrir_dialogo_detalhe(self, equip_id:int):
        rec = self.model.obter_por_id(equip_id)
        if not rec:
            self._msg_erro("Erro", "Registro não encontrado.")
            return
        dlg = DetalheView()
        dlg.load_from_record(rec)
        dlg.btn_cancelar.clicked.connect(dlg.reject)
        dlg.btn_salvar.clicked.connect(dlg.accept)
        if dlg.exec_():
            vals = dlg.values()
            ok = self.model.atualizar_basico(
                equip_id=vals["id"],
                status=vals["status"],
                prioridade=vals["prioridade"],
                proxima_manutencao=vals["proxima"],
                observacoes=vals["observacoes"]
            )
            if ok:
                self._msg_info("Salvo", "Atualizado com sucesso.")
                # refresh da tela correta
                if self.stacked_widget.currentIndex() == 1:
                    self._consulta_buscar()
                else:
                    self.mostrar_historico()
            else:
                self._msg_erro("Erro", "Não foi possível atualizar.")

    # -------- EXCLUSÃO ----------
    def _excluir_selecionado(self):
        t = self.consulta_view.table_resultados
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        if QMessageBox.question(self.main_view, "Excluir", "Deseja remover este registro?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            if self.model.excluir(equip_id):
                self._msg_info("Removido", "Registro excluído.")
                self._consulta_buscar()

    def _excluir_selecionado_hist(self):
        t = self.historico_view.table_historico
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        if QMessageBox.question(self.main_view, "Excluir", "Deseja remover este registro?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            if self.model.excluir(equip_id):
                self._msg_info("Removido", "Registro excluído.")
                self.mostrar_historico()

    # -------- Navegação ----------
    def voltar(self):
        self.stacked_widget.setCurrentIndex(0)