import tkinter as tk
from tkinter import messagebox, filedialog, Menu
from main import update_time, toggle_pause, is_pause, reset
import main
import os

APP_VERSION = "1.0.0"
DEVELOPER_NAME = "Amaan Raza"

# ---------------- Colors / Theme ----------------
BG_COLOR = "#1E1E2E"
CARD_COLOR = "#2A2A3C"
TEXT_COLOR = "#F5F5F5"
ACCENT_GREEN = "#2ECC71"
ACCENT_ORANGE = "#F39C12"
ACCENT_RED = "#E74C3C"
ACCENT_BLUE = "#3498DB"
ACCENT_GRAY = "#7F8C8D"

lap_count = 1

root = tk.Tk()
root.title("Professional Stopwatch")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# ---------------- Window Icon ----------------
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stopwatch_icon.ico")
if os.path.exists(icon_path):
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass

# ---------------- Center Window on Screen ----------------
WIN_WIDTH, WIN_HEIGHT = 420, 560


def center_window(window, width, height):
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = int((screen_w / 2) - (width / 2))
    y = int((screen_h / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")


center_window(root, WIN_WIDTH, WIN_HEIGHT)

# ---------------- Menu Bar (Help -> About) ----------------
def show_about():
    messagebox.showinfo(
        "About Professional Stopwatch",
        f"Professional Stopwatch\nVersion: {APP_VERSION}\nDeveloped by: {DEVELOPER_NAME}"
    )


menu_bar = Menu(root)
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

# ---------------- Title ----------------
title_label = tk.Label(
    root,
    text="⏱ Professional Stopwatch",
    font=("Arial", 16, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack(pady=(15, 0))

# ---------------- Time Display ----------------
time_frame = tk.Frame(root, bg=BG_COLOR)
time_frame.pack(pady=(20, 10))

time_label = tk.Label(
    time_frame,
    text="00:00:00",
    font=("Consolas", 44, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
time_label.pack()

# ---------------- Main Controls (Start / Pause / Reset) ----------------
controls_frame = tk.Frame(root, bg=BG_COLOR)
controls_frame.pack(pady=15)

BTN_COMMON = dict(
    font=("Arial", 11, "bold"),
    fg="white",
    width=8,
    relief="flat",
    bd=0,
    padx=5,
    pady=8,
    cursor="hand2"
)


def start_stopwatch():
    if main.is_pause:
        toggle_pause()
    start_btn.config(state=tk.DISABLED)
    pause_btn.config(state=tk.NORMAL)


def pause_stopwatch():
    currently_pause = toggle_pause()
    pause_btn.config(text="Resume" if currently_pause else "Pause")


def reset_stopwatch():
    reset()
    time_label.config(text="00:00:00")
    start_btn.config(state=tk.NORMAL)
    pause_btn.config(state=tk.DISABLED)
    pause_btn.config(text="Pause")
    messagebox.showinfo("Success", "Reset successfully")


start_btn = tk.Button(controls_frame, text="Start", bg=ACCENT_GREEN, command=start_stopwatch, **BTN_COMMON)
pause_btn = tk.Button(controls_frame, text="Pause", bg=ACCENT_ORANGE, state=tk.DISABLED, command=pause_stopwatch, **BTN_COMMON)
reset_btn = tk.Button(controls_frame, text="Reset", bg=ACCENT_RED, command=reset_stopwatch, **BTN_COMMON)

start_btn.grid(row=0, column=0, padx=8)
pause_btn.grid(row=0, column=1, padx=8)
reset_btn.grid(row=0, column=2, padx=8)

# ---------------- Lap List ----------------
list_frame = tk.Frame(root, bg=BG_COLOR)
list_frame.pack(pady=15)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lap_list = tk.Listbox(
    list_frame,
    width=32,
    height=8,
    font=("Consolas", 11),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectbackground=ACCENT_BLUE,
    relief="flat",
    highlightthickness=0,
    yscrollcommand=scrollbar.set
)
lap_list.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=lap_list.yview)

# ---------------- Lap / Clear / Export Controls ----------------
secondary_frame = tk.Frame(root, bg=BG_COLOR)
secondary_frame.pack(pady=15)


def lap():
    global lap_count
    current_time = f"{main.hours:02}:{main.minute:02}:{main.second:02}"
    lap_list.insert(tk.END, f"Lap {lap_count}: {current_time}")
    lap_list.see(tk.END)
    lap_count += 1


def clear_lap():
    global lap_count
    lap_list.delete(0, tk.END)
    lap_count = 1


def export_laps():
    laps = lap_list.get(0, tk.END)
    if len(laps) == 0:
        messagebox.showinfo("Warning", "No laps to export!")
        return

    file_path = filedialog.asksaveasfilename(
        initialfile="laps.txt",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Laps As"
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            for lap_entry in laps:
                file.write(lap_entry + "\n")
        messagebox.showinfo("Success", "Laps exported successfully!")


lap_btn = tk.Button(secondary_frame, text="Lap", bg=ACCENT_BLUE, command=lap, **BTN_COMMON)
clear_btn = tk.Button(secondary_frame, text="Clear", bg=ACCENT_GRAY, command=clear_lap, **BTN_COMMON)
export_btn = tk.Button(secondary_frame, text="Export", bg=ACCENT_GRAY, command=export_laps, **BTN_COMMON)

lap_btn.grid(row=0, column=0, padx=8)
clear_btn.grid(row=0, column=1, padx=8)
export_btn.grid(row=0, column=2, padx=8)

# ---------------- Footer ----------------
footer_label = tk.Label(
    root,
    text=f"Developed by {DEVELOPER_NAME}",
    font=("Arial", 9, "italic"),
    bg=BG_COLOR,
    fg=ACCENT_GRAY
)
footer_label.pack(side=tk.BOTTOM, pady=12)

# ---------------- Keyboard Shortcuts ----------------
def handle_space(event):
    if start_btn["state"] == tk.NORMAL:
        start_stopwatch()
    elif pause_btn["state"] == tk.NORMAL:
        pause_stopwatch()


def handle_reset_key(event):
    reset_stopwatch()


def handle_lap_key(event):
    if pause_btn["state"] == tk.NORMAL:
        lap()


root.bind("<space>", handle_space)
root.bind("r", handle_reset_key)
root.bind("R", handle_reset_key)
root.bind("l", handle_lap_key)
root.bind("L", handle_lap_key)

# ---------------- Timer Loop ----------------
def running_loop():
    new_time = update_time()
    time_label.config(text=new_time)
    root.after(1000, running_loop)


running_loop()
root.mainloop()
