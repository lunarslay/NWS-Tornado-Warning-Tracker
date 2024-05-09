import requests
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime, timezone

class TornadoWarningDisplay(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg="#2b2b2b")
        self.pack(fill=tk.BOTH, expand=True)
        self.theme_mode = tk.StringVar(value="System")  
        self.set_theme_mode(self.theme_mode.get()) 
        self.timezone = self.get_system_timezone()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        
        self.warnings_tab = tk.Frame(self.notebook, bg="#2b2b2b")
        self.notebook.add(self.warnings_tab, text="Warnings")

        self.warning_listbox = tk.Listbox(self.warnings_tab, bg="#2b2b2b", fg="white", bd=1, relief=tk.SOLID, selectbackground="#d9d9d9", selectforeground="white")
        self.warning_listbox.pack(fill=tk.BOTH, expand=True)
        self.warning_listbox.bind("<Double-1>", self.on_warning_double_click)

       
        self.options_tab = tk.Frame(self.notebook, bg="#2b2b2b")
        self.notebook.add(self.options_tab, text="Options")

       
        self.show_severe_thunderstorm = tk.BooleanVar()
        self.show_tornado_warning = tk.BooleanVar()
        self.show_tornado_watch = tk.BooleanVar()
        self.show_flash_flood = tk.BooleanVar()
        self.show_weather_statement = tk.BooleanVar()

        self.severe_thunderstorm_check = tk.Checkbutton(self.options_tab, text="Severe Thunderstorm", variable=self.show_severe_thunderstorm, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b", command=self.update_warnings)
        self.severe_thunderstorm_check.pack(anchor=tk.W)

        self.tornado_warning_check = tk.Checkbutton(self.options_tab, text="Tornado Warning", variable=self.show_tornado_warning, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b", command=self.update_warnings)
        self.tornado_warning_check.pack(anchor=tk.W)

        self.tornado_watch_check = tk.Checkbutton(self.options_tab, text="Tornado Watch", variable=self.show_tornado_watch, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b", command=self.update_warnings)
        self.tornado_watch_check.pack(anchor=tk.W)

        self.flash_flood_check = tk.Checkbutton(self.options_tab, text="Flash Flood", variable=self.show_flash_flood, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b", command=self.update_warnings)
        self.flash_flood_check.pack(anchor=tk.W)

        self.weather_statement_check = tk.Checkbutton(self.options_tab, text="Weather Statement", variable=self.show_weather_statement, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b", command=self.update_warnings)
        self.weather_statement_check.pack(anchor=tk.W)

    def add_warning(self, issuance_time_str, event):
        issuance_time_utc = datetime.fromisoformat(issuance_time_str)
        issuance_time = issuance_time_utc.astimezone(self.timezone)
        formatted_issuance_time = issuance_time.strftime("%Y-%m-%d %I:%M %p")  
        self.warning_listbox.insert(tk.END, f"{event}: {formatted_issuance_time}")
        self.warning_listbox.itemconfig(tk.END, fg="white")
        self.warning_listbox.update()

    def on_warning_double_click(self, event):
        selection = self.warning_listbox.curselection()
        if selection:
            index = int(selection[0])
            details_window = tk.Toplevel(self)
            details_window.title("Warning Details")
            details_window.geometry("400x200")
            details_frame = tk.Frame(details_window, bg="#2b2b2b")
            details_frame.pack(fill=tk.BOTH, expand=True)
            details_text = ScrolledText(details_frame, wrap=tk.WORD, bg="#2b2b2b", fg="white", padx=10, pady=10, bd=1, relief=tk.SOLID)
            details_text.pack(fill=tk.BOTH, expand=True)
            selected_warning = self.warning_listbox.get(index)
            event, issuance_time = selected_warning.split(": ")
            details_text.insert(tk.END, f"Event: {event}\n")
            details_text.insert(tk.END, f"Issuance Time: {issuance_time}\n\n")
            details_text.insert(tk.END, f"Details: {warning_details[index]}")

    def get_system_timezone(self):
        return datetime.now().astimezone().tzinfo

    def set_theme_mode(self, mode):
        if mode == "Light":
            self.master.config(bg="white")
            self.warning_listbox.config(bg="white", fg="black")
        elif mode == "Dark":
            self.master.config(bg="#2b2b2b")
            self.warning_listbox.config(bg="#2b2b2b", fg="white")
        elif mode == "System":
            pass  

    def change_time_zone(self):
        self.timezone = self.get_system_timezone()

    def change_theme_mode(self):
        selected_mode = self.theme_mode.get()
        self.set_theme_mode(selected_mode)

    def update_warnings(self):
        print("Updating warnings...")
       
        self.warning_listbox.delete(0, tk.END)
        warning_details.clear()

       
        url = "https://api.weather.gov/alerts/active"
        headers = {"User-Agent": "Python Weather Alerts"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            alerts = response.json().get("features", [])
            print(f"Received {len(alerts)} alerts.")
            for alert in alerts:
                event = alert["properties"]["event"]
                print(f"Event: {event}")
                issuance_time_str = alert["properties"]["sent"]
                description = alert["properties"]["description"]
                if (event == "Severe Thunderstorm Warning" and self.show_severe_thunderstorm.get()) or \
                   (event == "Tornado Warning" and self.show_tornado_warning.get()) or \
                   (event == "Tornado Watch" and self.show_tornado_watch.get()) or \
                   (event == "Flash Flood Warning" and self.show_flash_flood.get()) or \
                   (event == "Special Weather Statement" and self.show_weather_statement.get()):
                    self.add_warning(issuance_time_str, event)
                    warning_details.append(description)
        else:
            messagebox.showerror("Error", "Failed to fetch weather alerts.")

root = tk.Tk()
root.title("Tornado Warnings")
root.geometry("400x300")
root.config(bg="#2b2b2b")

tornado_warning_display = TornadoWarningDisplay(root)
tornado_warning_display.change_time_zone()

warning_details = []

menubar = tk.Menu(root)
options_menu = tk.Menu(menubar, tearoff=0)

theme_menu = tk.Menu(options_menu, tearoff=0)
theme_menu.add_radiobutton(label="Light", variable=tornado_warning_display.theme_mode, value="Light", command=tornado_warning_display.change_theme_mode)
theme_menu.add_radiobutton(label="Dark", variable=tornado_warning_display.theme_mode, value="Dark", command=tornado_warning_display.change_theme_mode)
theme_menu.add_radiobutton(label="System", variable=tornado_warning_display.theme_mode, value="System", command=tornado_warning_display.change_theme_mode)

options_menu.add_cascade(label="Theme", menu=theme_menu)
options_menu.add_command(label="Change Time Zone", command=tornado_warning_display.change_time_zone)

menubar.add_cascade(label="Options", menu=options_menu)
root.config(menu=menubar)

root.mainloop()

#Hey! I see you snooping around. i bet your wondering why my codes so junk? well let me explain. the time zone change is broken, this is INTENTIONAL, this will be fixed next update
#I plan to add a way to select dif warnings you want to recieve and show
#i know tornado emergencies dont show, this will be fixed next update
#i also plan to add a option to switch between light dark and match system theme modes
#i will prob make the timezone match the system one next update
#overall code improvements will be made next update
#Thats it, CYA!!!!



