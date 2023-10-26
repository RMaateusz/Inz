from gui_py.gui import Window
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    if window.button_clicked():
        window.create_dialog()
    sys.exit(app.exec())
