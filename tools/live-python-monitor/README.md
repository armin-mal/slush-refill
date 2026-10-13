# Live Distance Monitor Script
This script reads distance values from an STM32 serial port and plots them live in a scrolling matplotlib graph.

## Usage
Double-click `start.bat` to start the project.

On the first run, it will:
- create a virtual environment in `.venv`
- install `pyserial` and `matplotlib` if they are missing
- launch `monitor.py` using the virtual environment Python

On later runs, it will skip setup and launch the script directly.

## Notes
- Make sure your STM32 device is connected before running the script.
- If the script cannot find the port automatically, check your USB serial connection and driver.