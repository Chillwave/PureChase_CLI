# PureChase_CLI
Python tools to control the Bluetooth-based mouse cat toy. Replaces the "Instachew" &amp; "Pets Hunt" app.

## Overview

Also known as the Instachew Purechase & the MySudui App Mouse Racer. The original applications were hard to use and did not have the ability to autonomously control the toy.

This project contains two scripts for controlling a Bluetooth cat toy:
1. `wasd_control.py` - Manual control using keyboard
2. `random_mouse.py` - Automated random movement patterns

## Requirements

- Python 3.7+
- Bleak library for Bluetooth LE communication
- Linux-based system

### Installation

```bash
# Install required packages
pip install bleak
```

## WASD Controller (`wasd_control.py`)

Manual control script that allows you to control the toy using keyboard inputs.

### Controls
- `W` - Move Forward
- `A` - Move Left
- `S` - Move Back
- `D` - Move Right
- `Space` - Stop Movement
- `Q` - Quit Program

### Usage
```bash
python wasd_control.py
```

## Random Mouse Simulator (`random_mouse.py`)

Automated script that simulates erratic mouse-like movements.

### Features
- Random directional movements
- Configurable movement and pause durations
- Automatic stop between movements

### Configuration
Adjust these variables in the script to modify behavior:
```python
MIN_MOVEMENT_TIME = 0.2  # Minimum movement duration
MAX_MOVEMENT_TIME = 1.0  # Maximum movement duration
MIN_PAUSE_TIME = 0.1    # Minimum pause between movements
MAX_PAUSE_TIME = 0.5    # Maximum pause between movements
```

### Usage
```bash
python3 random_mouse.py
```
Press `Ctrl+C` to stop the random movement pattern.

## Device Configuration

Both scripts require the Bluetooth address of your device. Update the `DEVICE_ADDRESS` constant in either script:

```python
DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"  # Replace with your device's address
```

## Command Protocol

The toy uses simple byte commands for control:
- `0x01` - Forward
- `0x02` - Back
- `0x03` - Left
- `0x04` - Right
- `0x00` - Stop

## Troubleshooting

1. **Connection Issues**
   - Ensure the device is powered on
   - Verify the Bluetooth address is correct
   - Check that no other devices are connected to the toy

2. **Permission Issues**
   - Ensure you have the necessary permissions for Bluetooth communication
   - You might need to run with sudo or add your user to the bluetooth group

3. **Movement Issues**
   - If movement continues after stopping, try adjusting the delay times
   - Verify that the stop command is being sent properly

## Notes

- The scripts are designed for Linux systems
- Bluetooth LE support is required
- Some systems might require root privileges for Bluetooth access

## Acknowledgments

This project was created through reverse engineering the OEM app's (Pets Hunt) Bluetooth communication protocol.
