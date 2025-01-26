from PyQt5.QtWidgets import QMainWindow, QTabWidget
from .watched_tab import WatchedTab
from .watchlist_tab import WatchlistTab
from data_manager import DataManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Film Tracker")
        self.setGeometry(100, 100, 800, 600)
        
        self.data_manager = DataManager()
        self.init_tabs()
        
    def init_tabs(self):
        self.tabs = QTabWidget()
        self.watched_tab = WatchedTab(self.data_manager)
        self.watchlist_tab = WatchlistTab(self.data_manager)
        
        self.tabs.addTab(self.watched_tab, "Watched Films")
        self.tabs.addTab(self.watchlist_tab, "Watchlist")
        
        self.setCentralWidget(self.tabs)
