import tkinter as tk
from tkinter import ttk
import time
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd

# Replace the TASKS list with a function to read from file
TASKS_FILENAME = "tasks.txt"

def load_tasks():
    """Load tasks from the tasks file, or return default tasks if file doesn't exist."""
    default_tasks = ["Check Email", "Work on Project", "Read Documentation", "Break", "Meeting"]
    
    try:
        with open(TASKS_FILENAME, "r", encoding="utf-8") as f:
            tasks = [line.strip() for line in f if line.strip()]
        return tasks if tasks else default_tasks
    except FileNotFoundError:
        # Create the file with default tasks
        with open(TASKS_FILENAME, "w", encoding="utf-8") as f:
            f.write("\n".join(default_tasks))
        return default_tasks

# Replace the TASKS constant with the function call
TASKS = load_tasks()

LOG_FILENAME = "time_log.txt"

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")

        # Variables
        self.current_task = None
        self.is_timing = False
        self.start_time = None
        self.elapsed_seconds = 0
        
        # Create main container
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for buttons
        self.left_frame = tk.Frame(self.main_container)
        self.left_frame.pack(side=tk.LEFT, pady=10, padx=10)
        
        # Right frame for charts
        self.right_frame = tk.Frame(self.main_container)
        self.right_frame.pack(side=tk.RIGHT, pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Task buttons frame (now in left frame)
        self.buttons_frame = tk.Frame(self.left_frame)
        self.buttons_frame.pack(pady=10, padx=10)
        
        # Create a button for each task
        self.task_buttons = {}
        for task in TASKS:
            btn = tk.Button(
                self.buttons_frame,
                text=task,
                font=("Arial", 12),
                width=20,
                height=2,
                command=lambda t=task: self.switch_task(t)
            )
            btn.pack(pady=5)
            self.task_buttons[task] = btn

        # Elapsed time label
        self.time_label_text = tk.StringVar()
        self.time_label_text.set("Elapsed Time: 00:00:00")
        self.time_label = tk.Label(self.left_frame, textvariable=self.time_label_text, font=("Arial", 14))
        self.time_label.pack(pady=10)

        # Create charts
        self.setup_charts()
        
        # Update the clock and charts every second
        self.update_clock()
        self.update_charts()

    def setup_charts(self):
        """Setup the donut charts for today and last 7 days"""
        # Create figures and subplots
        self.fig = Figure(figsize=(10, 5))
        self.today_ax = self.fig.add_subplot(121)
        self.week_ax = self.fig.add_subplot(122)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_time_data(self, days_ago=0):
        """Get time data for a specific day"""
        try:
            df = pd.read_csv(LOG_FILENAME, header=None, names=['timestamp', 'task', 'duration'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['duration'] = df['duration'].apply(lambda x: sum(int(i) * j for i, j in zip(x.split(':'), [3600, 60, 1])))
            
            target_date = datetime.now().date() - timedelta(days=days_ago)
            mask = df['timestamp'].dt.date == target_date
            daily_data = df[mask].groupby('task')['duration'].sum()
            
            # Add current session time if we're timing and it's today's chart
            if days_ago == 0 and self.is_timing and self.current_task and self.start_time:
                current_duration = time.time() - self.start_time
                if self.current_task in daily_data:
                    daily_data[self.current_task] += current_duration
                else:
                    daily_data[self.current_task] = current_duration
            
            return daily_data
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If no data file exists but we're currently timing, create data for current task
            if days_ago == 0 and self.is_timing and self.current_task and self.start_time:
                current_duration = time.time() - self.start_time
                return pd.Series({self.current_task: current_duration})
            return pd.Series()

    def update_charts(self):
        """Update both donut charts"""
        # Clear previous plots
        self.today_ax.clear()
        self.week_ax.clear()
        
        # Today's data
        today_data = self.get_time_data()
        if not today_data.empty:
            self.today_ax.pie(today_data.values, labels=today_data.index, autopct='%1.1f%%', pctdistance=0.85)
            self.today_ax.add_artist(plt.Circle((0,0), 0.70, fc='white'))
        self.today_ax.set_title("Today's Tasks")
        
        # Last 7 days data
        week_data = pd.Series()
        for i in range(7):
            daily_data = self.get_time_data(days_ago=i)
            week_data = week_data.add(daily_data, fill_value=0)
        
        if not week_data.empty:
            self.week_ax.pie(week_data.values, labels=week_data.index, autopct='%1.1f%%', pctdistance=0.85)
            self.week_ax.add_artist(plt.Circle((0,0), 0.70, fc='white'))
        self.week_ax.set_title("Last 7 Days")
        
        # Adjust layout and draw
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Schedule next update after 10 seconds instead of 1
        self.root.after(10000, self.update_charts)

    def switch_task(self, new_task):
        """Handle switching between tasks"""
        # If we're currently timing, log the previous task
        if self.is_timing and self.current_task:
            end_time = time.time()
            duration = end_time - self.start_time
            self.append_log(self.current_task, duration)

        # Reset button colors
        for btn in self.task_buttons.values():
            btn.configure(bg='SystemButtonFace', fg='black')  # Default colors

        # If switching to the same task, stop timing
        if new_task == self.current_task:
            self.is_timing = False
            self.current_task = None
            self.time_label_text.set("Elapsed Time: 00:00:00")
        else:
            # Start timing the new task
            self.current_task = new_task
            self.start_time = time.time()
            self.is_timing = True
            # Highlight the selected button
            self.task_buttons[new_task].configure(bg='red', fg='white')

    def update_clock(self):
        """
        Updates the elapsed time display if timing is active.
        Schedules itself to run again after 1 second.
        """
        if self.is_timing and self.start_time:
            elapsed = int(time.time() - self.start_time)
            formatted = self.format_time(elapsed)
            self.time_label_text.set(f"Elapsed Time: {formatted}")
        # Schedule the next update after 1 second
        self.root.after(1000, self.update_clock)

    def append_log(self, task_name, duration_seconds):
        """
        Append a line to the log file with the current date/time,
        the task name, and the duration in HH:MM:SS format.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration_str = self.format_time(int(duration_seconds))
        log_line = f"{now_str}, {task_name}, {duration_str}\n"
        with open(LOG_FILENAME, "a", encoding="utf-8") as f:
            f.write(log_line)

    @staticmethod
    def format_time(seconds):
        """ Format seconds into HH:MM:SS. """
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"


def run_gui():
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()


def interactive_cli():
    """
    A minimal CLI (command-line interface).
    You can expand this as needed.
    """
    while True:
        print("\n--- Interactive CLI ---")
        print("1) List tasks")
        print("2) Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Available tasks:")
            for idx, task in enumerate(TASKS, start=1):
                print(f"{idx}. {task}")
        elif choice == "2":
            print("Exiting CLI...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    print("Starting Time Tracker...")
    # Launch the GUI
    run_gui()
    
    print("Time Tracker has exited.")
