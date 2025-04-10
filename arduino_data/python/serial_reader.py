# serial_reader.py
import serial
import time
from config import SERIAL_PORT, BAUD_RATE

# Class reads and prints data from Arduino in real-time

# Serial port and baud rate are defined in config.py
# param SERIAL_PORT: str
# param BAUD_RATE: int
# return: None

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

print("Reading from Arduino...")

try:
    while True:
        line = ser.readline().decode().strip()
        if "," in line:
            ppg, gsr = map(int, line.split(","))
            print(f"PPG: {ppg} | GSR: {gsr}")
except KeyboardInterrupt:
    print("Stopped.")
finally:
    ser.close()
