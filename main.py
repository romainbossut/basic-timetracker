import tkinter as tk
from tkinter import ttk
import time
import datetime
import os

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
        self.current_task = tk.StringVar(value=TASKS[0])
        self.is_timing = False
        self.start_time = None
        self.elapsed_seconds = 0
        
        # --- GUI Elements ---
        
        # Task selection (Dropdown)
        self.task_label = tk.Label(root, text="Select Task:", font=("Arial", 12))
        self.task_label.pack(pady=(10, 0))
        
        self.task_dropdown = ttk.Combobox(root, 
            textvariable=self.current_task, 
            values=TASKS, 
            state="readonly",
            font=("Arial", 12),
            width=30
        )
        self.task_dropdown.pack(pady=5)

        # Start / Stop button
        self.start_stop_button = tk.Button(
            root, 
            text="Start", 
            command=self.toggle_timer,
            font=("Arial", 12),
            width=20,
            height=2
        )
        self.start_stop_button.pack(pady=10)

        # Elapsed time label
        self.time_label_text = tk.StringVar()
        self.time_label_text.set("Elapsed Time: 00:00:00")
        self.time_label = tk.Label(root, textvariable=self.time_label_text, font=("Arial", 14))
        self.time_label.pack(pady=10)

        # Update the clock every second
        self.update_clock()

    def toggle_timer(self):
        if not self.is_timing:
            # Start timing
            self.start_time = time.time()
            self.is_timing = True
            self.start_stop_button.config(text="Stop")
        else:
            # Stop timing
            end_time = time.time()
            duration = end_time - self.start_time
            self.is_timing = False
            self.start_stop_button.config(text="Start")

            # Append a record to the log file
            self.append_log(self.current_task.get(), duration)

            # Reset elapsed time display
            self.time_label_text.set("Elapsed Time: 00:00:00")

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
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
