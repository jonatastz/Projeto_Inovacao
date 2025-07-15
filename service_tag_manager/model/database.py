import sqlite3

class Database:
    def __init__(self, db_name="equipments.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_tag TEXT NOT NULL UNIQUE,
                equipment_name TEXT NOT NULL,
                description TEXT,
                date_added TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_equipment(self, service_tag, name, description):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO equipment (service_tag, equipment_name, description) VALUES (?, ?, ?)",
                       (service_tag, name, description))
        self.conn.commit()

    def get_all_equipments(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM equipment")
        return cursor.fetchall()