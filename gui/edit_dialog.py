from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QTextEdit, QDateEdit, QDialogButtonBox
from PyQt5.QtCore import QDate

class EditFilmDialog(QDialog):
    def __init__(self, film_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Film Entry")
        self.setup_ui(film_data)
        
    def setup_ui(self, film_data):
        layout = QFormLayout()
        
        # Form fields
        self.title_input = QLineEdit(film_data[0])
        self.director_input = QLineEdit(film_data[1])
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, QDate.currentDate().year())
        self.year_input.setValue(int(film_data[2]))
        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 10)
        self.rating_input.setValue(int(film_data[3]))
        self.comments_input = QTextEdit(film_data[4])
        self.watch_date_input = QDateEdit(QDate.fromString(film_data[5], "yyyy-MM-dd"))
        
        # Add to layout
        layout.addRow("Title:", self.title_input)
        layout.addRow("Director:", self.director_input)
        layout.addRow("Year:", self.year_input)
        layout.addRow("Rating:", self.rating_input)
        layout.addRow("Watch Date:", self.watch_date_input)
        layout.addRow("Comments:", self.comments_input)
        
        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def get_updated_data(self):
        return [
            self.title_input.text().strip(),
            self.director_input.text().strip(),
            str(self.year_input.value()),
            str(self.rating_input.value()),
            self.comments_input.toPlainText().strip(),
            self.watch_date_input.date().toString("yyyy-MM-dd")
        ]