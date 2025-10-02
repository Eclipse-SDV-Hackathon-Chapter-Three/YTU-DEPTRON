"""Application configuration settings"""

# MQTT Settings for Zenoh
# ZENOH_MQTT_BROKER = "192.168.89.250"
ZENOH_MQTT_BROKER = "127.0.0.1"
ZENOH_MQTT_PORT = 1883
ZENOH_MQTT_TOPICS = {
    "speed": "EGOVehicle/0/0/2/8001",
    "obstacles": "vehicle/obstacles",
    "sleep_detection": "vehicle/sleep",
    "coordinates": "vehicle/coordinates"
}

# Display Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Vehicle Dashboard System"

# Speed Gauge Settings
SPEED_MAX = 260
SPEED_UNIT = "km/h"

# Obstacle Detection Settings
OBSTACLE_RANGE = 360  # degrees
OBSTACLE_MAX_DISTANCE = 100  # meters

# Colors
COLOR_BACKGROUND = "#0f0f0f"
COLOR_PANEL_BG = "#1a1a1a"
COLOR_TEXT = "#e0e0e0"
COLOR_WARNING = "#ff3333"
COLOR_NORMAL = "#33ff33"
COLOR_OBSTACLE = "#ffaa00"