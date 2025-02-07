import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import subprocess
import os

COMMANDS_FILE = "commands.json"

class CommandRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Command Runner")
        self.root.geometry("600x500")
        
        # Load commands from JSON
        self.commands = self.load_commands()
        
        # UI Elements
        self.create_widgets()

    def load_commands(self):
        """Load commands from JSON file"""
        if os.path.exists(COMMANDS_FILE):
            with open(COMMANDS_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_commands(self):
        """Save commands to JSON file"""
        with open(COMMANDS_FILE, "w") as file:
            json.dump(self.commands, file, indent=4)

    def create_widgets(self):
        """Create UI Components"""
        # Action Selection
        self.action_label = tk.Label(self.root, text="Select Action:")
        self.action_label.pack(pady=5)

        self.action_var = tk.StringVar()
        self.action_menu = ttk.Combobox(self.root, textvariable=self.action_var, state="readonly")
        self.action_menu.pack(pady=5)
        self.update_action_menu()

        # Run Button
        self.run_button = tk.Button(self.root, text="Run Command", command=self.run_command)
        self.run_button.pack(pady=5)

        # Command Output
        self.output_label = tk.Label(self.root, text="Output:")
        self.output_label.pack(pady=5)

        self.output_text = tk.Text(self.root, height=10, width=70)
        self.output_text.pack(pady=5)

        # Action Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.add_button = tk.Button(self.button_frame, text="Add/Edit Command", command=self.add_edit_command)
        self.add_button.grid(row=0, column=0, padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove Command", command=self.remove_command)
        self.remove_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.export_button = tk.Button(self.button_frame, text="Export Output", command=self.export_output)
        self.export_button.grid(row=0, column=3, padx=5)

    def update_action_menu(self):
        """Update dropdown with saved commands"""
        self.action_menu["values"] = list(self.commands.keys())

    def run_command(self):
        """Execute the selected command and display output"""
        action = self.action_var.get()
        if not action:
            messagebox.showwarning("Warning", "Please select an action!")
            return

        command = self.commands.get(action)
        if not command:
            messagebox.showerror("Error", "Command not found!")
            return

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
        except Exception as e:
            output = str(e)

        self.output_text.insert(tk.END, f"Running: {command}\n{output}\n{'-'*50}\n")

    def add_edit_command(self):
        """Add or edit a command"""
        self.add_edit_window = tk.Toplevel(self.root)
        self.add_edit_window.title("Add/Edit Command")
        self.add_edit_window.geometry("400x200")

        tk.Label(self.add_edit_window, text="Action Name:").pack(pady=5)
        self.action_entry = tk.Entry(self.add_edit_window)
        self.action_entry.pack(pady=5)

        tk.Label(self.add_edit_window, text="Command:").pack(pady=5)
        self.command_entry = tk.Entry(self.add_edit_window)
        self.command_entry.pack(pady=5)

        tk.Button(self.add_edit_window, text="Save", command=self.save_new_command).pack(pady=10)

    def save_new_command(self):
        """Save new or edited command"""
        action = self.action_entry.get().strip()
        command = self.command_entry.get().strip()

        if not action or not command:
            messagebox.showerror("Error", "Both fields are required!")
            return

        self.commands[action] = command
        self.save_commands()
        self.update_action_menu()
        self.add_edit_window.destroy()
        messagebox.showinfo("Success", "Command saved successfully!")

    def remove_command(self):
        """Remove selected command"""
        action = self.action_var.get()
        if not action:
            messagebox.showwarning("Warning", "Please select an action to remove!")
            return

        if messagebox.askyesno("Confirm", f"Are you sure you want to remove '{action}'?"):
            del self.commands[action]
            self.save_commands()
            self.update_action_menu()
            self.action_var.set("")
            messagebox.showinfo("Success", "Command removed successfully!")

    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete("1.0", tk.END)

    def export_output(self):
        """Export output to a text file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        
        with open(file_path, "w") as file:
            file.write(self.output_text.get("1.0", tk.END))
        
        messagebox.showinfo("Success", "Output exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CommandRunnerApp(root)
    root.mainloop()
