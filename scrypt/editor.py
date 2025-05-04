from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class PageTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page_height = 792  # Full page height in pixels
        self.margin_top_bottom = 72
        self.page_content_height = self.page_height - 2 * self.margin_top_bottom

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self.viewport())
        painter.setPen(QColor(180, 180, 180, 160))  # Light gray line

        layout = self.document().documentLayout()
        doc_height = int(self.document().size().height())  # height in layout units (usually pixels)

        y_offset = -self.verticalScrollBar().value()  # Adjust for scroll position

        page_y = self.page_content_height
        while page_y < doc_height:
            # Use document margin to account for the top margin
            y = self.document().documentMargin() + page_y + y_offset
            painter.drawLine(0, int(y), self.viewport().width(), int(y))
            page_y += self.page_content_height
