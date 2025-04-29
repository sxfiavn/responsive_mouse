# config.py
SERIAL_PORT = '/dev/cu.usbmodem744DBD9FD0942'  # ← change to your port (check Arduino IDE)
BAUD_RATE = 115200 # don't touch
SAMPLING_RATE = 50  # Hz

# change per trial
LABEL = 'not_stressed' 
DURATION = 10 # trial length in seconds, set to None for continuous logging

#TODO: add script to run log data and prompt label and duration
#TODO: add requirements.txt for conda environment