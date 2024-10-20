from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

Form, Window = uic.loadUiType("dialog.ui")

d = mama

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()
