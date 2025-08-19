
import sqlite3

class EquipmentModel:
    def __init__(self, db_path="equipamentos.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._criar_tabelas()
        self._garantir_indices()

    def _criar_tabelas(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS equipamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                descricao TEXT,
                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
                cliente TEXT,
                modelo TEXT,
                serial TEXT,
                tipo_servico TEXT,
                status TEXT,
                prioridade TEXT,
                proxima_manutencao TEXT,
                custo REAL,
                garantia_meses INTEGER,
                observacoes TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipamento_id INTEGER NOT NULL,
                data_servico TEXT DEFAULT CURRENT_TIMESTAMP,
                tipo TEXT,
                descricao TEXT,
                tecnico TEXT,
                status TEXT,
                custo REAL,
                garantia_meses INTEGER,
                observacoes TEXT,
                FOREIGN KEY(equipamento_id) REFERENCES equipamentos(id) ON DELETE CASCADE
            )
        """ )
        self.conn.commit()

    def _garantir_indices(self):
        c = self.conn.cursor()
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_eq_tag ON equipamentos(tag);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_eq_nome ON equipamentos(nome);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_eq_cliente ON equipamentos(cliente);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_eq_status ON equipamentos(status);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_serv_equip ON servicos(equipamento_id);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_serv_data ON servicos(data_servico);")
        self.conn.commit()

    # ===== Equipamentos =====
    def adicionar_equipamento(self, tag, nome, descricao=None, cliente=None, modelo=None, serial=None,
                              tipo_servico=None, status=None, prioridade=None, proxima_manutencao=None,
                              custo=None, garantia_meses=None, observacoes=None):
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO equipamentos
            (tag, nome, descricao, cliente, modelo, serial, tipo_servico, status, prioridade,
             proxima_manutencao, custo, garantia_meses, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tag, nome, descricao or "", cliente or "", modelo or "", serial or "",
               tipo_servico or "", status or "", prioridade or "", proxima_manutencao or "",
               float(custo or 0.0), int(garantia_meses or 0), observacoes or ""))
        self.conn.commit()
        return c.lastrowid

    def atualizar_equipamento(self, equip_id:int, **kwargs):
        if not kwargs:
            return False
        cols = []
        vals = []
        for k, v in kwargs.items():
            cols.append(f"{k} = ?")
            vals.append(v if v is not None else "")
        vals.append(equip_id)
        sql = f"UPDATE equipamentos SET {', '.join(cols)} WHERE id = ?"
        c = self.conn.cursor()
        c.execute(sql, vals)
        self.conn.commit()
        return c.rowcount > 0

    def excluir_equipamento(self, equip_id:int):
        c = self.conn.cursor()
        c.execute("DELETE FROM equipamentos WHERE id = ?", (equip_id,))
        self.conn.commit()
        return c.rowcount > 0

    def obter_por_id(self, equip_id:int):
        c = self.conn.cursor()
        c.execute("""
            SELECT id, tag, nome, cliente, modelo, serial, descricao, tipo_servico, status, prioridade,
                   proxima_manutencao, custo, garantia_meses, observacoes, data_cadastro
            FROM equipamentos WHERE id = ?
        """, (equip_id,))
        return c.fetchone()

    def consultar(self, termo=None, tag=None, nome=None, cliente=None, modelo=None,
                  status=None, tipo=None, prioridade=None, prox_ini=None, prox_fim=None):
        where = []
        params = []
        if termo:
            like = f"%{termo}%"
            where.append("(tag LIKE ? OR nome LIKE ? OR cliente LIKE ? OR modelo LIKE ?)")
            params += [like, like, like, like]
        if tag: where.append("tag LIKE ?") or params.append(f"%{tag}%")
        if nome: where.append("nome LIKE ?") or params.append(f"%{nome}%")
        if cliente: where.append("cliente LIKE ?") or params.append(f"%{cliente}%")
        if modelo: where.append("modelo LIKE ?") or params.append(f"%{modelo}%")
        if status: where.append("status = ?") or params.append(status)
        if tipo: where.append("tipo_servico = ?") or params.append(tipo)
        if prioridade: where.append("prioridade = ?") or params.append(prioridade)
        if prox_ini: where.append("date(COALESCE(proxima_manutencao,'')) >= date(?)") or params.append(prox_ini)
        if prox_fim: where.append("date(COALESCE(proxima_manutencao,'')) <= date(?)") or params.append(prox_fim)

        sql = """
            SELECT id, COALESCE(tag,''), COALESCE(nome,''), COALESCE(cliente,''), COALESCE(modelo,''),
                   COALESCE(descricao,''), COALESCE(tipo_servico,''), COALESCE(status,''), COALESCE(prioridade,''),
                   COALESCE(proxima_manutencao,''), COALESCE(data_cadastro,'')
            FROM equipamentos
        """
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY id DESC"
        c = self.conn.cursor()
        c.execute(sql, params)
        return c.fetchall()

    # ===== Serviços =====
    def adicionar_servico(self, equipamento_id:int, data_servico=None, tipo=None, descricao=None,
                          tecnico=None, status=None, custo=None, garantia_meses=None, observacoes=None):
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO servicos (equipamento_id, data_servico, tipo, descricao, tecnico, status, custo, garantia_meses, observacoes)
            VALUES (?, COALESCE(?, CURRENT_TIMESTAMP), ?, ?, ?, ?, ?, ?, ?)
        """, (equipamento_id, data_servico, tipo or "", descricao or "", tecnico or "",
                status or "", float(custo or 0.0), int(garantia_meses or 0), observacoes or ""))
        self.conn.commit()
        return c.lastrowid

    def listar_servicos_por_equipamento(self, equipamento_id:int):
        c = self.conn.cursor()
        c.execute("""
            SELECT id, equipamento_id, COALESCE(data_servico,''), COALESCE(tipo,''), COALESCE(descricao,''),
                   COALESCE(tecnico,''), COALESCE(status,''), COALESCE(custo,0.0), COALESCE(garantia_meses,0),
                   COALESCE(observacoes,'')
            FROM servicos
            WHERE equipamento_id = ?
            ORDER BY date(COALESCE(data_servico,'')) DESC, id DESC
        """, (equipamento_id,))
        return c.fetchall()
