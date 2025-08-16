# model/equipment_model.py
import sqlite3

class EquipmentModel:
    def __init__(self, db_path="equipamentos.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._criar_tabela()
        self._migrar_data_cadastro()
        self._sanear_tags_e_deduplicar()
        self._garantir_indices()

    def _criar_tabela(self):
        """
        Cria a tabela caso não exista. Em bases novas, já cria com data_cadastro.
        Em bases antigas (sem a coluna), a migração é feita em _migrar_data_cadastro.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,                -- pode estar sem NOT NULL em bases antigas
                nome TEXT NOT NULL,
                descricao TEXT,
                data_cadastro TEXT       -- coluna de data
            )
        ''')
        self.conn.commit()

    def _migrar_data_cadastro(self):
        """
        Se a coluna data_cadastro não existir, adiciona SEM default (limitação do SQLite)
        e preenche os registros antigos com datetime('now').
        """
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(equipamentos);")
        colunas = [row[1] for row in cursor.fetchall()]
        if "data_cadastro" not in colunas:
            cursor.execute("ALTER TABLE equipamentos ADD COLUMN data_cadastro TEXT;")
            self.conn.commit()
            cursor.execute("UPDATE equipamentos SET data_cadastro = datetime('now') WHERE data_cadastro IS NULL;")
            self.conn.commit()

    def _sanear_tags_e_deduplicar(self):
        """
        - Converte tags vazias/espaços para NULL (evita conflito no UNIQUE).
        - Remove duplicatas mantendo o registro MAIS RECENTE (maior id) e apagando os antigos.
        Depois disso já é seguro criar o índice UNIQUE.
        """
        c = self.conn.cursor()

        # 1) Normalizar: tag vazia vira NULL
        c.execute("UPDATE equipamentos SET tag = NULL WHERE tag IS NULL OR TRIM(tag) = '';")
        self.conn.commit()

        # 2) Encontrar tags duplicadas (não nulas)
        c.execute("""
            SELECT tag
            FROM equipamentos
            WHERE tag IS NOT NULL
            GROUP BY tag
            HAVING COUNT(*) > 1;
        """)
        dups = [row[0] for row in c.fetchall()]

        # 3) Para cada tag duplicada, manter o MAIS RECENTE (maior id) e apagar os outros
        for tag in dups:
            c.execute("SELECT id FROM equipamentos WHERE tag = ? ORDER BY id DESC;", (tag,))
            ids = [r[0] for r in c.fetchall()]
            manter = ids[0]
            apagar = ids[1:]
            if apagar:
                c.executemany("DELETE FROM equipamentos WHERE id = ?;", [(i,) for i in apagar])
        self.conn.commit()

    def _garantir_indices(self):
        """
        Cria índices. O UNIQUE em tag será aplicado agora que as duplicatas foram sanadas.
        Observação: em SQLite, UNIQUE permite múltiplos NULLs, então linhas antigas com tag NULL não quebram o índice.
        """
        c = self.conn.cursor()
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_equipamentos_tag ON equipamentos(tag);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_equipamentos_nome ON equipamentos(nome);")
        self.conn.commit()

    def adicionar_equipamento(self, tag, nome, descricao):
        """
        Adiciona um equipamento. Lança sqlite3.IntegrityError se TAG já existir.
        """
        tag = (tag or "").strip()
        nome = (nome or "").strip()
        descricao = (descricao or "").strip()

        if not tag or not nome:
            # Deixe o controller validar e mostrar mensagem. Aqui só garantimos consistência.
            raise sqlite3.IntegrityError("Tag e Nome são obrigatórios.")

        c = self.conn.cursor()
        # Grava data por código (portabilidade; não dependemos de DEFAULT em schema)
        c.execute('''
            INSERT INTO equipamentos (tag, nome, descricao, data_cadastro)
            VALUES (?, ?, ?, datetime('now'))
        ''', (tag, nome, descricao))
        self.conn.commit()
        return True

    def listar_equipamentos(self):
        c = self.conn.cursor()
        c.execute('''
            SELECT tag, nome, descricao, COALESCE(data_cadastro, "")
            FROM equipamentos
            ORDER BY id DESC
        ''')
        return c.fetchall()

    def buscar_por_tag_ou_nome(self, termo):
        c = self.conn.cursor()
        termo_like = f"%{(termo or '').strip()}%"
        c.execute('''
            SELECT tag, nome, descricao, COALESCE(data_cadastro, "")
            FROM equipamentos
            WHERE tag LIKE ? OR nome LIKE ?
            ORDER BY id DESC
        ''', (termo_like, termo_like))
        return c.fetchall()