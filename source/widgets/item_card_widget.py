from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QMouseEvent
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from source.models.pdf_data_model import Pdf
from source.views.pdf_viewer_dialog import PdfViewerDialog
from source.widgets.note_widget import NoteWidgetDialog


class ItemCardWidget(QWidget):
    def __init__(self, pdf: Pdf):
        super().__init__()
        layout = QVBoxLayout()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("ItemCardWidget")

        paper_metadata = pdf.metadata
        authors = paper_metadata["authors"]
        all_names = ""
        for author in authors:
            name = author.get("full_name")
            all_names += name + ", "

        # TODO: HS: 4.7.2024
        # Fix authors data shape

        self.year_label = ResearchYearLabel(str(paper_metadata["year"]))
        self.title_label = ResearchTitleLabel(paper_metadata["title"])
        self.authors_label = AuthorsLabel(all_names)
        self.abstraction_label = ResearchAbstractLabel(paper_metadata["abstract"])
        self._pdf = pdf

        layout.addWidget(self.year_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.authors_label)
        layout.addWidget(self.abstraction_label)

        layout.setSpacing(0)

        self.setLayout(layout)
        self.setFixedHeight(300)
        self.setFixedWidth(250)

        self.setStyleSheet(
            """
            ResearchTitleLabel {
            font-size: 24px;
            font-family: 'Trebuchet MS', sans-serif;
            margin: 0px;
            padding: 0px;
            }

            ResearchYearLabel {
            color: #868786;
            background-color: #e6e7e7;
            padding: 2px;  /* Adjust padding to reduce excess background */
            margin: 0px;
            font-weight: bold;
            border-radius: 5px;
            }

            AuthorsLabel {
            color: #5d5c5d;
            margin: 0px;
            padding: 0px;
            }

            ResearchAbstractLabel {
            margin: 0px;
            padding: 0px;
            color: #a5a5a4;
            }
        """
        )

        self.is_selected = False

        self._pdf_dialog = PdfViewerDialog(self._pdf.path)
        self._pdf_dialog.hide()
        self._note_widget = NoteWidgetDialog(self._pdf)
        self._note_widget.hide()

    def mousePressEvent(self, event):
        # self.clicked.emit()  # Emit clicked signal
        self.toggle_selection()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self._pdf_dialog.show()
        self._pdf_dialog.load_pdf()
        self._note_widget.show()

        return super().mouseDoubleClickEvent(event)

    def toggle_selection(self):
        self.is_selected = not self.is_selected
        if self.is_selected:
            self.setStyleSheet(
                """
                #ItemCardWidget {
                    border: 2px solid #8edf91;
                }
            ResearchTitleLabel {
            font-size: 24px;
            font-family: 'Trebuchet MS', sans-serif;
            margin: 0px;
            padding: 0px;
            }

            ResearchYearLabel {
            color: #868786;
            background-color: #e6e7e7;
            padding: 2px;  /* Adjust padding to reduce excess background */
            margin: 0px;
            font-weight: bold;
            border-radius: 5px;
            }

            AuthorsLabel {
            color: #5d5c5d;
            margin: 0px;
            padding: 0px;
            }

            ResearchAbstractLabel {
            margin: 0px;
            padding: 0px;
            color: #a5a5a4;
            }
        """
            )
        else:
            self.setStyleSheet(
                """

            ResearchTitleLabel {
            font-size: 24px;
            font-family: 'Trebuchet MS', sans-serif;
            margin: 0px;
            padding: 0px;
            }

            ResearchYearLabel {
            color: #868786;
            background-color: #e6e7e7;
            padding: 2px;  /* Adjust padding to reduce excess background */
            margin: 0px;
            font-weight: bold;
            border-radius: 5px;
            }

            AuthorsLabel {
            color: #5d5c5d;
            margin: 0px;
            padding: 0px;
            }

            ResearchAbstractLabel {
            margin: 0px;
            padding: 0px;
            color: #a5a5a4;
            }
        """
            )


class ResearchTitleLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self._original_text = text
        self._width = 100
        self.update_text()
        self.setWordWrap(True)
        self.setMaximumHeight(90)
        self.updateWidth()
        self.setContentsMargins(0, 0, 0, 0)

    def update_text(self):
        # Create a QFontMetrics object to measure text dimensions
        metrics = QFontMetrics(self.font())
        wrapped_lines = self.wrap_text(self._original_text, self._width, metrics)
        if len(wrapped_lines) > 3:
            display_text = "\n".join(wrapped_lines[:3]) + "..."
        else:
            display_text = "\n".join(wrapped_lines)
        self.setText(display_text)

    def wrap_text(self, text, width, metrics):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            if metrics.horizontalAdvance(test_line) <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def updateWidth(self):
        metrics = QFontMetrics(self.font())
        text_height = metrics.height()

        self.setFixedHeight(text_height * 5)


class AuthorsLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setWordWrap(True)
        self.updateWidth()
        self.setContentsMargins(0, 0, 0, 0)

    def updateWidth(self):
        metrics = QFontMetrics(self.font())
        text_height = metrics.height()


        self.setFixedHeight(text_height - 3)


class ResearchYearLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setAutoFillBackground(True)
        self.setWordWrap(True)
        self.updateWidth()
        self.setContentsMargins(0, 0, 0, 0)

    def setText(self, text):
        super().setText(text)
        self.updateWidth()

    def updateWidth(self):
        metrics = QFontMetrics(self.font())
        text_width = metrics.horizontalAdvance(self.text())
        text_height = metrics.height()

        self.setFixedWidth(text_width + 10)
        self.setFixedHeight(text_height)


class ResearchAbstractLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self._original_text = text
        self._width = 200
        self.setWordWrap(True)
        self.updateWidth()
        self.update_text()
        self.setContentsMargins(0, 0, 0, 0)

    def updateWidth(self):
        metrics = QFontMetrics(self.font())
        text_height = metrics.height()

        self.setFixedHeight(text_height * 8)

    def update_text(self):
        metrics = QFontMetrics(self.font())
        wrapped_lines = self.wrap_text(self._original_text, self._width, metrics)
        if len(wrapped_lines) > 8:
            display_text = "\n".join(wrapped_lines[:8]) + "..."
        else:
            display_text = "\n".join(wrapped_lines)
        self.setText(display_text)

    def wrap_text(self, text, width, metrics):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            if metrics.horizontalAdvance(test_line) <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))
        return lines
