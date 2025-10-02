"""Speed gauge widget - left quarter of screen"""
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QRadialGradient, QPainterPath


class SpeedGauge(QWidget):
    """Speed gauge displaying 0-260 km/h"""
    
    def __init__(self):
        super().__init__()
        self.speed = 0.0
        self.max_speed = 260
        self.setMinimumSize(350, 350)
        
    def set_speed(self, speed):
        """Set current speed"""
        self.speed = max(0, min(speed, self.max_speed))
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        side = min(width, height)
        
        painter.translate(width / 2, height / 2)
        painter.scale(side / 400.0, side / 400.0)
        
        self._draw_background(painter)
        self._draw_scale(painter)
        self._draw_needle(painter)
        self._draw_center(painter)
        self._draw_digital_display(painter)
    
    def _draw_background(self, painter):
        """Draw gauge background"""
        gradient = QRadialGradient(0, 0, 200)
        gradient.setColorAt(0, QColor(35, 35, 45))
        gradient.setColorAt(0.8, QColor(25, 25, 35))
        gradient.setColorAt(1, QColor(15, 15, 25))
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(-180, -180, 360, 360)
        
        painter.setPen(QPen(QColor(70, 70, 90), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(-175, -175, 350, 350)
    
    def _draw_scale(self, painter):
        """Draw speed scale markings"""
        painter.setPen(QPen(QColor(200, 200, 220), 2))
        font = QFont("Arial", 11, QFont.Weight.Bold)
        painter.setFont(font)
        
        for i in range(0, int(self.max_speed) + 1, 20):
            angle = 225 - (i / self.max_speed * 270)
            angle_rad = math.radians(angle)
            
            inner_radius = 140
            outer_radius = 160
            
            if i % 40 == 0:
                painter.setPen(QPen(QColor(255, 255, 255), 3))
            else:
                painter.setPen(QPen(QColor(150, 150, 170), 2))
            
            x1 = inner_radius * math.cos(angle_rad)
            y1 = inner_radius * math.sin(angle_rad)
            x2 = outer_radius * math.cos(angle_rad)
            y2 = outer_radius * math.sin(angle_rad)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            
            if i % 40 == 0:
                text_radius = 115
                text_x = text_radius * math.cos(angle_rad)
                text_y = text_radius * math.sin(angle_rad)
                painter.setPen(QColor(220, 220, 240))
                painter.drawText(int(text_x - 20), int(text_y - 10), 40, 20,
                               Qt.AlignmentFlag.AlignCenter, str(i))
    
    def _draw_needle(self, painter):
        """Draw speed needle"""
        needle_angle = 225 - (self.speed / self.max_speed * 270)
        needle_rad = math.radians(needle_angle)
        
        painter.setBrush(QColor(255, 50, 50))
        painter.setPen(QPen(QColor(200, 0, 0), 2))
        
        needle_path = QPainterPath()
        needle_path.moveTo(0, 0)
        needle_path.lineTo(8 * math.cos(needle_rad + math.pi/2),
                          8 * math.sin(needle_rad + math.pi/2))
        needle_path.lineTo(130 * math.cos(needle_rad),
                          130 * math.sin(needle_rad))
        needle_path.lineTo(8 * math.cos(needle_rad - math.pi/2),
                          8 * math.sin(needle_rad - math.pi/2))
        needle_path.closeSubpath()
        painter.drawPath(needle_path)
    
    def _draw_center(self, painter):
        """Draw center circle"""
        painter.setBrush(QColor(80, 80, 100))
        painter.setPen(QPen(QColor(150, 150, 170), 2))
        painter.drawEllipse(-12, -12, 24, 24)
    
    def _draw_digital_display(self, painter):
        """Draw digital speed display"""
        painter.setPen(QColor(0, 255, 100))
        font = QFont("Arial", 32, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(-60, 50, 120, 45, Qt.AlignmentFlag.AlignCenter,
                        f"{self.speed:.1f}")
        
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor(180, 180, 200))
        painter.drawText(-60, 90, 120, 20, Qt.AlignmentFlag.AlignCenter, "km/h")