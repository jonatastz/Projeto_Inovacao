import sqlite3

class EquipmentModel:
    def __init__(self):
        self.conn = sqlite3.connect("equipamentos.db")
        self._criar_tabela()

    def _criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                nome TEXT,
                descricao TEXT
            )
        ''')
        self.conn.commit()

    def adicionar_equipamento(self, tag, nome, descricao):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO equipamentos (tag, nome, descricao)
            VALUES (?, ?, ?)
        ''', (tag, nome, descricao))
        self.conn.commit()

    def listar_equipamentos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT tag, nome, descricao FROM equipamentos')
        return cursor.fetchall()

    def buscar_por_tag_ou_nome(self, termo):
        cursor = self.conn.cursor()
        termo_like = f"%{termo}%"
        cursor.execute('''
            SELECT tag, nome, descricao
            FROM equipamentos
            WHERE tag LIKE ? OR nome LIKE ?
        ''', (termo_like, termo_like))
        return cursor.fetchall()