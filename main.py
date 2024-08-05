import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk
import time


def switch_to_break_theme():
    global style1
    global style
    global style_frame
    global style2

    work_break_label.config(text="Break Time", background=start_color, foreground=background_color)
    time_label.config(background=start_color, foreground=background_color)
    style.configure("c.TButton", background=start_color, foreground=background_color)
    style1.configure("c1.TButton", background=start_color)
    style_frame.configure("c.TFrame", background=start_color)
    style2.configure("c2.TButton", background=start_color, foreground=background_color)
    window.config(background=start_color)

def switch_to_work_theme():
    global style1
    global style
    global style_frame
    global style2

    work_break_label.config(text="Work Time", background=background_color, foreground=label_color)
    time_label.config(background=background_color, foreground=label_color)
    style.configure("c.TButton", background=start_color, foreground=background_color)
    style1.configure("c1.TButton", background=reset_color)
    style_frame.configure("c.TFrame", background=background_color)
    style2.configure("c2.TButton", background=background_color, foreground=label_color)
    window.config(background=background_color)

def format_time(t):
    str_t = str(t)
    if len(str_t) == 1:
        str_t = "0" + str_t
    return str_t

def start_countdown(clicked=False, reset=False, stop=False):
    global seconds
    global minutes
    global start_pause_switch
    global start
    global reset_settings
    global work_break_switch

    if clicked:
        start_pause_switch += 1
        if start_pause_switch % 2 == 0:
            start_button.config(text="Start")
            start = False
        else:
            start_button.config(text="Pause")
            start = True

    if reset:
        minutes = reset_settings[0]
        seconds = reset_settings[1]
        time_label.config(text=reset_settings[2])
        return
    if stop:
        return
    elif start:
        if seconds != 0:
            seconds -= 1

        elif minutes == 0 and seconds == 0:
            work_break_switch += 1
            if work_break_switch % 2 == 0:
                # work
                switch_to_work_theme()
                minutes = work_minutes
                seconds = 10
                text = f"{format_time(minutes+1)}:00"
                reset_settings = [minutes, seconds, text]
            else:
                switch_to_break_theme()
                minutes = break_minutes
                seconds = break_seconds
                text = f"{format_time(minutes+1)}:00"
                reset_settings = [minutes, seconds, text]
                time_label.config(text=text)

        else:
            minutes -= 1
            seconds = 59

        str_minutes = format_time(minutes)
        str_secs = format_time(seconds)

        time_label.config(text=str_minutes + ":" + str_secs)
        window.after(100, start_countdown)

def full_reset():
    global work_minutes, work_seconds, break_minutes, break_seconds, minutes, seconds, reset_settings, start_pause_switch, work_break_switch, start

    work_minutes = 0
    work_seconds = 59
    break_minutes = 0
    break_seconds = 10

    minutes = work_minutes
    seconds = work_seconds
    reset_settings = [minutes, seconds, f"{format_time(minutes + 1)}:00"]
    start = True

    switch_to_work_theme()

    start_countdown(0, 1, 1)

def center_window(w, h, win, push_y=0, push_x=0):
    x_coordinate = int((win.winfo_screenwidth() / 2) - (w / 2)) + push_x
    y_coordinate = int((win.winfo_screenheight() / 2) - (h / 2)) + push_y
    win.geometry(f"{w}x{h}+{x_coordinate}+{y_coordinate}")

work_minutes = 0
work_seconds = 59
break_minutes = 0
break_seconds = 10

minutes = work_minutes
seconds = work_seconds
reset_settings = [minutes, seconds, f"{format_time(minutes+1)}:00"]
start_pause_switch = 0
work_break_switch = 0
start = True

 # Colors
background_color = "#A02334"
label_color = "#FFAD60"
start_color = "#FFEEAD"
reset_color = "#FFAD60"
special_color = "#96CEB4"

# Fonts
font_large = ("Courier", 50)
font_small = ("Courier", 10)

# Window
window = tb.Window(resizable=(False, False))
window.title("Pomodoro")
center_window(600, 450, window,50)
window.configure(background=background_color, pady=10)

time_label = tb.Label(window, text=f"{format_time(work_minutes+1)}:00", font=font_large,
                      background=background_color,
                      foreground=label_color)
time_label.pack(pady=(50, 0))

work_break_label = tb.Label(window, text="Work Time",  font=font_small,
                            background=background_color,
                            foreground=label_color)
work_break_label.pack()

style_frame = tb.Style()
style_frame.configure('c.TFrame', background=background_color)
buttons_frame = tb.Frame(window, style="c.TFrame")
buttons_frame.pack(pady=(20))

style = tb.Style()
style.configure("c.TButton", background=start_color,
                borderwidth=0,
                foreground=background_color,
                font=('Courier', 15))

style1 = tb.Style()
style1.configure("c1.TButton", background=reset_color,
                borderwidth=0,
                foreground=background_color,
                font=('Courier', 15))

style2 = tb.Style()
style2.configure("c2.TButton", background=background_color,
                borderwidth=0,
                foreground=label_color,
                font=('Courier', 10))

start_button = tb.Button(buttons_frame,
                         text="Start",
                         style="c.TButton",
                         command= lambda: start_countdown(1))
start_button.grid(row=0, column=0, padx=15, pady=(30,0))

reset_button = tb.Button(buttons_frame,
                         text="Reset",
                         style="c1.TButton",
                         command= lambda: start_countdown(False, True))
reset_button.grid(row=0, column=1, padx=15, pady=(30,0))

full_reset_button = tb.Button(window,
                         text="Full Reset",
                         style="c2.TButton",
                         command= full_reset)
full_reset_button.pack()


window.mainloop()