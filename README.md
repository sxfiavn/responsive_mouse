# responsive_mouse

## TODO:

- Edit name and description
- Check contributors
- Edit Attributions
- add machine learning code?

# Responsive Mouse - Biosensing Based Stress Mitigation System

A biofeedback-based stress detection system using Arduino sensors (PPG and GSR). This system monitors physiological signals to detect stress levels in real time. The project collects sensor data, processes it, and logs it for machine learning model training.

This repository contains code for calibrating the sensors, logging sensor data, and processing the data for further analysis.

## Table of Contents

1. [License](#license)
2. [Description](#description)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Files and Scripts](#files-and-scripts)
6. [Contributors](#contributors)

## License

This project is licensed under the **Apache 2.0 License** - see the [LICENSE](LICENSE) file for details.

## Description

This project utilizes Arduino sensors to measure heart rate (PPG) and skin conductance (GSR) as a way to detect stress levels in users. The data collected from these sensors are processed and saved in CSV files for analysis. In the long term, this data will be used to train a machine learning model to predict whether a user is stressed based on these physiological signals.

The system also includes a feature that can stop notifications on a user's iMac when stress is detected in real-time.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/responsive_mouse_project.git
   cd responsive_mouse_project
   ```


2. Create a **Conda** environment and install the dependencies:

   ```bash
   conda create --name responsive_mouse_env python=3.8
   conda activate responsive_mouse_env
   pip install -r requirements.txt
   ```

3. **Dependencies**:
   - `pyserial`: For serial communication with the Arduino.
   - `numpy`: For data processing.
   - `matplotlib`: (optional) For visualization.
   - `scikit-learn`: For machine learning models (if applicable).

## Usage

### Calibrating the Sensors

To calibrate the PPG and GSR sensors before starting data collection, run the following script:

```bash
python calibrate.py
```

You will be prompted to press a key when ready for calibration. The script will perform averaging to stabilize sensor readings and then log the calibration data to a CSV file.

### Logging Data

To start logging data, use the `log_data.py` script. It will collect real-time sensor data and store it in a CSV file. You will be prompted for the participant ID, trial label, and trial number.

```bash
python log_data.py
```

Follow the prompts to enter participant info. The script will then start logging PPG and GSR data along with the provided labels, storing it in a timestamped CSV file.

### Viewing Real-time Data (Optional)

If you want to visualize the data in real-time while it is being logged, you can use the **Serial Plotter** in the Arduino IDE or run a Python script to plot the data.

```bash
python plot_data.py
```

## Files and Scripts

- **calibrate.py**: Calibrates the sensors and logs the calibration data.
- **log_data.py**: Collects real-time sensor data and logs it into a CSV file with a timestamp.
- **plot_data.py**: (Optional) Visualizes the sensor data in real-time.
- **.gitignore**: Contains files and folders (e.g., `data/`) that should not be tracked by Git.

## Contributors

- **[Sofia Vaca Narvaja]** - Arduino, Developer
- **[Evani Dalal]** - Machine Learning Model
- **[Ming Dong]** - Design
- **[Yuxin Ni]** -

## Acknowledgements 

- The sensors used in this project (PPG and GSR) are available through various suppliers and were chosen based on their accessibility and ease of use with Arduino.
- This project was submitted as part of the [2025 IHIET - Human Interaction & Emerging Technologies conference] (https://www.ihiet.org/index-ihiet.html) as a proof of concept of a biofeedback based stress mitigation system.
