import sys

from PySide6.QtWidgets import QApplication

from source.models.model_store import ModelStore
from source.services.services import Services
from source.views.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ModelStore()
    Services()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
