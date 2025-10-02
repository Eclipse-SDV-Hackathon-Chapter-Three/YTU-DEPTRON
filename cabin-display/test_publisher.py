"""Test MQTT publisher for Zenoh"""
import paho.mqtt.publish as publish
import json
import time
import random
import math


def publish_test_data():
    """Publish test data to all topics"""
    speed = 0
    angle = 0
    sleep_state = 0
    sleep_counter = 0
    
    print("Publishing test data to Zenoh MQTT broker...")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            # Speed (0-260)
            speed += random.uniform(-5, 8)
            speed = max(0, min(260, speed))
            publish.single("vehicle/speed", str(speed), hostname="localhost")
            
            # Obstacles (360 degree scan)
            for _ in range(5):  # 5 obstacles per iteration
                obstacle_angle = random.uniform(0, 360)
                obstacle_distance = random.uniform(10, 80)
                obstacle_data = json.dumps({
                    "angle": obstacle_angle,
                    "distance": obstacle_distance
                })
                publish.single("vehicle/obstacles", obstacle_data, hostname="localhost")
            
            # Sleep detection (toggle every 10 seconds)
            sleep_counter += 1
            if sleep_counter >= 50:  # Toggle every 5 seconds (50 * 0.1s)
                sleep_state = 1 if sleep_state == 0 else 0
                sleep_counter = 0
            publish.single("vehicle/sleep", str(sleep_state), hostname="localhost")
            
            # Coordinates
            coord_data = json.dumps({
                "initial": round(random.uniform(0, 100), 2),
                "at_moment": round(random.uniform(0, 100), 2),
                "final": round(random.uniform(0, 100), 2)
            })
            publish.single("vehicle/coordinates", coord_data, hostname="localhost")
            
            print(f"Speed: {speed:.1f} | Sleep: {sleep_state} | Obstacles published")
            
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            print("\nTest publisher stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    publish_test_data()
