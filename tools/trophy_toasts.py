#!/usr/bin/env python3
"""Local trophy notification viewer. No PSN integration.

Run: python tools/trophy_toasts.py <user-dir>
Uses a borderless, topmost Tk window when a desktop is available.
"""
import argparse
from pathlib import Path
import time
import tkinter as tk

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_dir", type=Path)
    args = parser.parse_args()
    path = args.user_dir / "trophy_events.log"
    offset = path.stat().st_size if path.exists() else 0
    root = tk.Tk()
    root.withdraw()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg="#191b22")
    frame = tk.Frame(root, bg="#191b22", padx=18, pady=12,
                     highlightbackground="#a98b4b", highlightthickness=1)
    frame.pack(fill="both", expand=True)
    icon_label = tk.Label(frame, text="🏆", font=("Segoe UI Emoji", 24),
                          bg="#191b22", fg="#e3bf70")
    icon_label.pack(side="left", padx=(0, 12))
    info = tk.Frame(frame, bg="#191b22")
    info.pack(side="left", fill="both", expand=True)
    tk.Label(info, text="GOD OF WAR III REMASTERED", font=("Segoe UI", 9, "bold"),
             fg="#d3b16a", bg="#191b22", anchor="w").pack(fill="x")
    title = tk.Label(info, text="", font=("Segoe UI", 12, "bold"),
                     fg="#ffffff", bg="#191b22", anchor="w")
    title.pack(fill="x")
    hide_job = None
    photo = None

    def hide():
        root.withdraw()

    def show(trophy_id):
        nonlocal hide_job, photo
        title.configure(text=f"Conquista desbloqueada! (ID {trophy_id})")
        icon_path = args.user_dir / "trophy_icons" / f"TROP{trophy_id:03d}.PNG"
        photo = None
        if icon_path.is_file():
            try:
                from PIL import Image, ImageTk
                with Image.open(icon_path) as im:
                    im = im.convert("RGBA")
                    im.thumbnail((48, 48))
                    photo = ImageTk.PhotoImage(im)
                icon_label.configure(image=photo, text="")
            except (ImportError, OSError):
                pass
        if photo is None:
            icon_label.configure(image="", text="🏆")
        width, height = 430, 86
        x = max(0, (root.winfo_screenwidth() - width) // 2)
        root.geometry(f"{width}x{height}+{x}+24")
        root.deiconify()
        root.lift()
        if hide_job is not None:
            root.after_cancel(hide_job)
        hide_job = root.after(5500, hide)

    def poll():
        nonlocal offset
        try:
            if path.exists():
                size = path.stat().st_size
                if size < offset:
                    offset = 0
                with path.open("r", encoding="utf-8", errors="replace") as file:
                    file.seek(offset)
                    lines = file.readlines()
                    offset = file.tell()
                for line in lines:
                    value = line.strip()
                    if value.isdecimal() and 0 <= int(value) < 35:
                        show(int(value))
        except OSError as exc:
            print(f"Trophy viewer: {exc}")
        root.after(500, poll)

    print(f"Watching {path} for trophy events (Ctrl+C to stop)")
    root.after(500, poll)
    root.mainloop()

if __name__ == "__main__":
    main()
