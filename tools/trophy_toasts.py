#!/usr/bin/env python3
"""Experimental Windows toast viewer for local God of War III trophy events.

Run separately while the game is active:
    python tools/trophy_toasts.py "C:\\path\\to\\user"
Only events appended after startup are displayed. No PSN integration.
"""
import argparse
from pathlib import Path
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_dir", type=Path, help="Port's configured user/save directory")
    args = parser.parse_args()
    path = args.user_dir / "trophy_events.log"
    offset = path.stat().st_size if path.exists() else 0
    print(f"Watching {path} for new trophy IDs (Ctrl+C to stop)")
    while True:
        if path.exists():
            size = path.stat().st_size
            if size < offset:
                offset = 0
            with path.open("r", encoding="utf-8", errors="replace") as f:
                f.seek(offset)
                lines = f.readlines()
                offset = f.tell()
            for line in lines:
                trophy_id = line.strip()
                if not trophy_id.isdecimal() or int(trophy_id) >= 128:
                    continue
                title = f"Conquista desbloqueada! (ID {trophy_id})"
                try:
                    from win10toast import ToastNotifier
                    ToastNotifier().show_toast("God of War III Remastered", title, duration=5, threaded=False)
                except (ImportError, OSError, RuntimeError):
                    print(title)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
