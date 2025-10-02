"""Information panel widget - right quarter of screen"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath


class InfoPanel(QWidget):
    """Right panel showing sleep detection and coordinates"""
    
    def __init__(self):
        super().__init__()
        self.sleep_detected = 0  # 0 or 1
        self.coord_initial = 0.0
        self.coord_at_moment = 0.0
        self.coord_final = 0.0
        self.setMinimumSize(300, 600)
        
    def set_sleep_detection(self, status):
        """Set sleep detection status (0 or 1)"""
        self.sleep_detected = status
        self.update()
    
    def set_coordinates(self, initial, at_moment, final):
        """Set coordinate values"""
        self.coord_initial = initial
        self.coord_at_moment = at_moment
        self.coord_final = final
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Background
        painter.fillRect(0, 0, width, height, QColor(20, 20, 30))
        
        # Draw sleep detection (top half)
        self._draw_sleep_detection(painter, width, height // 2)
        
        # Draw coordinate bars (bottom half)
        self._draw_coordinate_bars(painter, width, height)
    
    def _draw_sleep_detection(self, painter, width, height):
        """Draw sleep detection indicator"""
        panel_height = height
        margin = 20
        
        # Draw panel background
        painter.setPen(QPen(QColor(60, 60, 80), 2))
        painter.setBrush(QColor(30, 30, 45))
        painter.drawRoundedRect(margin, margin, 
                               width - 2 * margin, 
                               panel_height - 2 * margin, 10, 10)
        
        # Title
        painter.setPen(QColor(180, 180, 200))
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(margin, margin + 30, width - 2 * margin, 30,
                        Qt.AlignmentFlag.AlignCenter, "SLEEP DETECTION")
        
        # Warning icon (triangle)
        if self.sleep_detected == 1:
            # Alert mode - red
            color = QColor(255, 50, 50)
            text = "DETECT SLEEP"
            text_color = QColor(255, 50, 50)
        else:
            # Normal mode - dim
            color = QColor(80, 80, 100)
            text = "DETECT SLEEP"
            text_color = QColor(100, 100, 120)
        
        # Draw warning triangle
        center_x = width // 2
        center_y = margin + 100
        size = 50
        
        painter.setBrush(color)
        painter.setPen(QPen(color.lighter(120), 3))
        
        triangle = QPainterPath()
        triangle.moveTo(center_x, center_y - size)
        triangle.lineTo(center_x - size, center_y + size)
        triangle.lineTo(center_x + size, center_y + size)
        triangle.closeSubpath()
        painter.drawPath(triangle)
        
        # Draw exclamation mark
        if self.sleep_detected == 1:
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(center_x - 4, center_y - 25, 8, 30)
            painter.drawEllipse(center_x - 5, center_y + 15, 10, 10)
        
        # Status text
        painter.setPen(text_color)
        font = QFont("Arial", 14, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(margin, center_y + 80, width - 2 * margin, 40,
                        Qt.AlignmentFlag.AlignCenter, text)
    
    def _draw_coordinate_bars(self, painter, width, height):
        """Draw coordinate bars at bottom"""
        start_y = height // 2 + 40
        margin = 20
        bar_height = 50
        spacing = 70
        
        painter.setPen(QColor(180, 180, 200))
        font = QFont("Arial", 10, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Title
        painter.drawText(margin, start_y - 20, width - 2 * margin, 20,
                        Qt.AlignmentFlag.AlignCenter, "COORDINATES")
        
        # Draw three bars
        coords = [
            ("At the Moment", self.coord_at_moment, QColor(0, 200, 255)),
            ("Initial", self.coord_initial, QColor(100, 200, 100)),
            ("Final", self.coord_final, QColor(255, 150, 50))
        ]
        
        for i, (label, value, color) in enumerate(coords):
            y_pos = start_y + i * spacing
            
            # Label
            painter.setPen(QColor(150, 150, 170))
            painter.drawText(margin, y_pos, width - 2 * margin, 15,
                           Qt.AlignmentFlag.AlignLeft, label)
            
            # Bar background
            bar_y = y_pos + 20
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(40, 40, 50))
            painter.drawRoundedRect(margin, bar_y, 
                                   width - 2 * margin, bar_height, 5, 5)
            
            # Value text
            painter.setPen(QColor(255, 255, 255))
            font_val = QFont("Arial", 16, QFont.Weight.Bold)
            painter.setFont(font_val)
            painter.drawText(margin, bar_y, width - 2 * margin, bar_height,
                           Qt.AlignmentFlag.AlignCenter, f"{value:.2f}")

