from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

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
        v.btn_editar.clicked.connect(self._abrir_detalhe_selecionado)
        v.btn_excluir.clicked.connect(self._excluir_selecionado)
        v.btn_limpar.clicked.connect(self._consulta_limpar)

        # Busca reativa
        v.input_busca.returnPressed.connect(self._consulta_buscar)
        v.input_busca.textChanged.connect(self._consulta_buscar)
        v.filtro_status.currentIndexChanged.connect(self._consulta_buscar)
        v.filtro_tipo.currentIndexChanged.connect(self._consulta_buscar)
        v.filtro_prioridade.currentIndexChanged.connect(self._consulta_buscar)

        # Histórico
        h = self.historico_view
        h.btn_voltar_historico.clicked.connect(self.voltar)
        h.btn_editar_h.clicked.connect(self._abrir_detalhe_selecionado_hist)
        h.btn_excluir_h.clicked.connect(self._excluir_selecionado_hist)

    # Helpers
    def _msg_info(self, titulo, texto): QMessageBox.information(self.main_view, titulo, texto)
    def _msg_erro(self, titulo, texto): QMessageBox.critical(self.main_view, titulo, texto)

    def _linha_para_id(self, table, row):
        item = table.item(row, 0)
        if not item: return None
        try: return int(item.text())
        except: return None

    # CADASTRO
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

    # CONSULTA
    def mostrar_consulta(self):
        v = self.consulta_view
        v.input_busca.clear()
        v.filtro_status.setCurrentIndex(0)
        v.filtro_tipo.setCurrentIndex(0)
        v.filtro_prioridade.setCurrentIndex(0)
        v.table_resultados.setRowCount(0)
        v.lbl_count.setText("0 resultados")
        self.stacked_widget.setCurrentIndex(1)

    def _consulta_limpar(self):
        v = self.consulta_view
        v.input_busca.clear()
        v.filtro_status.setCurrentIndex(0)
        v.filtro_tipo.setCurrentIndex(0)
        v.filtro_prioridade.setCurrentIndex(0)
        v.table_resultados.setRowCount(0)
        v.lbl_count.setText("0 resultados")

    def _consulta_buscar(self):
        v = self.consulta_view
        termo = (v.input_busca.text() or "").strip()

        status = v.filtro_status.currentText()
        tipo = v.filtro_tipo.currentText()
        prioridade = v.filtro_prioridade.currentText()
        status = "" if status.startswith("(") else status
        tipo = "" if tipo.startswith("(") else tipo
        prioridade = "" if prioridade.startswith("(") else prioridade

        # usar buscar_simples para texto e buscar_avancado para filtros
        if any([status, tipo, prioridade]):
            resultados = self.model.buscar_avancado(
                termo=termo, status=status, tipo=tipo, prioridade=prioridade
            )
            # buscar_avancado não retorna descrição; então fazemos um merge simples:
            # para simplificar, quando filtros existem, mostramos sem a coluna descrição (ou vazia).
            # (Mantemos a estrutura das 11 colunas, coluna 5 vazia)
            t = v.table_resultados
            t.setRowCount(len(resultados))
            for i, (eid, tag, nome, cliente, modelo, status, prioridade, prox, data) in enumerate(resultados):
                values = [eid, tag, nome, cliente, modelo, "", "", status, prioridade, prox, data]
                for col, val in enumerate(values):
                    t.setItem(i, col, QTableWidgetItem(str(val or "")))
        else:
            res = self.model.buscar_simples(termo)
            t = v.table_resultados
            t.setRowCount(len(res))
            for i, row in enumerate(res):
                # (id, tag, nome, cliente, modelo, descricao, tipo, status, prioridade, prox, data)
                for col, val in enumerate(row):
                    t.setItem(i, col, QTableWidgetItem(str(val or "")))

        v.lbl_count.setText(f"{v.table_resultados.rowCount()} resultados")

    def _abrir_detalhe_selecionado(self):
        t = self.consulta_view.table_resultados
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        self._abrir_dialogo_detalhe(equip_id)

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

    # HISTÓRICO
    def mostrar_historico(self):
        v = self.historico_view
        res = self.model.buscar_avancado(termo="")
        t = v.table_historico
        t.setRowCount(len(res))
        for i, (eid, tag, nome, cliente, modelo, status, prioridade, prox, data) in enumerate(res):
            for col, val in enumerate([eid, tag, nome, cliente, modelo, status, prioridade, prox, data]):
                t.setItem(i, col, QTableWidgetItem(str(val or "")))
        v.lbl_count_h.setText(f"{t.rowCount()} resultados")
        self.stacked_widget.setCurrentIndex(2)

    def _abrir_detalhe_selecionado_hist(self):
        t = self.historico_view.table_historico
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        self._abrir_dialogo_detalhe(equip_id)

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

    # DIÁLOGO DETALHE (reutiliza o que já existir no seu projeto)
    def _abrir_dialogo_detalhe(self, equip_id:int):
        try:
            from view.detalheview import DetalheView
        except Exception:
            self._msg_erro("Detalhe não disponível", "A tela de edição/detalhe não está configurada.")
            return
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
                # atualiza a tela atual
                if self.stacked_widget.currentIndex() == 1:
                    self._consulta_buscar()
                else:
                    self.mostrar_historico()
            else:
                self._msg_erro("Erro", "Não foi possível atualizar.")

    # Navegação
    def voltar(self):
        self.stacked_widget.setCurrentIndex(0)