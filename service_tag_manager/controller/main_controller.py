
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from view.service_dialog import ServiceDialog
from view.service_history_dialog import ServiceHistoryDialog
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
        v.btn_editar.clicked.connect(self._abrir_detalhe_selecionado)
        v.btn_excluir.clicked.connect(self._excluir_selecionado)
        v.btn_limpar.clicked.connect(self._consulta_limpar)
        v.btn_buscar.clicked.connect(self._consulta_buscar)
        v.btn_novo_servico.clicked.connect(self._novo_servico_consulta)
        v.table_resultados.itemDoubleClicked.connect(lambda *_: self._mostrar_historico_do_selecionado('consulta'))

        # Historico
        h = self.historico_view
        h.btn_voltar_historico.clicked.connect(self.voltar)
        h.btn_editar_h.clicked.connect(self._abrir_detalhe_selecionado_hist)
        h.btn_excluir_h.clicked.connect(self._excluir_selecionado_hist)
        h.btn_novo_servico_h.clicked.connect(self._novo_servico_historico)
        h.table_historico.itemDoubleClicked.connect(lambda *_: self._mostrar_historico_do_selecionado('historico'))

    # Utils
    def _msg_info(self, title, text):
        QMessageBox.information(self.stacked_widget, title, text)

    def _msg_erro(self, title, text):
        QMessageBox.critical(self.stacked_widget, title, text)

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
        if not tag or not nome:
            self._msg_erro("Campos obrigatórios", "Informe ao menos Tag e Nome.")
            return
        try:
            equip_id = self.model.adicionar_equipamento(
                tag=tag, nome=nome,
                descricao=(mv.input_desc.toPlainText() or ""),
                cliente=(mv.input_cliente.text() or ""),
                modelo=(mv.input_modelo.text() or ""),
                serial=(mv.input_serial.text() or ""),
                tipo_servico=mv.combo_tipo_servico.currentText(),
                status=mv.combo_status.currentText(),
                prioridade=mv.combo_prioridade.currentText(),
                proxima_manutencao=mv.date_proxima.date().toString("yyyy-MM-dd"),
                custo=float(mv.input_custo.value()),
                garantia_meses=int(mv.input_garantia_meses.value()),
                observacoes=(mv.input_observacoes.toPlainText() or ""),
            )
            self._msg_info("Sucesso", f"Equipamento cadastrado (ID {equip_id}).")
            mv.clear_inputs()
        except Exception as e:
            self._msg_erro("Erro", f"Falha ao cadastrar: {e}")

    # CONSULTA
    def mostrar_consulta(self):
        self.stacked_widget.setCurrentIndex(1)
        # Não buscar automaticamente: tabela vazia até o usuário clicar em Buscar
        try:
            t = self.consulta_view.table_resultados
            t.setRowCount(0)
        except Exception:
            pass
        try:
            self.consulta_view.lbl_count.setText("0 resultados")
        except Exception:
            pass

    def _consulta_limpar(self):
        v = self.consulta_view
        v.input_termo.clear()
        v.combo_status.setCurrentIndex(0)
        v.combo_prioridade.setCurrentIndex(0)
        self._consulta_buscar()

    def _consulta_buscar(self):
        v = self.consulta_view
        rows = self.model.consultar(
            termo=(v.input_termo.text() or "").strip(),
            status=v.combo_status.currentText() or None,
            prioridade=v.combo_prioridade.currentText() or None,
        )
        t = v.table_resultados
        t.setRowCount(0)
        for r in rows:
            row = t.rowCount(); t.insertRow(row)
            for col, val in enumerate(r):
                t.setItem(row, col, QTableWidgetItem(str(val if val is not None else "")))
        v.lbl_count.setText(f"{t.rowCount()} resultados")

    def _abrir_detalhe_selecionado(self):
        t = self.consulta_view.table_resultados
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        rec = self.model.obter_por_id(equip_id)
        if not rec: return
        dlg = DetalheView(self.stacked_widget)
        dlg.load_from_record(rec)
        if dlg.exec_():
            vals = dlg.values()
            ok = self.model.atualizar_equipamento(
                vals["id"],
                status=vals["status"],
                prioridade=vals["prioridade"],
                proxima_manutencao=vals["proxima_manutencao"],
                custo=vals["custo"],
                garantia_meses=vals["garantia_meses"],
                descricao=vals["descricao"],
                observacoes=vals["observacoes"]
            )
            if ok:
                self._msg_info("Salvo", "Atualizado com sucesso.")
                self._consulta_buscar()
            else:
                self._msg_erro("Erro", "Não foi possível atualizar.")

    def _excluir_selecionado(self):
        t = self.consulta_view.table_resultados
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        if QMessageBox.question(self.stacked_widget, "Confirmar", "Excluir este equipamento?") == QMessageBox.Yes:
            if self.model.excluir_equipamento(equip_id):
                self._consulta_buscar()

    # HISTÓRICO
    def mostrar_historico(self):
        self.stacked_widget.setCurrentIndex(2)
        # Reusa a consulta para listar
        rows = self.model.consultar()
        t = self.historico_view.table_historico
        t.setRowCount(0)
        for r in rows:
            i = t.rowCount(); t.insertRow(i)
            for col, val in enumerate([r[0], r[1], r[2], r[3], r[4], r[7], r[8], r[9], r[10]]):
                t.setItem(i, col, QTableWidgetItem(str(val or "")))
        self.historico_view.lbl_count_h.setText(f"{t.rowCount()} resultados")

    def _abrir_detalhe_selecionado_hist(self):
        t = self.historico_view.table_historico
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        rec = self.model.obter_por_id(equip_id)
        if not rec: return
        dlg = DetalheView(self.stacked_widget)
        dlg.load_from_record(rec)
        if dlg.exec_():
            vals = dlg.values()
            ok = self.model.atualizar_equipamento(
                vals["id"],
                status=vals["status"],
                prioridade=vals["prioridade"],
                proxima_manutencao=vals["proxima_manutencao"],
                custo=vals["custo"],
                garantia_meses=vals["garantia_meses"],
                descricao=vals["descricao"],
                observacoes=vals["observacoes"]
            )
            if ok:
                self._msg_info("Salvo", "Atualizado com sucesso.")
                self.mostrar_historico()
            else:
                self._msg_erro("Erro", "Não foi possível atualizar.")

    def _excluir_selecionado_hist(self):
        t = self.historico_view.table_historico
        row = t.currentRow()
        if row < 0: return
        equip_id = self._linha_para_id(t, row)
        if not equip_id: return
        if QMessageBox.question(self.stacked_widget, "Confirmar", "Excluir este equipamento?") == QMessageBox.Yes:
            if self.model.excluir_equipamento(equip_id):
                self.mostrar_historico()

    # ===== Serviços (Histórico) =====
    def _selected_equipment_from_table(self, table):
        row = table.currentRow()
        if row < 0:
            return None, None
        id_item = table.item(row, 0)
        tag_item = table.item(row, 1)
        nome_item = table.item(row, 2)
        equip_id = int(id_item.text()) if id_item and id_item.text().isdigit() else None
        label = f"[{tag_item.text() if tag_item else ''}] {nome_item.text() if nome_item else ''}".strip()
        return equip_id, label

    def _novo_servico_consulta(self):
        t = self.consulta_view.table_resultados
        equip_id, label = self._selected_equipment_from_table(t)
        if not equip_id:
            self._msg_erro("Seleção necessária", "Selecione um equipamento na lista.")
            return
        dlg = ServiceDialog(self.stacked_widget, equip_label=label)
        if dlg.exec_():
            vals = dlg.values()
            self.model.adicionar_servico(equip_id, **vals)
            self._msg_info("Registrado", "Serviço adicionado ao histórico.")

    def _novo_servico_historico(self):
        t = self.historico_view.table_historico
        equip_id, label = self._selected_equipment_from_table(t)
        if not equip_id:
            self._msg_erro("Seleção necessária", "Selecione um equipamento na lista.")
            return
        dlg = ServiceDialog(self.stacked_widget, equip_label=label)
        if dlg.exec_():
            vals = dlg.values()
            self.model.adicionar_servico(equip_id, **vals)
            self._msg_info("Registrado", "Serviço adicionado ao histórico.")

    def _mostrar_historico_do_selecionado(self, origem='consulta'):
        t = self.consulta_view.table_resultados if origem=='consulta' else self.historico_view.table_historico
        equip_id, label = self._selected_equipment_from_table(t)
        if not equip_id:
            self._msg_erro("Seleção necessária", "Selecione um equipamento.")
            return
        rows = self.model.listar_servicos_por_equipamento(equip_id)
        dlg = ServiceHistoryDialog(self.stacked_widget, equip_label=label, rows=rows)
        dlg.exec_()

    # Navegação
    def voltar(self):
        self.stacked_widget.setCurrentIndex(0)
