import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Config file containing commands
CONFIG_FILE = "commands.txt"

def load_commands():
    """Load commands from config file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            commands = file.readlines()
        return [cmd.strip() for cmd in commands if cmd.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", f"Config file '{CONFIG_FILE}' not found!")
        return []

def run_command():
    """Run selected command and display output."""
    selected_index = command_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select a command to run.")
        return

    selected_command = command_listbox.get(selected_index)

    try:
        result = subprocess.run(selected_command, shell=True, capture_output=True, text=True)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.stdout + result.stderr)
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute command: {e}")

# UI Setup
root = tk.Tk()
root.title("Command Runner")

# Command Listbox
tk.Label(root, text="Available Commands:").pack()
command_listbox = tk.Listbox(root, height=10, width=50)
command_listbox.pack()

# Load commands into listbox
commands = load_commands()
for cmd in commands:
    command_listbox.insert(tk.END, cmd)

# Run Button
run_button = tk.Button(root, text="Run Command", command=run_command)
run_button.pack()

# Output Display
tk.Label(root, text="Command Output:").pack()
output_text = scrolledtext.ScrolledText(root, height=10, width=60, state=tk.DISABLED)
output_text.pack()

# Run UI Loop
root.mainloop()
