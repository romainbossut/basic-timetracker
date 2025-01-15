# Time Tracker

A simple yet powerful desktop application for tracking time spent on different tasks throughout your day. Built with Python and Tkinter, featuring real-time visualization of your time distribution.

## Features

- **Task Tracking**
  - One-click task switching
  - Real-time elapsed time display
  - Automatic task logging
  - Visual indication of active task

- **Data Visualization**
  - Real-time donut charts updating every 10 seconds
  - Today's task distribution
  - Last 7 days task distribution
  - Percentage breakdown of time spent

- **Data Persistence**
  - Automatic logging of all task sessions
  - Historical data tracking
  - Custom task list support

## Requirements

- Python 3.x
- Required packages:
  - tkinter
  - matplotlib
  - pandas

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
```bash
pip install matplotlib pandas
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Click on a task button to start tracking time for that task
3. Click the same task button again to stop tracking
4. Click a different task button to switch tasks

The application will automatically:
- Track your time
- Save your task history
- Display real-time visualizations
- Maintain historical data

## File Structure

- `main.py` - Main application code
- `tasks.txt` - List of trackable tasks (customizable)
- `time_log.txt` - Historical time tracking data
- `README.md` - This documentation

## Customizing Tasks

Edit `tasks.txt` to customize your task list. Each task should be on a new line. Default tasks include:
- Check Email
- Work on Project
- Read Documentation
- Break
- Meeting

## Data Storage

Time tracking data is stored in `time_log.txt` in the format:
```
YYYY-MM-DD HH:MM:SS, Task Name, HH:MM:SS
```

## Contributing

Feel free to fork this repository and submit pull requests for any improvements you'd like to add. 