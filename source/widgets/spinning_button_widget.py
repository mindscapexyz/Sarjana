from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QPushButton


class SpinningButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self._default_text = text
        self.angle = 0
        self.is_spinning = False

    def paintEvent(self, event):
        if not self.is_spinning:
            super().paintEvent(event)
        else:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.translate(self.width() / 2, self.height() / 2)
            painter.rotate(self.angle)

            for i in range(8):
                painter.rotate(45)
                painter.drawRect(-2, -10, 4, 10)

    def spin(self):
        self.is_spinning = True
        self.setText("")
        self.spin_timer = QTimer(self)
        self.spin_timer.timeout.connect(self.update_spin)
        self.spin_timer.start(50)

    def update_spin(self):
        self.angle = (self.angle + 30) % 360
        self.update()

    def stop_spin(self):
        self.spin_timer.stop()
        self.is_spinning = False
        self.setText(self._default_text)
        self.update()
