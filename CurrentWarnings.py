import requests
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime, timezone, timedelta

class TornadoWarningDisplay(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg="#2b2b2b")
        self.pack(fill=tk.BOTH, expand=True)
        self.timezone = timezone(timedelta(hours=-5))  #CHANGE THIS TO YOUR DESIRED TIMEZONE
        self.create_widgets()

    def create_widgets(self):
        self.warning_listbox = tk.Listbox(self, bg="#2b2b2b", fg="white", bd=1, relief=tk.SOLID, selectbackground="#d9d9d9", selectforeground="white")
        self.warning_listbox.pack(fill=tk.BOTH, expand=True)
        self.warning_listbox.bind("<Double-1>", self.on_warning_double_click)

    def add_warning(self, issuance_time_str, description):
        issuance_time_utc = datetime.fromisoformat(issuance_time_str)
        issuance_time = issuance_time_utc.astimezone(self.timezone)
        formatted_issuance_time = issuance_time.strftime("%Y-%m-%d %I:%M:%S %p") + " EST"  #CHANGE THIS TO YOUR DESIRED TIMEZONE ABBREVIATION
        self.warning_listbox.insert(tk.END, f"Tornado Warning For: {formatted_issuance_time}")
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
            issuance_time = selected_warning.split(": ")[1]
            details_text.insert(tk.END, f"Issuance Time: {issuance_time}\n\n")
            details_text.insert(tk.END, f"Details: {warning_details[index]}")

    def change_time_zone(self):
        self.timezone = timezone(timedelta(hours=-5))  #CHANGE THIS TO YOUR DESIRED TIMEZONE
        self.timezone_abbr = "EST" #this is a optional change but i reccomend it

        for index in range(self.warning_listbox.size()):
            warning = self.warning_listbox.get(index)
            issuance_time = warning.split(": ")[1]
            self.warning_listbox.delete(index)
            self.add_warning(issuance_time, warning.split(": ")[2])

def check_tornado_warnings(root, tornado_warning_display):
    url = "https://api.weather.gov/alerts/active"
    headers = {"User-Agent": "Python Weather Alerts"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        alerts = response.json().get("features", [])
       
        tornado_warning_display.warning_listbox.delete(0, tk.END)
        warning_details.clear()
        for alert in alerts:
            event = alert["properties"]["event"]
            if event == "Tornado Warning":
                issuance_time_str = alert["properties"]["sent"]
                description = alert["properties"]["description"]
                if description not in warning_details:
                    tornado_warning_display.add_warning(issuance_time_str, description)
                    warning_details.append(description)
    else:
        messagebox.showerror("Error", "Failed to fetch weather alerts.")

    root.after(300000, lambda: check_tornado_warnings(root, tornado_warning_display))

root = tk.Tk()
root.title("Tornado Warnings")
root.geometry("400x300")
root.config(bg="#2b2b2b")

tornado_warning_display = TornadoWarningDisplay(root)
tornado_warning_display.change_time_zone()

warning_details = []

check_tornado_warnings(root, tornado_warning_display)

menubar = tk.Menu(root)
options_menu = tk.Menu(menubar, tearoff=0)
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



