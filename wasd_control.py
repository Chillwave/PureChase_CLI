import asyncio
from bleak import BleakScanner, BleakClient
import sys
import tty
import termios
import contextlib
import time

# Device Configuration
DEVICE_ADDRESS = "B3:04:A6:20:04:34"
MOUSE_WRITE_FUNC_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"

# Control Configuration
DEBUG = True

# Command values
FORWARD = 0x01
BACK = 0x02
LEFT = 0x03
RIGHT = 0x04
STOP = 0x00

def debug_print(message):
    if DEBUG:
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

async def get_key():
    if sys.platform == 'win32':
        raise NotImplementedError("Windows support not implemented")
    else:
        with raw_mode(sys.stdin):
            return sys.stdin.read(1)

class MouseController:
    def __init__(self):
        self.client = None
        self.command_count = 0
        self.current_direction = None

    async def set_mouse_control(self, direction):
        command = None
        debug_print(f"Direction requested: {direction}")

        # Movement commands with correct values
        if direction == 'w':    # Forward
            command = bytes([FORWARD, 0x00])
        elif direction == 's':  # Back
            command = bytes([BACK, 0x00])
        elif direction == 'a':  # Left
            command = bytes([LEFT, 0x00])
        elif direction == 'd':  # Right
            command = bytes([RIGHT, 0x00])
        elif direction == 'stop':
            command = bytes([STOP, 0x00])
        
        if command:
            try:
                # Send the command
                debug_print(f"Sending command: {command.hex()}")
                await self.client.write_gatt_char(MOUSE_WRITE_FUNC_UUID, command)
                self.command_count += 1
                self.current_direction = direction if direction != 'stop' else None
                
                # If it was a movement command, send a stop command after a brief delay
                if direction in ['w', 'a', 's', 'd']:
                    await asyncio.sleep(0.1)  # Brief delay
                    stop_command = bytes([STOP, 0x00])
                    debug_print(f"Sending stop command: {stop_command.hex()}")
                    await self.client.write_gatt_char(MOUSE_WRITE_FUNC_UUID, stop_command)
                
                return True
            except Exception as e:
                debug_print(f"Error sending command: {str(e)}")
                return False
        return False

async def control_loop(controller):
    print("\nControl Loop Started")
    print("-------------------")
    print("W: Forward")
    print("S: Back")
    print("A: Left")
    print("D: Right")
    print("Q: Quit")
    print("Space: Stop")
    print("-------------------")
    
    while True:
        try:
            key = await get_key()
            
            if key.lower() == 'q':
                debug_print("Quit command received")
                await controller.set_mouse_control('stop')
                return
            elif key.lower() in ['w', 'a', 's', 'd']:
                await controller.set_mouse_control(key.lower())
            elif key == ' ':
                await controller.set_mouse_control('stop')
            
        except Exception as e:
            debug_print(f"Error in control loop: {str(e)}")

async def main():
    controller = MouseController()
    
    try:
        print("Scanning for device...")
        devices = await BleakScanner.discover()
        target_device = next((d for d in devices if d.address.upper() == DEVICE_ADDRESS.upper()), None)
        
        if not target_device:
            print(f"Could not find device with address {DEVICE_ADDRESS}")
            return

        print(f"Connecting to {target_device.address}...")
        
        async with BleakClient(target_device) as client:
            # Perform service discovery
            services = await client.get_services()
            debug_print("Services discovered:")
            for service in services:
                debug_print(f"Service: {service.uuid}")
                for char in service.characteristics:
                    debug_print(f"  Characteristic: {char.uuid}")
            
            controller.client = client
            print("\nConnection established!")
            await control_loop(controller)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if controller.client:
            await controller.set_mouse_control('stop')

if __name__ == "__main__":
    asyncio.run(main())
