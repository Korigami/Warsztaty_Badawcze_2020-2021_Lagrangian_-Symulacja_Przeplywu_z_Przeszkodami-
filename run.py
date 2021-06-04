from PyQt5.QtWidgets import QApplication
from Interfejs.aplikacja_okienkowa import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = StartWindow()
    sys.exit(app.exec_())
