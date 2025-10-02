"""Zenoh MQTT client for receiving vehicle data"""
import json
from PyQt6.QtCore import QThread, pyqtSignal
import paho.mqtt.client as mqtt


class ZenohMQTTClient(QThread):
    """MQTT client for Zenoh bridge"""
    
    # Signals for different data types
    speed_received = pyqtSignal(float)
    obstacle_received = pyqtSignal(dict)  # {angle: float, distance: float}
    sleep_detected = pyqtSignal(int)  # 0 or 1
    coordinates_received = pyqtSignal(dict)  # {initial: float, final: float, at_moment: float}
    
    def __init__(self, broker="192.168.89.250", port=1883):
        super().__init__()
        self.broker = broker
        self.port = port
        self.client = None
        self.running = True
        self.topics = []
        
    def add_topic(self, topic):
        """Add a topic to subscribe"""
        self.topics.append(topic)
    
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback when connected to broker"""
        if rc == 0:
            print(f"Connected to Zenoh MQTT Broker: {self.broker}:{self.port}")
            for topic in self.topics:
                client.subscribe(topic)
                print(f"Subscribed to: {topic}")
        else:
            print(f"Connection failed with code: {rc}")
    
    def on_message(self, client, userdata, msg):
        """Callback when message received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode()
            
            # Parse based on topic
            if "speed" in topic:
                speed = float(payload)
                self.speed_received.emit(speed)
                
            elif "obstacles" in topic:
                data = json.loads(payload)
                self.obstacle_received.emit(data)
                
            elif "sleep" in topic:
                sleep_status = int(payload)
                self.sleep_detected.emit(sleep_status)
                
            elif "coordinates" in topic:
                data = json.loads(payload)
                self.coordinates_received.emit(data)
                
        except Exception as e:
            print(f"Error parsing message: {e}")
    
    def run(self):
        """Run MQTT client loop"""
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            while self.running:
                self.msleep(100)
                
        except Exception as e:
            print(f"MQTT connection error: {e}")
    
    def stop(self):
        """Stop MQTT client"""
        self.running = False
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()