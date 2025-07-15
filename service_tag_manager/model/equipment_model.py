from .database import Database

class EquipmentModel:
    def __init__(self):
        self.db = Database()

    def add_equipment(self, tag, name, description):
        self.db.insert_equipment(tag, name, description)

    def list_equipments(self):
        return self.db.get_all_equipments()