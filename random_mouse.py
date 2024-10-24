import asyncio
from bleak import BleakScanner, BleakClient
import random
import time

# Device Configuration
DEVICE_ADDRESS = "B3:04:A6:20:04:34"
MOUSE_WRITE_FUNC_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"

# Command values
FORWARD = 0x01
BACK = 0x02
LEFT = 0x03
RIGHT = 0x04
STOP = 0x00

# Movement Configuration
MIN_MOVEMENT_TIME = 0.2  # Minimum time for a movement in seconds
MAX_MOVEMENT_TIME = 1.0  # Maximum time for a movement in seconds
MIN_PAUSE_TIME = 0.1    # Minimum pause between movements
MAX_PAUSE_TIME = 0.5    # Maximum pause between movements

def debug_print(message):
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")

class MouseController:
    def __init__(self):
        self.client = None
        self.is_running = True
        self.movements = [
            ('forward', FORWARD),
            ('back', BACK),
            ('left', LEFT),
            ('right', RIGHT)
        ]

    async def send_command(self, command_name, command_value):
        try:
            command = bytes([command_value, 0x00])
            debug_print(f"Sending command: {command_name} ({command.hex()})")
            await self.client.write_gatt_char(MOUSE_WRITE_FUNC_UUID, command)
            return True
        except Exception as e:
            debug_print(f"Error sending command: {str(e)}")
            return False

    async def random_movement(self):
        while self.is_running:
            try:
                # Choose random movement
                movement_name, movement_command = random.choice(self.movements)
                
                # Random movement duration
                movement_time = random.uniform(MIN_MOVEMENT_TIME, MAX_MOVEMENT_TIME)
                
                # Execute movement
                debug_print(f"Moving {movement_name} for {movement_time:.2f} seconds")
                await self.send_command(movement_name, movement_command)
                
                # Wait for movement duration
                await asyncio.sleep(movement_time)
                
                # Stop movement
                await self.send_command('stop', STOP)
                
                # Random pause
                pause_time = random.uniform(MIN_PAUSE_TIME, MAX_PAUSE_TIME)
                debug_print(f"Pausing for {pause_time:.2f} seconds")
                await asyncio.sleep(pause_time)

            except Exception as e:
                debug_print(f"Error in movement loop: {str(e)}")
                await asyncio.sleep(1)

    def stop(self):
        self.is_running = False

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
            controller.client = client
            print("\nConnection established!")
            print("Random movement pattern started!")
            print("Press Ctrl+C to stop")
            
            try:
                # Start random movement pattern
                await controller.random_movement()
            except KeyboardInterrupt:
                print("\nStopping movements...")
                controller.stop()
                await controller.send_command('stop', STOP)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if controller.client:
            await controller.send_command('stop', STOP)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
