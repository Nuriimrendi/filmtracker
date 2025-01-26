from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDateEdit, QDialogButtonBox
from PyQt5.QtCore import QDate

class EditWatchlistDialog(QDialog):
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Watchlist Entry")
        self.setup_ui(item_data)
        
    def setup_ui(self, item_data):
        layout = QFormLayout()
        
        self.title_input = QLineEdit(item_data[0])
        self.date_input = QDateEdit(QDate.fromString(item_data[1], "yyyy-MM-dd"))
        
        layout.addRow("Title:", self.title_input)
        layout.addRow("Added Date:", self.date_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def get_updated_data(self):
        return [
            self.title_input.text().strip(),
            self.date_input.date().toString("yyyy-MM-dd")
        ]