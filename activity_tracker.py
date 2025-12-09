import tkinter as tk
from pynput.keyboard import Listener
from datetime import datetime
import os
import threading

# =====================================================
# CONFIGURATION
# =====================================================
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "activity_log.csv")

# Create required folders
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# =====================================================
# KEY LOGGER FUNCTION
# =====================================================
def log_key(key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Normalize key format
    try:
        key_val = key.char
    except:
        key_val = str(key)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{timestamp},{key_val}\n")

# Background thread function
def start_listener():
    with Listener(on_press=log_key) as listener:
        listener.join()

# =====================================================
# CONSENT WINDOW
# =====================================================
def show_consent():
    window = tk.Tk()
    window.title("Activity Tracker - Consent")
    window.geometry("450x230")
    window.resizable(False, False)

    label = tk.Label(
        window,
        text="This Activity Tracker monitors keyboard activity for productivity analysis.\n"
             "By clicking 'Accept', you confirm you are aware and agree to tracking.",
        wraplength=400,
        justify="center"
    )
    label.pack(pady=25)

    def accept():
        window.destroy()
        run_program()

    button = tk.Button(window, text="Accept and Continue", width=20, command=accept)
    button.pack(pady=10)

    disclaimer = tk.Label(window, text="Note: No data leaves this device.", fg="gray")
    disclaimer.pack(pady=5)

    window.mainloop()

# =====================================================
# MAIN PROGRAM WINDOW
# =====================================================
def run_program():
    tracker = tk.Tk()
    tracker.title("Activity Tracker - Running")
    tracker.geometry("350x150")
    tracker.resizable(False, False)

    message = tk.Label(tracker, text="The Activity Tracker is running...\nLogging keystrokes with consent.", justify="center")
    message.pack(pady=30)

    def stop_tracker():
        tracker.destroy()
        os._exit(0)

    stop_btn = tk.Button(tracker, text="Stop Tracking and Exit", command=stop_tracker)
    stop_btn.pack(pady=10)

    # Start key listener in the background
    listener_thread = threading.Thread(target=start_listener, daemon=True)
    listener_thread.start()

    tracker.mainloop()

# =====================================================
# PROGRAM START
# =====================================================
show_consent()
