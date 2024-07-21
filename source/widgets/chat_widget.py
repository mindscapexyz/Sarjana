from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget


class ChatWidget(QWidget):
    """Basic interface to chat with PDF"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.chatDisplay = QTextEdit()
        self.chatDisplay.setReadOnly(True)
        layout.addWidget(self.chatDisplay)

        inputLayout = QHBoxLayout()
        self.inputField = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(self.sendMessage)
        inputLayout.addWidget(self.inputField)
        inputLayout.addWidget(self.sendButton)

        layout.addLayout(inputLayout)
        self.setLayout(layout)

        self.setWindowTitle("Chat Widget")
        self.setGeometry(300, 300, 300, 400)

    def sendMessage(self):
        message = self.inputField.text()
        if message:
            message = message + "\n\n"
            self.chatDisplay.append(f"You: {message}")
            self.inputField.clear()
            # TODO: Add here
            # Here you would typically send the message to a server
            # and handle the response
