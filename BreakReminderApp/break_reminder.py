import tkinter as tk
from tkinter import messagebox
import time
import threading

class BreakReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Break Reminder")
        self.root.geometry("400x350")
        
        # Default interval settings (in seconds)
        self.short_break_duration = 600   # 10 minutes for short break
        self.long_break_duration = 1800   # 30 minutes for long break
        
        # Initialize last break times
        self.last_short_break = time.time()
        self.last_long_break = time.time()
        
        # Default break intervals in seconds (1 hour and 4 hours)
        self.short_break_interval = 3600   # 1 hour default
        self.long_break_interval = 14400   # 4 hours default
        
        # Flag to track if break is active
        self.break_active = False
        
        # UI Elements
        self.timer_label = tk.Label(root, text="Break Reminder Timer", font=("Helvetica", 14))
        self.timer_label.pack(pady=10)
        
        self.short_break_label = tk.Label(root, text="Set short break interval (hours):", font=("Helvetica", 12))
        self.short_break_label.pack()
        
        self.short_break_entry = tk.Entry(root, width=10)
        self.short_break_entry.pack()
        self.short_break_entry.insert(0, "1")  # Default 1 hour
        
        self.long_break_label = tk.Label(root, text="Set long break interval (hours):", font=("Helvetica", 12))
        self.long_break_label.pack()
        
        self.long_break_entry = tk.Entry(root, width=10)
        self.long_break_entry.pack()
        self.long_break_entry.insert(0, "4")  # Default 4 hours
        
        self.set_button = tk.Button(root, text="Set Timers", command=self.set_timers)
        self.set_button.pack(pady=5)
        
        # Countdown labels for short and long breaks
        self.short_break_countdown_label = tk.Label(root, text="Time until next short break: --:--:--", font=("Helvetica", 10))
        self.short_break_countdown_label.pack(pady=5)
        
        self.long_break_countdown_label = tk.Label(root, text="Time until next long break: --:--:--", font=("Helvetica", 10))
        self.long_break_countdown_label.pack(pady=5)
        
        self.status_label = tk.Label(root, text="Status: Working", font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
        self.reset_button = tk.Button(root, text="Reset Timers", command=self.reset_timers)
        self.reset_button.pack(pady=5)
        
        # Start the break reminder thread
        self.running = True
        self.thread = threading.Thread(target=self.check_timers)
        self.thread.start()
        
        # Start the countdown updater
        self.update_countdown()

    def set_timers(self):
        """Set timers based on user input."""
        try:
            # Convert hours to seconds
            self.short_break_interval = int(float(self.short_break_entry.get()) * 3600)
            self.long_break_interval = int(float(self.long_break_entry.get()) * 3600)
            
            # Reset timers to start countdown with new intervals
            self.last_short_break = time.time()
            self.last_long_break = time.time()
            
            self.status_label.config(text="Timers set. Status: Working")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for hours.")
    
    def reset_timers(self):
        """Reset timers after a break."""
        self.last_short_break = time.time()
        self.last_long_break = time.time()
        self.break_active = False
        self.status_label.config(text="Status: Working")

    def check_timers(self):
        """Check timers and show alerts at the right times."""
        while self.running:
            current_time = time.time()
            
            # Check for short break
            if current_time - self.last_short_break >= self.short_break_interval:
                self.show_break_alert("Take a 10-minute break!", self.short_break_duration)
                self.last_short_break = time.time()
            
            # Check for long break
            if current_time - self.last_long_break >= self.long_break_interval:
                self.show_break_alert("Take a 30-minute walk or lunch break!", self.long_break_duration)
                self.last_long_break = time.time()
            
            time.sleep(10)  # Check every 10 seconds

    def show_break_alert(self, message, duration):
        """Display a break alert and keep track of break duration."""
        self.break_active = True
        start_break = time.time()
        
        # Show popup alert
        messagebox.showinfo("Break Reminder", message)
        self.status_label.config(text=f"Status: On break - {duration // 60} minutes")
        
        # Wait for break duration
        time.sleep(duration)
        
        # Return from break
        end_break = time.time()
        break_time = end_break - start_break
        self.status_label.config(text=f"Break ended. Duration: {int(break_time // 60)} mins")
        self.break_active = False

    def update_countdown(self):
        """Update countdown timers on the UI every second."""
        if self.running:
            # Calculate time remaining for next short and long breaks
            time_to_short_break = max(0, self.short_break_interval - (time.time() - self.last_short_break))
            time_to_long_break = max(0, self.long_break_interval - (time.time() - self.last_long_break))
            
            # Convert seconds to hours, minutes, and seconds
            short_hours, short_remainder = divmod(time_to_short_break, 3600)
            short_minutes, short_seconds = divmod(short_remainder, 60)
            self.short_break_countdown_label.config(
                text=f"Time until next short break: {int(short_hours):02}:{int(short_minutes):02}:{int(short_seconds):02}"
            )
            
            long_hours, long_remainder = divmod(time_to_long_break, 3600)
            long_minutes, long_seconds = divmod(long_remainder, 60)
            self.long_break_countdown_label.config(
                text=f"Time until next long break: {int(long_hours):02}:{int(long_minutes):02}:{int(long_seconds):02}"
            )
            
            # Schedule the next update in 1 second
            self.root.after(1000, self.update_countdown)

    def on_closing(self):
        """Handle app closing."""
        self.running = False
        self.root.destroy()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BreakReminderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

