from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                            QSpinBox, QTextEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QDateEdit, QHBoxLayout, QLabel, QMessageBox, QApplication, QHeaderView, QAction, QDialog)
from PyQt5.QtCore import Qt, QDate
from .edit_dialog import EditFilmDialog

class WatchedTab(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()
        self.setup_context_menu()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, director, or comments...")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        self.setup_form(layout)
        self.setup_table(layout)
        self.setLayout(layout)
        self.load_data()

    def filter_table(self):
        search_text = self.search_input.text().lower().strip()
        
        for row in range(self.table.rowCount()):
            match = False
            # Check these columns: Title(0), Director(1), Comments(4)
            for col in [0, 1, 4]:
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)
            
    def setup_context_menu(self):
        self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(self.edit_selected_film)
        self.table.addAction(edit_action)
    
    def edit_selected_film(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            original_data = [
                self.table.item(selected_row, col).text() 
                for col in range(self.table.columnCount())
            ]
            
            dialog = EditFilmDialog(original_data, self)
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_updated_data()
                
                if self.data_manager.update_watched_film(original_data, new_data):
                    self.load_data()
    
    def setup_form(self, layout):
        form = QFormLayout()
        
        # Form elements
        self.title_input = QLineEdit()
        self.director_input = QLineEdit()
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, QDate.currentDate().year())
        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 10)
        self.comments_input = QTextEdit()
        self.watch_date_input = QDateEdit()
        self.watch_date_input.setDate(QDate.currentDate())
        
        # Add rows to form
        form.addRow(QLabel("Title:"), self.title_input)
        form.addRow(QLabel("Director:"), self.director_input)
        form.addRow(QLabel("Year:"), self.year_input)
        form.addRow(QLabel("Rating (1-10):"), self.rating_input)
        form.addRow(QLabel("Watch Date:"), self.watch_date_input)
        form.addRow(QLabel("Comments:"), self.comments_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Film")
        self.add_button.clicked.connect(self.add_film)
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.clicked.connect(self.clear_form)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(form)
        layout.addLayout(button_layout)
    
    def setup_table(self, layout):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Title", "Director", "Year", 
            "Rating", "Comments", "Watch Date"
        ])
        
        # Set column width policies
        self.table.setColumnWidth(0, 200)   # Title
        self.table.setColumnWidth(1, 150)   # Director
        self.table.setColumnWidth(2, 80)    # Year
        self.table.setColumnWidth(3, 80)    # Rating
        self.table.setColumnWidth(5, 120)   # Watch Date
        
        # Comments column gets remaining space
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Additional formatting
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Enable word wrap for comments
        self.table.setWordWrap(True)
        self.table.setTextElideMode(Qt.ElideRight)
        
        layout.addWidget(self.table)
        # Set alternating row colors
        self.table.setAlternatingRowColors(True)
        
    def load_data(self):
        self.table.setRowCount(0)  # Clear existing data
        films = self.data_manager.get_watched_films()
        
        self.table.setRowCount(len(films))
        for row_idx, film in enumerate(films):
            for col_idx, value in enumerate(film):
                item = QTableWidgetItem(value)
                if col_idx in (2, 3):  # Year and Rating columns
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.DisplayRole, int(value))
                self.table.setItem(row_idx, col_idx, item)
        
        # Adjust columns after loading
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        
    def clear_form(self):
        self.title_input.clear()
        self.director_input.clear()
        self.year_input.setValue(QDate().year())
        self.rating_input.setValue(3)
        self.comments_input.clear()
        self.watch_date_input.setDate(QDate.currentDate())
    
    def add_film(self):
        film_data = [
            self.title_input.text().strip(),
            self.director_input.text().strip(),
            str(self.year_input.value()),
            str(self.rating_input.value()),
            self.comments_input.toPlainText().strip(),
            self.watch_date_input.date().toString("yyyy-MM-dd")
        ]
        
        if not film_data[0]:
            QMessageBox.warning(self, "Error", "Title is required!")
            return
            
        if self.data_manager.add_watched_film(film_data):
            self.load_data()
            self.clear_form()
            # Explicitly process events to update UI
            QApplication.processEvents()
    
    def setup_context_menu(self):
        self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        # Edit action
        self.edit_action = QAction("Edit Entry", self)
        self.edit_action.triggered.connect(self.edit_selected_film)
        self.table.addAction(self.edit_action)
        
        # Delete action
        self.delete_action = QAction("Delete Entry", self)
        self.delete_action.triggered.connect(self.delete_selected_film)
        self.table.addAction(self.delete_action)

    def delete_selected_film(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            film_data = [
                self.table.item(selected_row, col).text() 
                for col in range(self.table.columnCount())
            ]
            
            if self.data_manager.delete_watched_film(film_data):
                self.load_data()
