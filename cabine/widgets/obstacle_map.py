"""Obstacle detection map widget - center of screen"""
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath


class ObstacleMap(QWidget):
    """360-degree obstacle detection display"""
    
    def __init__(self):
        super().__init__()
        self.obstacles = []  # List of {angle: float, distance: float}
        self.max_distance = 100  # meters
        self.setMinimumSize(400, 400)
        
    def add_obstacle(self, angle, distance):
        """Add or update obstacle at given angle"""
        # Remove old obstacle at same angle
        self.obstacles = [obs for obs in self.obstacles if abs(obs['angle'] - angle) > 5]
        
        if distance > 0 and distance <= self.max_distance:
            self.obstacles.append({'angle': angle, 'distance': distance})
        
        # Keep only recent obstacles (max 360)
        if len(self.obstacles) > 360:
            self.obstacles = self.obstacles[-360:]
        
        self.update()
    
    def clear_obstacles(self):
        """Clear all obstacles"""
        self.obstacles.clear()
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        side = min(width, height)
        
        painter.translate(width / 2, height / 2)
        painter.scale(side / 450.0, side / 450.0)
        
        self._draw_background(painter)
        self._draw_grid(painter)
        self._draw_vehicle(painter)
        self._draw_obstacles(painter)
        self._draw_labels(painter)
    
    def _draw_background(self, painter):
        """Draw radar background"""
        painter.setBrush(QColor(20, 20, 30))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(-200, -200, 400, 400)
        
        painter.setPen(QPen(QColor(60, 60, 80), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(-195, -195, 390, 390)
    
    def _draw_grid(self, painter):
        """Draw radar grid circles"""
        painter.setPen(QPen(QColor(40, 40, 60), 1))
        
        for i in range(1, 5):
            radius = i * 50
            painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        
        # Draw angle lines
        for angle in range(0, 360, 45):
            angle_rad = math.radians(angle)
            x = 200 * math.cos(angle_rad)
            y = 200 * math.sin(angle_rad)
            painter.drawLine(QPointF(0, 0), QPointF(x, y))
    
    def _draw_vehicle(self, painter):
        """Draw vehicle at center"""
        painter.setBrush(QColor(0, 200, 100))
        painter.setPen(QPen(QColor(0, 255, 150), 2))
        
        # Draw triangle representing vehicle (pointing up)
        vehicle_path = QPainterPath()
        vehicle_path.moveTo(0, -20)
        vehicle_path.lineTo(-15, 15)
        vehicle_path.lineTo(15, 15)
        vehicle_path.closeSubpath()
        painter.drawPath(vehicle_path)
    
    def _draw_obstacles(self, painter):
        """Draw detected obstacles"""
        painter.setBrush(QColor(255, 170, 0))
        painter.setPen(QPen(QColor(255, 200, 50), 2))
        
        for obstacle in self.obstacles:
            angle = obstacle['angle']
            distance = obstacle['distance']
            
            # Convert to radar coordinates (0° = top, clockwise)
            angle_rad = math.radians(angle - 90)
            
            # Scale distance to radar size
            scaled_distance = (distance / self.max_distance) * 190
            
            x = scaled_distance * math.cos(angle_rad)
            y = scaled_distance * math.sin(angle_rad)
            
            # Draw obstacle as circle
            size = 8
            painter.drawEllipse(QPointF(x, y), size, size)
    
    def _draw_labels(self, painter):
        """Draw direction labels"""
        painter.setPen(QColor(150, 150, 170))
        font = QFont("Arial", 10, QFont.Weight.Bold)
        painter.setFont(font)
        
        # North
        painter.drawText(-10, -210, 20, 20, Qt.AlignmentFlag.AlignCenter, "N")
        # East
        painter.drawText(200, -10, 20, 20, Qt.AlignmentFlag.AlignCenter, "E")
        # South
        painter.drawText(-10, 200, 20, 20, Qt.AlignmentFlag.AlignCenter, "S")
        # West
        painter.drawText(-220, -10, 20, 20, Qt.AlignmentFlag.AlignCenter, "W")
