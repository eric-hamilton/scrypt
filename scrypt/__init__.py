from PyQt5.QtWidgets import QApplication
import sys
from scrypt.ui import MainWindow

def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
