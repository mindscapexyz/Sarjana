from pathlib import Path

from PySide6.QtCore import QDir, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QWidget


class PdfViewerDialog(QWidget):
    def __init__(self, path: Path):
        super().__init__()
        self.setWindowTitle("Research Paper Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.browser = QWebEngineView(self)
        self._pdf_path = path
        layout = QHBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)
        self.init_viewer()

    def init_viewer(self):

        app_dir = QDir.currentPath()

        viewer_path = QDir(app_dir).filePath("ext/PDF_js/PDF_js/web/viewer.html")
        viewer_url = QUrl.fromLocalFile(viewer_path)
        self.browser.load(viewer_url)
        self.load_pdf()

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("PDF files (*.pdf)")
        dialog.setWindowTitle("Open PDF File")
        if dialog.exec() == QFileDialog.Accepted:
            pdf_path = dialog.selectedFiles()[0]
            if pdf_path:
                self.load_pdf()

    def load_pdf(self):
        encoded_pdf_url = QUrl.fromLocalFile(self._pdf_path).toString()
        full_url = f"{self.browser.url().toString()}?file={encoded_pdf_url}"
        print(full_url)
        self.browser.setUrl(QUrl(full_url))
