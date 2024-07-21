from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QMainWindow, QScrollArea, QWidget

from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.services import Services
from source.views.custom_layout import CustomLayout
from source.views.main_toolbar import MainToolBar
from source.widgets.item_card_widget import ItemCardWidget


class MainWindow(QMainWindow):
    """Main window of the app"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sarjana")
        self.setGeometry(100, 100, 1100, 800)

        layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        main_tool_bar = MainToolBar()
        self.addToolBar(main_tool_bar)

        # TODO: HS: 7.7.2024
        # Redesign sidebar
        self.sidebar = QListWidget()
        # self._load_all_sidebar_categories()
        # layout.addWidget(self.sidebar)

        self.main_layout = CustomLayout()
        self._load_local_metadata()

        self.content_widget = QScrollArea()
        self.content_widget.setLayout(self.main_layout)
        layout.addWidget(self.content_widget, 1)  # Give more space for content widget
        self.setStyleSheet(
            """
            ItemCardWidget {
                border: 2px solid #eeefee;
                border-radius: 10px;
                background-color: #feffff;
                margin: 0px;
                padding: 100px;
            }

            QListWidget {
            background-color: #feffff;
            border: 2px solid #eeefee;
            font-family: 'Trebuchet MS', sans-serif;
            }

        """
        )
        ModelStore().pdf().data_added.connect(self.on_pdf_data_added)

    @Slot()
    def on_pdf_data_added(self, key: str):
        paper_metadata = ModelStore().pdf().data.get(key)
        if not paper_metadata:
            return
        self._add_item_card_widget(paper_metadata)

    def _load_local_metadata(self):
        pdf_obj_list = Services().file_handling().read_all_local_pdf_json()
        for pdf_obj in pdf_obj_list:
            self._add_item_card_widget(pdf_obj)
            Services().pdf().append_data(pdf_obj.path.name, pdf_obj)

    def _add_item_card_widget(self, paper: Pdf):
        card = ItemCardWidget(
            paper,
        )
        self.main_layout.addWidget(card)

    def _load_all_sidebar_categories(self):
        # TODO: HS: 4.5.2024
        # Add this into separate widget
        self.sidebar.addItem("Recent")
        self.sidebar.addItem("Bookmarked")
        self.sidebar.addItem("Discover")

        categories = [
            ("Computer Science", "#FF6347"),
            ("Machine learning", "#4682B4"),
            ("Game Development", "#3CB371"),
        ]

        for category, color in categories:
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(color))

            icon = QIcon(pixmap)
            item = QListWidgetItem(icon, category)
            item.setSizeHint(QSize(200, 20)) 

            self.sidebar.addItem(item)
