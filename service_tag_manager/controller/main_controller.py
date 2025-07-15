class MainController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.connect_signals()

    def connect_signals(self):
        self.view.btn_add.clicked.connect(self.add_equipment)
        self.load_equipments()

    def add_equipment(self):
        tag = self.view.input_tag.text()
        name = self.view.input_name.text()
        desc = self.view.input_desc.toPlainText()
        if tag and name:
            self.model.add_equipment(tag, name, desc)
            self.view.clear_inputs()
            self.load_equipments()

    def load_equipments(self):
        self.view.table.clearContents()
        equipments = self.model.list_equipments()
        self.view.populate_table(equipments)