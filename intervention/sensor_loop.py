
# Description:
# Role: Sensor data handler 
# Responsibility:
# Continuously reads sensor data from the serial port
# Maintains a rolling buffer of last 10s


import random
import time
from config import USE_MOCK_SENSOR


if not USE_MOCK_SENSOR:
    import serial

def start_sensor_loop(buffer, port="/dev/tty.usbmodem744DBD9FD0942", baudrate=115200):
    """
    Reads data from sensor or mocks it, and fills the buffer with (ppg, gsr, timestamp).
    Called by main_window.py.
    """
    if USE_MOCK_SENSOR:
        print("Sensor loop started in MOCK mode")
    else:
        print("Sensor loop started with serial input")
        ser = serial.Serial(port, baudrate)

    while True:
        try:
            if USE_MOCK_SENSOR:
                # Simulate readings every 25 ms (40 Hz)
                ppg = random.randint(500, 600)
                gsr = random.randint(200, 400)
                buffer.append((ppg, gsr, time.time()))
                time.sleep(0.025)
            else:
                line = ser.readline().decode().strip()
                ppg, gsr = map(int, line.split(","))
                buffer.append((ppg, gsr, time.time()))

        except Exception as e:
            print(f"[Sensor Error] {e}")
            continue