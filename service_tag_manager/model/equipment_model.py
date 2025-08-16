import sqlite3

class EquipmentModel:
    def __init__(self, db_path="equipamentos.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._criar_tabela()
        self._migrar_colunas()
        self._sanear_tags_e_deduplicar()
        self._garantir_indices()

    def _criar_tabela(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS equipamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                nome TEXT NOT NULL,
                descricao TEXT,
                data_cadastro TEXT
            )
        """)
        self.conn.commit()

    def _migrar_colunas(self):
        c = self.conn.cursor()
        c.execute("PRAGMA table_info(equipamentos);")
        cols = {row[1] for row in c.fetchall()}

        add_cols = []
        for col_sql in [
            ("data_cadastro",      "TEXT"),
            ("cliente",            "TEXT"),
            ("modelo",             "TEXT"),
            ("serial",             "TEXT"),
            ("tipo_servico",       "TEXT"),
            ("status",             "TEXT"),
            ("prioridade",         "TEXT"),
            ("proxima_manutencao", "TEXT"),
            ("custo",              "REAL"),
            ("garantia_meses",     "INTEGER"),
            ("observacoes",        "TEXT"),
        ]:
            if col_sql[0] not in cols:
                add_cols.append(f"ALTER TABLE equipamentos ADD COLUMN {col_sql[0]} {col_sql[1]};")

        for sql in add_cols:
            c.execute(sql)
        self.conn.commit()

        c.execute("UPDATE equipamentos SET data_cadastro = COALESCE(data_cadastro, datetime('now')) WHERE data_cadastro IS NULL;")
        self.conn.commit()

    def _sanear_tags_e_deduplicar(self):
        c = self.conn.cursor()
        c.execute("UPDATE equipamentos SET tag = NULL WHERE tag IS NULL OR TRIM(tag) = '';")
        self.conn.commit()
        c.execute("""
            SELECT tag FROM equipamentos
            WHERE tag IS NOT NULL
            GROUP BY tag HAVING COUNT(*) > 1;
        """)
        dups = [r[0] for r in c.fetchall()]
        for tag in dups:
            c.execute("SELECT id FROM equipamentos WHERE tag = ? ORDER BY id DESC;", (tag,))
            ids = [r[0] for r in c.fetchall()]
            manter, apagar = ids[0], ids[1:]
            if apagar:
                c.executemany("DELETE FROM equipamentos WHERE id = ?;", [(i,) for i in apagar])
        self.conn.commit()

    def _garantir_indices(self):
        c = self.conn.cursor()
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_equip_tag ON equipamentos(tag);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_equip_nome ON equipamentos(nome);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_equip_cliente ON equipamentos(cliente);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_equip_status ON equipamentos(status);")
        self.conn.commit()

    # --- CRUD ---
    def adicionar_equipamento(self, tag, nome, descricao, cliente, modelo, serial,
                              tipo_servico, status, prioridade, proxima_manutencao,
                              custo, garantia_meses, observacoes):
        if not tag or not nome or not cliente:
            raise sqlite3.IntegrityError("Tag, Nome e Cliente são obrigatórios.")
        tag = tag.strip(); nome = nome.strip(); cliente = cliente.strip()
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO equipamentos
            (tag, nome, descricao, data_cadastro, cliente, modelo, serial,
             tipo_servico, status, prioridade, proxima_manutencao, custo,
             garantia_meses, observacoes)
            VALUES (?, ?, ?, datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tag, nome, (descricao or ""), cliente, (modelo or ""), (serial or ""),
              (tipo_servico or ""), (status or ""), (prioridade or ""),
              (proxima_manutencao or ""), float(custo or 0), int(garantia_meses or 0),
              (observacoes or "")))
        self.conn.commit()
        return c.lastrowid

    def obter_por_id(self, equip_id:int):
        c = self.conn.cursor()
        c.execute("""
            SELECT id, tag, nome, cliente, modelo, serial, descricao, tipo_servico,
                   status, prioridade, proxima_manutencao, custo, garantia_meses,
                   observacoes, data_cadastro
            FROM equipamentos WHERE id = ?
        """, (equip_id,))
        return c.fetchone()

    def atualizar_basico(self, equip_id:int, status:str, prioridade:str, proxima_manutencao:str, observacoes:str):
        c = self.conn.cursor()
        c.execute("""
            UPDATE equipamentos
               SET status = ?, prioridade = ?, proxima_manutencao = ?, observacoes = ?
             WHERE id = ?
        """, (status or "", prioridade or "", proxima_manutencao or "", observacoes or "", equip_id))
        self.conn.commit()
        return c.rowcount > 0

    def excluir(self, equip_id:int):
        c = self.conn.cursor()
        c.execute("DELETE FROM equipamentos WHERE id = ?", (equip_id,))
        self.conn.commit()
        return c.rowcount > 0

    # --- Buscas ---
    def buscar_simples(self, termo=""):
        """Consulta (com id primeiro): por tag/nome/cliente/modelo."""
        c = self.conn.cursor()
        where = []; params = []
        termo = (termo or "").strip()
        if termo:
            like = f"%{termo}%"
            where.append("(tag LIKE ? OR nome LIKE ? OR cliente LIKE ? OR modelo LIKE ?)")
            params += [like, like, like, like]

        sql = """
            SELECT id, COALESCE(tag,''), COALESCE(nome,''), COALESCE(cliente,''), COALESCE(modelo,''),
                   COALESCE(descricao,''), COALESCE(tipo_servico,''), COALESCE(status,''),
                   COALESCE(prioridade,''), COALESCE(proxima_manutencao,''), COALESCE(data_cadastro,'')
            FROM equipamentos
        """
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY id DESC"

        c.execute(sql, params)
        return c.fetchall()

    def buscar_avancado(self, termo="", status="", tipo="", prioridade="",
                        cliente="", modelo="", data_ini="", data_fim="",
                        prox_ini="", prox_fim=""):
        """Histórico (com id primeiro)."""
        c = self.conn.cursor()
        where = []; params = []

        if termo:
            like = f"%{termo}%"
            where.append("(tag LIKE ? OR nome LIKE ? OR cliente LIKE ? OR modelo LIKE ?)")
            params += [like, like, like, like]
        if status:
            where.append("status = ?"); params.append(status)
        if tipo:
            where.append("tipo_servico = ?"); params.append(tipo)
        if prioridade:
            where.append("prioridade = ?"); params.append(prioridade)
        if cliente:
            where.append("cliente LIKE ?"); params.append(f"%{cliente}%")
        if modelo:
            where.append("modelo LIKE ?"); params.append(f"%{modelo}%")
        if data_ini:
            where.append("date(data_cadastro) >= date(?)"); params.append(data_ini)
        if data_fim:
            where.append("date(data_cadastro) <= date(?)"); params.append(data_fim)
        if prox_ini:
            where.append("date(COALESCE(proxima_manutencao,'')) >= date(?)"); params.append(prox_ini)
        if prox_fim:
            where.append("date(COALESCE(proxima_manutencao,'')) <= date(?)"); params.append(prox_fim)

        sql = """
            SELECT id, COALESCE(tag,''), COALESCE(nome,''), COALESCE(cliente,''), COALESCE(modelo,''),
                   COALESCE(status,''), COALESCE(prioridade,''), COALESCE(proxima_manutencao,''), COALESCE(data_cadastro,'')
            FROM equipamentos
        """
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY id DESC"

        c.execute(sql, params)
        return c.fetchall()