from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QDateEdit, QHBoxLayout, QLabel, QHeaderView, QAction, QDialog)
from PyQt5.QtCore import Qt, QDate
from .edit_watchlist_dialog import EditWatchlistDialog

class WatchlistTab(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()
        self.setup_context_menu()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add search bar at the top
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search watchlist...")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_input)
        
        # Add search bar first
        layout.addLayout(search_layout)
        
        # Then add form and table
        self.setup_form(layout)
        self.setup_table(layout)
        
        self.setLayout(layout)
        self.load_data()
        
    def filter_table(self):
        search_text = self.search_input.text().lower().strip()
        
        for row in range(self.table.rowCount()):
            match = False
            # Check title column(0)
            item = self.table.item(row, 0)
            if item and search_text in item.text().lower():
                match = True
            self.table.setRowHidden(row, not match)
            
    def setup_context_menu(self):
        self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        # Edit action
        self.edit_action = QAction("Edit Entry", self)
        self.edit_action.triggered.connect(self.edit_selected_item)
        self.table.addAction(self.edit_action)
        
        # Delete action
        self.delete_action = QAction("Delete Entry", self)
        self.delete_action.triggered.connect(self.delete_selected_item)
        self.table.addAction(self.delete_action)
    
    def edit_selected_item(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            original_data = [
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text()
            ]
            
            dialog = EditWatchlistDialog(original_data, self)
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_updated_data()
                
                if self.data_manager.update_watchlist(original_data, new_data):
                    self.load_data()

    def delete_selected_item(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            item_data = [
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text()
            ]
            
            if self.data_manager.delete_watchlist(item_data):
                self.load_data()
    
    def setup_form(self, layout):
        form = QFormLayout()
        
        self.title_input = QLineEdit()
        form.addRow(QLabel("Title:"), self.title_input)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add to Watchlist")
        self.add_button.clicked.connect(self.add_to_watchlist)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(form)
        layout.addLayout(button_layout)
        
    def setup_table(self, layout):
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Title", "Added Date"])
        
        # Set column resize modes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Title expands
        header.setSectionResizeMode(1, QHeaderView.Fixed)    # Date fixed width
        self.table.setColumnWidth(1, 150)  # Fixed width for date column
        
        # Uniform styling
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.setTextElideMode(Qt.ElideRight)
        
        layout.addWidget(self.table)
        # Set alternating row colors
        self.table.setAlternatingRowColors(True)
        
    def load_data(self):
        self.table.setRowCount(0)
        watchlist = self.data_manager.get_watchlist()
        
        self.table.setRowCount(len(watchlist))
        for row_idx, item in enumerate(watchlist):
            # Title column
            title_item = QTableWidgetItem(item[0])
            title_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row_idx, 0, title_item)
            
            # Date column
            date_item = QTableWidgetItem(item[1])
            date_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 1, date_item)
        
        self.table.resizeRowsToContents()

    def clear_form(self):
        self.title_input.clear()
        
    def add_to_watchlist(self):
        title = self.title_input.text().strip()
        if not title:
            return
            
        added_date = QDate.currentDate().toString("yyyy-MM-dd")
        if self.data_manager.add_to_watchlist([title, added_date]):
            self.load_data()
            self.clear_form()