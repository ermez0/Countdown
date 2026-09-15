import sys
from pathlib import Path
import tkinter as tk
from tkinter import font
import json
import datetime

fullscreen = False
def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen",fullscreen)


def update_timer(target: datetime.datetime, timer_label: tk.Label, root: tk.Tk):
    now = datetime.datetime.now()
    remaining = target - now
    if remaining.total_seconds() <= 0:
        timer_label.config(text="Countdown Complete!")
        return
    days = remaining.days
    total_seconds =  remaining.total_seconds() - (days * 86400)
    hours, rem = divmod(total_seconds,3600)
    minutes, seconds = divmod(rem,60)
    ss = int((seconds - int(seconds)) * 100)
    seconds = int(seconds) 
    hours = int(hours)
    minutes = int(minutes)
    new_time = f"{days}d {hours}h {minutes}m {seconds}s {ss}ss"
    timer_label.config(text=new_time)
    root.after(10,update_timer,target,timer_label,root)

    
def main():
    if len(sys.argv) < 2:
        raise Exception("No config provided.")
    timer_path: Path = Path(sys.argv[1])
    with open(timer_path, encoding="utf-8") as f:
        timer_conf: dict = json.load(f)
    global root
    root = tk.Tk()
    root.title("Countdown")
    frame = tk.Frame(root)
    frame.pack(expand=True)
    frame.config(bg=timer_conf.get("bg_color","#000000"))
    main_text = tk.Label(
        frame,
        text=timer_conf.get("text","N/A"),
        fg=timer_conf.get("text_color","#FFFFFF"),
        bg=timer_conf.get("bg_color","#000000"),
        font=(timer_conf["font"].get("family","Times New Roman"),timer_conf["font"].get("size",32),timer_conf["font"].get("style","bold"))
        )
    timer_text = tk.Label(
        frame,
        text="No Timer Assigned",
        fg=timer_conf.get("countdown_color","#FFFFFF"),
        bg=timer_conf.get("bg_color","#000000"),
        font=(timer_conf["font"].get("family","Times New Roman"),timer_conf["font"].get("size",32),timer_conf["font"].get("style","bold"))
        )
    main_text.pack(pady=10)
    timer_text.pack(pady=10)
    root.bind("<F11>",toggle_fullscreen)
    root.configure(bg=timer_conf.get("bg_color","#000000"))
    year = timer_conf["datetime"].get("year",datetime.datetime.now().year)
    month = timer_conf["datetime"].get("month",datetime.datetime.now().month)
    day = timer_conf["datetime"].get("day",datetime.datetime.now().day)
    hour = timer_conf["datetime"].get("hour",datetime.datetime.now().hour)
    minute = timer_conf["datetime"].get("minute",datetime.datetime.now().minute)
    second = timer_conf["datetime"].get("second",datetime.datetime.now().second) 
    timer_date = datetime.datetime(year,month,day,hour,minute,second)
    update_timer(timer_date,timer_text,root)
    root.mainloop()
    

if __name__ == "__main__":
    main()