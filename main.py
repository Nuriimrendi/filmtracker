import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
# main.py

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from gui.main_window import MainWindow

    app = QApplication(sys.argv)
    
    # Soft Orange Theme
    
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
