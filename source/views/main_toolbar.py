from pathlib import Path

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QSizePolicy, QToolBar, QToolButton, QWidget

from source.common.enums.icon import Icon
from source.services.services import Services


class MainToolBar(QToolBar):
    """Main toolbar"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Main toolbar")

        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        add_pdf_button = QToolButton()
        add_pdf_button.setIcon(QIcon(Icon.PLUS.value))
        add_pdf_button.clicked.connect(self.on_add_pdf_button_pressed)

        self.addWidget(spacer_widget)
        self.addWidget(add_pdf_button)

    @Slot()
    def on_add_pdf_button_pressed(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("PDF files (*.pdf)")
        dialog.setWindowTitle("Open PDF File")
        if dialog.exec():
            pdf_path = dialog.selectedFiles()[0]
            if pdf_path:
                pdf_path = Path(pdf_path)
                documents = Services().pdf().load_pdf(pdf_path)
                first_page_text = Services().pdf().get_first_page_pdf_text(pdf_path)
                metadata = Services().llm().parse_research_paper_metadata(first_page_text)
                pdf = Services().pdf().create_pdf_obj(pdf_path, documents, metadata)
                Services().pdf().append_data(pdf_path.name, pdf)
                Services().file_handling().save_pdf_obj_as_json(pdf_path.name, pdf)
