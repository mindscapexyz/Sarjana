import datetime

from PySide6.QtCore import Qt, QThreadPool, QTimer, Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QLabel, QScrollArea, QTextEdit, QVBoxLayout, QWidget

from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.services import Services
from source.services.llm_service_runner import LLMServiceRunner
from source.widgets.spinning_button_widget import SpinningButton


class NoteWidgetDialog(QWidget):
    def __init__(self, pdf: Pdf):
        super().__init__()
        self._pdf = pdf
        # TODO: HS: 7.7.2024
        # maybe only need key to pdf instead of passing pdf obj
        self._thread_pool = QThreadPool()
        self._title = self.add_line_breaks(pdf.metadata["title"])
        self._pdf_model_store = ModelStore().pdf()
        self._pdf_model_store.summaries_added.connect(self.on_summaries_finished_generated)
        self.initUI()

        # TODO: HS: 12.7.2024
        # stop timer is not working properly

    def initUI(self):
        self.setWindowTitle("Notes")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)

        date_now = datetime.datetime.now()
        date_now = date_now.strftime("%B %d, at %I:%M %p")
        date_label = QLabel(date_now)

        date_label.setStyleSheet("color: #888; margin-bottom: 10px;")
        content_layout.addWidget(date_label)

        title_label = QLabel(self._title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        content_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.note_edit = QTextEdit()
        self.note_edit.clear()
        self.note_edit.setPlaceholderText("Write your notes here...")
        self.note_edit.setStyleSheet("QTextEdit { border: none; }")

        scroll_area.setWidget(self.note_edit)
        content_layout.addWidget(scroll_area)

        self.summary_button = SpinningButton("Generate summary")
        self.summary_button.setStyleSheet("background-color: white; border: 1px solid #ddd; padding: 5px 10px;")
        self.summary_button.clicked.connect(self.on_summary_button_clicked)

        self._word_list = []
        self.summary_button.clicked.connect(self.start_updates)
        self.current_index = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)

        content_layout.addWidget(self.summary_button)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def add_line_breaks(self, text: str, max_length=30):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            if sum(len(w) for w in current_line) + len(current_line) + len(word) <= max_length:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return "\n".join(lines)

    @Slot()
    def on_summary_button_clicked(self):

        pdf = ModelStore().pdf().get_pdf_obj(self._pdf.path.name)
        if pdf is None:
            return
        if not pdf.summaries:
            self.summary_button.spin()

            runner = LLMServiceRunner(pdf)

            self._thread_pool.start(runner, priority=5)
        if pdf.summaries:
            self.summary_button.spin()
            self._summaries = pdf.summaries["output_text"]
            QTimer.singleShot(3000, self._load_summaries)

    @Slot()
    def on_summaries_finished_generated(self, summaries):
        pdf = ModelStore().pdf().get_pdf_obj(self._pdf.path.name)
        self._word_list = summaries.split()
        self.current_index = 0
        self.note_edit.clear()
        self.timer.start(50)  # Update every 1000 ms (1 second)
        self.summary_button.setEnabled(False)

        if pdf:
            Services().file_handling().save_pdf_obj_as_json(self._pdf.path.name, pdf)
        # QTimer.singleShot(3000, self.summary_button.stop_spin)
        self.summary_button.stop_spin()

    def _load_summaries(self):
        self.on_summaries_finished_generated(self._summaries)

    def start_updates(self):
        self.current_index = 0
        self.note_edit.clear()
        self.timer.start(50)  # Update every 1000 ms (1 second)
        self.summary_button.setEnabled(False)

    def update_text(self):
        if self.current_index < len(self._word_list):
            current_text = self.note_edit.toPlainText()
            new_word = self._word_list[self.current_index]
            if current_text:
                updated_text = current_text + " " + new_word
            else:
                updated_text = new_word
            self.note_edit.setPlainText(updated_text)

            cursor = self.note_edit.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.note_edit.setTextCursor(cursor)

            self.current_index += 1
        else:
            self.timer.stop()
            self.summary_button.setEnabled(True)
            self.summary_button.setText("Regenerate summary")
