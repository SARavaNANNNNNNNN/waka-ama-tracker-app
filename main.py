import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
import customtkinter as ctk

# username: admin
# password: password

# Set the initial theme to dark mode
current_mode = "light"
ctk.set_appearance_mode(current_mode)  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.withdraw()  # Hide the main window initially
        self.create_welcome_window()

    def create_welcome_window(self):
        self.welcome_window = tk.Tk()
        self.welcome_window.title("Welcome To The Waka-ama Tracker")

        # Welcome label
        welcome_label = tk.Label(self.welcome_window, text="Welcome To The Waka-ama Tracker", font=("Helvetica", 16))
        welcome_label.pack(pady=20)

        # Login button
        login_button = ctk.CTkButton(self.welcome_window, text="Login", command=self.open_login_window)
        login_button.pack(pady=10)

        self.welcome_window.mainloop()

    def open_login_window(self):
        self.welcome_window.destroy()
        self.create_login_window()

    def create_login_window(self):
        global username_var, password_var

        self.login_window = ctk.CTkToplevel(self.root)
        self.login_window.title("Login")

        username_label = ctk.CTkLabel(self.login_window, text="Username:")
        username_label.grid(row=0, column=0, padx=10, pady=10)

        username_var = StringVar()
        username_entry = ctk.CTkEntry(self.login_window, textvariable=username_var)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label = ctk.CTkLabel(self.login_window, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=10)

        password_var = StringVar()
        password_entry = ctk.CTkEntry(self.login_window, textvariable=password_var, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        login_button = ctk.CTkButton(self.login_window, text="Enter", command=self.check_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Button to toggle between dark mode and light mode (Login Window)
        toggle_mode_button_login = ctk.CTkButton(self.login_window, text="Toggle Dark/Light Mode", command=toggle_mode)
        toggle_mode_button_login.grid(row=3, column=0, columnspan=2, pady=10)

    def check_login(self):
        username = username_var.get().strip()
        password = password_var.get().strip()

        errors = []
        if len(username) > 10:
            errors.append("username exceeds the limit (maximum 10 characters)")
        if len(password) > 20:
            errors.append("password exceeds the limit (maximum 20 characters)")

        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return

        if username == "admin" and password == "password":
            self.login_window.destroy()
            self.create_main_window()  # Show the main window
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_main_window(self):
        global directory_var, name_filter_var, current_file_var, filtered_files_var

        self.root.title("Results Specifications")

        # Frame for directory selection
        directory_frame = ctk.CTkFrame(self.root)
        directory_frame.pack(pady=10)

        directory_label = ctk.CTkLabel(directory_frame, text="Select Directory:")
        directory_label.grid(row=0, column=0)

        directory_var = StringVar()
        directory_entry = ctk.CTkEntry(directory_frame, textvariable=directory_var, width=500)
        directory_entry.grid(row=0, column=1, padx=10)

        browse_button = ctk.CTkButton(directory_frame, text="Select", command=self.browse_directory)
        browse_button.grid(row=0, column=2)

        # Frame for name filter
        filter_frame = ctk.CTkFrame(self.root)
        filter_frame.pack(pady=10)

        name_filter_label = ctk.CTkLabel(filter_frame, text="File Name:")
        name_filter_label.grid(row=0, column=0)

        name_filter_var = StringVar(value="")
        name_filter_entry = ctk.CTkEntry(filter_frame, textvariable=name_filter_var, width=500)
        name_filter_entry.grid(row=0, column=1, padx=10)

        apply_filter_button = ctk.CTkButton(filter_frame, text="Apply", command=self.apply_name_filter)
        apply_filter_button.grid(row=0, column=2)

        # Frame for buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        # Button to check files and assign points
        check_files_button = ctk.CTkButton(button_frame, text="Results", command=self.process_and_save_results)
        check_files_button.grid(row=0, column=0, padx=5)

        # Button to toggle between dark mode and light mode (Main Window)
        toggle_mode_button_main = ctk.CTkButton(button_frame, text="Toggle Dark/Light Mode", command=toggle_mode)
        toggle_mode_button_main.grid(row=0, column=1, padx=5)

        # Frame for current file being processed
        current_file_frame = ctk.CTkFrame(self.root)
        current_file_frame.pack(pady=10)

        current_file_var = StringVar(value="Files processed: None")
        current_file_label = ctk.CTkLabel(current_file_frame, textvariable=current_file_var)
        current_file_label.pack()

        # Variable to store filtered files
        filtered_files_var = tk.Variable(value=[])

        self.root.deiconify()  # Show the main window

    # Function to browse directory
    def browse_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            directory_var.set(directory_path)

    # Function to apply name filter and display files
    def apply_name_filter(self):
        directory_path = directory_var.get()
        if not directory_path:
            messagebox.showerror("Error", "Directory not selected")
            return

        filter_text = name_filter_var.get().lower()
        filtered_files = []

        for filename in os.listdir(directory_path):
            if filter_text in filename.lower():
                filtered_files.append(filename)

        if filtered_files:
            messagebox.showinfo("Filtered Files", "\n".join(filtered_files))
        else:
            messagebox.showinfo("Filtered Files", "No files matched the filter")

        filtered_files_var.set(filtered_files)

    # Function to process filtered files and assign points
    def process_and_save_results(self):
        directory_path = directory_var.get()
        if not directory_path:
            messagebox.showerror("Error", "Directory not selected")
            return

        filtered_files = filtered_files_var.get()
        if not filtered_files:
            messagebox.showerror("Error", "No files to process")
            return

        club_points = {}

        for filename in filtered_files:
            current_file_var.set(f"Processing: {filename}")
            self.root.update_idletasks()  # Force update the GUI

            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        lines = file.readlines()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read file {filename}: {e}")
                    return

            try:
                for i, line in enumerate(lines[1:]):
                    columns = line.split(',')
                    if len(columns) > 5:
                        club_name = columns[5].strip()
                        if club_name.upper() in ["DQ", "DNS"]:
                            continue  # Skip DQ or DNS entries
                        points = self.assign_points(i + 1)
                        if club_name in club_points:
                            club_points[club_name] += points
                        else:
                            club_points[club_name] = points
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file {filename}: {e}")
                return

        current_file_var.set("Results Processed.")
        self.root.update_idletasks()  # Ensure the final update to the GUI
        self.save_results_to_txt(club_points)

    # Function to assign points based on placement
    def assign_points(self, placement):
        if placement <= 0:  # No points for DQ or DNS (placement <= 0)
            return 0
        points = 9 - placement
        return max(points, 1)  # Ensure minimum points is 1

    def save_results_to_txt(self, club_points):
        results_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not results_file_path:
            return

        try:
            with open(results_file_path, 'w', newline='', encoding='utf-8') as txtfile:
                sorted_clubs = sorted(club_points.items(), key=lambda item: item[1], reverse=True)
                for club, points in sorted_clubs:
                    txtfile.write(f'{club},{points}\n')

            messagebox.showinfo("Success", f"Results saved to {results_file_path}")

            # Automatically open the file in Notepad
            if platform.system() == 'Windows':
                os.startfile(results_file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', results_file_path))
            else:  # linux variants
                subprocess.call(('xdg-open', results_file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Results did not save: {e}")

# Function to toggle between dark mode and light mode
def toggle_mode():
    global current_mode
    if current_mode == "dark":
        ctk.set_appearance_mode("light")
        current_mode = "light"
    else:
        ctk.set_appearance_mode("dark")
        current_mode = "dark"

# Run the application
app = App()
