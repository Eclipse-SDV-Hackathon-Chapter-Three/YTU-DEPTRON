
# Experiment with SAC to drive on the Carla simulator.

## Overview

The training of the SAC policy was done with https://github.com/zihaosheng/VLM-RL

- observation space: steer, throttle, speed, rgb_camera
- action space: steer, throttle


## SAC policy video driving in Carla simulator

[![SAC Policy Video](https://img.youtube.com/vi/gQlz7sNyhC4/0.jpg)](https://youtu.be/gQlz7sNyhC4)


## Run instructions
### Start ankaios for the mqtt_broker and ustreamer
```
sudo systemctl start ank-server ank-agent
```

### Run Carla
```
~/carla-simulator/CarlaUE4.sh -prefernvidia -quality-level=Epic -carla-rpc-port=2000 -RenderOffScreen
```

### Run the control with the SAC policy
```
uv run python manual_control_sensors.py \
    --host 127.0.0.1 --port 2000 \
    --res 640x480 \
    --filter vehicle.audi.etron \
    --rolename ego_vehicle \
    --router 127.0.0.1
```

### get data from the vehicle
```
RUST_LOG=debug cargo run --release -- --ego-vehicle-role ego_vehicle --router 127.0.0.1
```

### Debugging all topics
```
mosquitto_sub -v -h 127.0.0.1 -p 1883 -t '#'
```

