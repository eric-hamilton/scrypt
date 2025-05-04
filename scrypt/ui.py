from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QListWidget, QVBoxLayout, QWidget, QShortcut
)
from PyQt5.QtGui import QTextBlockFormat, QTextCharFormat, QFont

from PyQt5.QtCore import Qt, QTimer
from scrypt.editor import PageTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrypt")

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Start creating...")
        self.last_element_type = None

        # Double-enter detection
        self.last_key_was_enter = False

        # Element chooser popup
        self.element_popup = QListWidget()
        self.element_popup.addItems([
            "Scene Heading", "Action", "Character", 
            "Dialogue", "Parenthetical", "Transition"
        ])
        self.element_popup.hide()
        self.element_popup.setWindowFlags(Qt.Popup)
        self.element_popup.itemClicked.connect(self.insert_element_click)
        self.element_popup.keyPressEvent = self.element_popup_keypress

        # Container with gray background
        outer = QWidget()
        outer.setStyleSheet("background-color: #cccccc;")  # Light gray like an editor

        # Editor setup
        self.editor = PageTextEdit()
        self.editor.setFixedWidth(612)  # Approx 8.5 inches at 72dpi
        self.editor.setStyleSheet("background-color: white; padding: 1in; font-family: Courier; font-size: 12pt;")
        self.editor.setLineWrapMode(QTextEdit.WidgetWidth)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.editor)
        outer.setLayout(layout)

        self.setCentralWidget(outer)

    def reset_enter_counter(self):
        self.enter_counter = 0

    def eventFilter(self, source, event):
        if source == self.editor and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return:
                if self.last_key_was_enter:
                    # Undo the last newline
                    cursor = self.editor.textCursor()
                    cursor.movePosition(cursor.PreviousBlock, cursor.KeepAnchor)
                    cursor.removeSelectedText()
                    cursor.deleteChar()  # Ensure block break is gone
                    self.editor.setTextCursor(cursor)

                    self.show_element_popup()
                    self.last_key_was_enter = False
                    return True
                else:
                    self.last_key_was_enter = True
                    self.handle_auto_next_element()
                    return False
            else:
                self.last_key_was_enter = False
        return super().eventFilter(source, event)


    def handle_auto_next_element(self):
        if self.last_element_type == "Character":
            self.insert_element("Dialogue")
        elif self.last_element_type == "Scene Heading":
            self.insert_element("Action")
        elif self.last_element_type == "Dialogue":
            self.insert_element("Action")
        else:
            self.insert_element("General")


    def show_element_popup(self):
        cursor_rect = self.editor.cursorRect()
        global_pos = self.editor.mapToGlobal(cursor_rect.bottomLeft())
        self.element_popup.move(global_pos)
        self.element_popup.setCurrentRow(0)
        self.element_popup.show()
        self.element_popup.setFocus()

    def element_popup_keypress(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            current_item = self.element_popup.currentItem()
            if current_item:
                self.insert_element(current_item.text())
        else:
            QListWidget.keyPressEvent(self.element_popup, event)

    def insert_element_click(self, item):
        self.insert_element(item.text())

    def insert_element(self, element_type):
        self.element_popup.hide()
        self.last_element_type = element_type

        cursor = self.editor.textCursor()

        block_format = QTextBlockFormat()
        char_format = QTextCharFormat()
        font = QFont("Courier", 12)
        char_format.setFont(font)

        if element_type == "Scene Heading":
            block_format.setAlignment(Qt.AlignLeft)
            block_format.setLeftMargin(0)
            char_format.setFontWeight(QFont.Bold)
        elif element_type == "Action":
            block_format.setAlignment(Qt.AlignLeft)
            block_format.setLeftMargin(0)
        elif element_type == "Character":
            block_format.setAlignment(Qt.AlignLeft)
            block_format.setLeftMargin(150)
            char_format.setFontCapitalization(QFont.AllUppercase)
        elif element_type == "Dialogue":
            block_format.setAlignment(Qt.AlignLeft)
            block_format.setLeftMargin(100)
        elif element_type == "Parenthetical":
            block_format.setAlignment(Qt.AlignLeft)
            block_format.setLeftMargin(120)
        elif element_type == "Transition":
            block_format.setAlignment(Qt.AlignRight)
        elif element_type == "General":
            block_format.setAlignment(Qt.AlignLeft)
            block_format.setLeftMargin(0)

        cursor.insertBlock(block_format, char_format)
        self.editor.setFocus()


