"""Main dashboard window"""
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt
from widgets.speed_gauge import SpeedGauge
from widgets.obstacle_map import ObstacleMap
from widgets.info_panel import InfoPanel
# from mqtt.zenoh_client import ZenohMQTTClient
import paho.mqtt.client as mqtt
from config import *


class DashboardWindow(QMainWindow):
    """Main dashboard window with all widgets"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setStyleSheet(f"background-color: {COLOR_BACKGROUND};")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create widgets
        self.speed_gauge = SpeedGauge()
        self.obstacle_map = ObstacleMap()
        self.info_panel = InfoPanel()
        
        # Set parents
        self.speed_gauge.setParent(central_widget)
        self.obstacle_map.setParent(central_widget)
        self.info_panel.setParent(central_widget)
        
        # Setup MQTT
        self._setup_mqtt()
        
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    def _setup_mqtt(self):
        """Setup MQTT client and connect signals"""
        # self.mqtt_client = ZenohMQTTClient(ZENOH_MQTT_BROKER, ZENOH_MQTT_PORT)
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        def on_connect(client, userdata, flags, reason_code, properties):
            print(f"Connected with result code {reason_code}")
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("#")

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload.decode()))
            self._on_speed_received(float(msg.payload.decode()))

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        
        # Add topics
        # for topic in ZENOH_MQTT_TOPICS.values():
            # print(f"Subscribing to topic: {topic}")
            # self.mqtt_client.add_topic(topic)
        self.mqtt_client.connect("127.0.0.1", 1883, 60)
        
        # Connect signals
        # self.mqtt_client.speed_received.connect(self._on_speed_received)
        # self.mqtt_client.obstacle_received.connect(self._on_obstacle_received)
        # self.mqtt_client.sleep_detected.connect(self._on_sleep_detected)
        # self.mqtt_client.coordinates_received.connect(self._on_coordinates_received)
        
        # # Start MQTT client
        # self.mqtt_client.start()

        thread = self.mqtt_client.loop_start()
    
    def _on_speed_received(self, speed):
        """Handle speed data"""
        print(speed)

        self.speed_gauge.set_speed(speed)
    
    def _on_obstacle_received(self, data):
        """Handle obstacle data"""
        angle = data.get('angle', 0)
        distance = data.get('distance', 0)
        self.obstacle_map.add_obstacle(angle, distance)
    
    def _on_sleep_detected(self, status):
        """Handle sleep detection"""
        self.info_panel.set_sleep_detection(status)
    
    def _on_coordinates_received(self, data):
        """Handle coordinates data"""
        initial = data.get('initial', 0.0)
        at_moment = data.get('at_moment', 0.0)
        final = data.get('final', 0.0)
        self.info_panel.set_coordinates(initial, at_moment, final)
    
    def resizeEvent(self, event):
        """Handle window resize"""
        width = self.width()
        height = self.height()
        
        # Left quarter: Speed gauge
        quarter_width = width // 4
        self.speed_gauge.setGeometry(20, 20, quarter_width - 40, height - 40)
        
        # Center half: Obstacle map
        map_size = min(width // 2 - 60, height - 40)
        map_x = quarter_width + (width // 2 - map_size) // 2
        self.obstacle_map.setGeometry(map_x, 20, map_size, height - 40)
        
        # Right quarter: Info panel
        right_start = quarter_width + width // 2
        self.info_panel.setGeometry(right_start + 20, 20, 
                                    quarter_width - 40, height - 40)
    
    def closeEvent(self, event):
        """Handle window close"""
        self.mqtt_client.stop()
        self.mqtt_client.wait()
        event.accept()
