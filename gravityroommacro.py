"""
Reqs:
pip install mss opencv-python pillow numpy keyboard pytesseract
install tesseract OCR
"""

import threading
import time
import traceback
import tkinter.simpledialog as simpledialog
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
import mss
import pytesseract
import re
import os, sys
import ctypes
import os

#fix
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware() 
    except Exception:
        pass

try:
    import keyboard
except Exception:
    keyboard = None

#tesseract path :)))) (update)
def get_tesseract_path():
    import sys, os
    try:
        base_path = sys._MEIPASS  # wiggly cat wiggling in hand
    except Exception:
        base_path = os.path.abspath(".")

    # wiggle cat wiggle wiggle cat on hand
    local_path = os.path.join(base_path, "tesseract", "tesseract.exe")
    if os.path.exists(local_path):
        return local_path

    # maybe u have it installed on windows idk
    system_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for path in system_paths:
        if os.path.exists(path):
            return path

    return None

tesseract_cmd = get_tesseract_path()
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
else:
    print("Tesseract not found. Place the 'tesseract' carpet in the same path as the exe.")

def preprocess_for_ocr(img_bgra: np.ndarray):
    if img_bgra is None:
        return None
    gray = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2GRAY)
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    # Adaptive threshold instead of Otsu
    th = cv2.adaptiveThreshold(gray, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV,
                               31, 15)
    return th

def recognize_text(img_bgra: np.ndarray):
    prep = preprocess_for_ocr(img_bgra)
    if prep is None:
        return ""
    config = "--psm 7 --oem 3 -c tessedit_char_whitelist=WASD"
    text = pytesseract.image_to_string(prep, config=config)
    letters = re.findall(r"[WASD]", text)
    return "".join(letters)


# macro
class GameBotGUI:
    def __init__(self, root: tk.Toplevel):
        self.root = root

        self.region = None
        self.running = False
        self.bot_thread = None

        self.interval_read = tk.DoubleVar(value=0.7)
        self.interval_type = tk.DoubleVar(value=0.04)
        self.start_key = tk.StringVar(value="F4")
        self.stop_key = tk.StringVar(value="F6")

        self.status_text = tk.StringVar(value="Sin región")
        self.last_detected = tk.StringVar(value="Last: -")
        self.read_val_label = tk.StringVar(value=f"{self.interval_read.get():.2f}s")
        self.type_val_label = tk.StringVar(value=f"{self.interval_type.get():.3f}s")

        self._build_ui()
        self.preview_imgtk = None
        self.preview_loop()
        self.register_hotkeys()

        self.interval_read.trace_add(
            "write", lambda *a: self.read_val_label.set(f"{self.interval_read.get():.2f}s")
        )
        self.interval_type.trace_add(
            "write", lambda *a: self.type_val_label.set(f"{self.interval_type.get():.3f}s")
        )

    def _build_ui(self):
        self.root.title("DBOG Gravity Room Macro")
        self.root.geometry("760x650")

        left = ttk.Frame(self.root)
        left.pack(side="left", padx=8, pady=8)

        self.canvas = tk.Label(left, bd=2, relief="sunken", width=520, height=360)
        self.canvas.pack()

        ttk.Label(left, textvariable=self.status_text).pack(pady=4)
        ttk.Label(left, textvariable=self.last_detected, font=("Consolas", 10)).pack()

        right = ttk.Frame(self.root)
        right.pack(side="left", fill="y", padx=8, pady=8)

        ttk.Button(right, text="Select Area (Drag)", command=self.open_selector).pack(fill="x", pady=4)
        ttk.Button(right, text="Start Macro", command=self.start_bot).pack(fill="x", pady=4)
        ttk.Button(right, text="Stop Macro", command=self.stop_bot).pack(fill="x", pady=4)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=6)

        ttk.Label(right, text="Reading Interval (seconds)").pack(anchor="w")
        f_read = ttk.Frame(right)
        f_read.pack(fill="x", pady=2)
        ttk.Scale(
            f_read, from_=0.1, to=2.0, orient="horizontal", variable=self.interval_read
        ).pack(side="left", fill="x", expand=True)
        ttk.Label(f_read, textvariable=self.read_val_label, width=8).pack(side="left", padx=6)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(right, text="Interval Presets").pack(anchor="w")

        frame_presets = ttk.Frame(right)
        frame_presets.pack(fill="x", pady=4)

        ttk.Button(frame_presets, text="Health", command=lambda: self.set_reading_preset(0.9)).pack(fill="x", pady=2)
        ttk.Button(frame_presets, text="Agility", command=lambda: self.set_reading_preset(0.8)).pack(fill="x", pady=2)
        ttk.Button(frame_presets, text="Ki Control", command=lambda: self.set_reading_preset(0.75)).pack(fill="x", pady=2)
        ttk.Button(frame_presets, text="Physical Damage", command=lambda: self.set_reading_preset(0.8)).pack(fill="x", pady=2)
        ttk.Button(frame_presets, text="Ki Damage", command=lambda: self.set_reading_preset(1.15)).pack(fill="x", pady=2)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=6)

        ttk.Label(right, text="Typing Interval (seconds)").pack(anchor="w")
        f_type = ttk.Frame(right)
        f_type.pack(fill="x", pady=2)
        ttk.Scale(
            f_type, from_=0.01, to=0.5, orient="horizontal", variable=self.interval_type
        ).pack(side="left", fill="x", expand=True)
        ttk.Label(f_type, textvariable=self.type_val_label, width=8).pack(side="left", padx=6)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=6)

        ttk.Label(right, text="Start Hotkey").pack(anchor="w")
        ttk.Entry(right, textvariable=self.start_key).pack(fill="x", pady=2)
        ttk.Label(right, text="Stop Hotkey").pack(anchor="w")
        ttk.Entry(right, textvariable=self.stop_key).pack(fill="x", pady=2)
        ttk.Button(right, text="Apply hotkeys", command=self.register_hotkeys).pack(fill="x", pady=6)

    def set_reading_preset(self, value: float):
        self.interval_read.set(value)

    def preview_loop(self):
        try:
            if self.region:
                with mss.mss() as sct:
                    img = np.array(sct.grab(self.region))
                if img is not None:
                    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
                    h, w = frame.shape[:2]
                    max_w = 520
                    scale = min(1.0, max_w / w)
                    display = cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
                    im = Image.fromarray(display)
                else:
                    im = Image.new("RGB", (520, 360), (50, 50, 50))
            else:
                im = Image.new("RGB", (520, 360), (24, 24, 24))
            imgtk = ImageTk.PhotoImage(im)
            self.preview_imgtk = imgtk
            self.canvas.configure(image=imgtk)
        except Exception:
            print("Preview error:", traceback.format_exc())
        finally:
            self.root.after(80, self.preview_loop)

    def open_selector(self):
        self.region = None
        self.status_text.set("Selecting area...")

        sel = tk.Toplevel(self.root)
        sel.overrideredirect(True)
        sel.lift()
        sel.attributes("-alpha", 0.28)
        sel.config(bg="black")

        try:
            user32 = ctypes.windll.user32
            screen_w, screen_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        except Exception:
            screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        sel.geometry(f"{screen_w}x{screen_h}+0+0")

        canvas = tk.Canvas(sel, cursor="cross", bg="black", width=screen_w, height=screen_h, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        coords = {}
        rect_id = None

        def on_press(e):
            coords["x1"], coords["y1"] = e.x, e.y

        def on_drag(e):
            nonlocal rect_id
            x2, y2 = e.x, e.y
            if rect_id:
                canvas.delete(rect_id)
            rect_id = canvas.create_rectangle(coords["x1"], coords["y1"], x2, y2, outline="red", width=2)

        def on_release(e):
            x1, y1 = coords["x1"], coords["y1"]
            x2, y2 = e.x, e.y
            left, top = min(x1, x2), min(y1, y2)
            width, height = abs(x2 - x1), abs(y2 - y1)

            if width < 5 or height < 5:
                self.status_text.set("Invalid selection, try again")
                sel.destroy()
                return

            self.region = {"left": int(left), "top": int(top), "width": int(width), "height": int(height)}
            self.status_text.set(f"Área: {self.region}")
            sel.destroy()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

    def capture_region_image(self):
        if not self.region:
            return None
        try:
            with mss.mss() as sct:
                return np.array(sct.grab(self.region))
        except Exception as e:
            print("Capture error", e)
            return None

    def bot_loop(self):
        try:
            while self.running:
                img = self.capture_region_image()
                if img is None:
                    time.sleep(self.interval_read.get())
                    continue
                seq = recognize_text(img)
                if seq:
                    self.root.after(0, lambda s=seq: self.last_detected.set(f"Last: {s}"))
                    try:
                        for ch in seq:
                            if keyboard:
                                keyboard.press_and_release(ch.lower())
                            time.sleep(self.interval_type.get())
                    except Exception:
                        print("Error sending keys:", traceback.format_exc())
                else:
                    self.root.after(0, lambda: self.last_detected.set("Last: -"))
                time.sleep(self.interval_read.get())
        except Exception:
            print("bot_loop: exception", traceback.format_exc())
        finally:
            self.running = False
            self.root.after(0, lambda: self.status_text.set("Bot stopped (error or manually)"))

    def start_bot(self):
        if not self.region:
            self.status_text.set("Select area before starting")
            return
        if self.running:
            self.status_text.set("Macro already executing")
            return
        self.running = True
        self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
        self.bot_thread.start()
        self.status_text.set("Macro started")

    def stop_bot(self):
        if not self.running:
            self.status_text.set("Macro already stopped")
            return
        self.running = False
        self.status_text.set("Macro stopped")

    def register_hotkeys(self):
        if keyboard is None:
            self.status_text.set("Hotkeys not available (open as admin)")
            return
        try:
            keyboard.clear_all_hotkeys()
        except Exception:
            pass
        start_k = self.start_key.get().strip() or "F5"
        stop_k = self.stop_key.get().strip() or "F6"
        try:
            keyboard.add_hotkey(start_k, lambda: self.root.after(0, self.start_bot))
            keyboard.add_hotkey(stop_k, lambda: self.root.after(0, self.stop_bot))
            self.status_text.set(f"Hotkeys: Start={start_k} Stop={stop_k}")
        except Exception as e:
            self.status_text.set(f"Error hotkeys: {e}")

#launcher
class DBOGToolsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("DBOG Tools")
        self.root.geometry("400x280")

        ttk.Label(root, text="DBOG Tools", font=("Segoe UI", 14, "bold")).pack(pady=20)
        ttk.Label(root, text="by AmmonNH3", font=("Segoe UI", 11, "bold")).pack(pady=1) 

        ttk.Label(root, text="Special thanks: spxeedy on discord", font=("Segoe UI", 9)).pack(pady=4)
        
        ttk.Button(
            root,
            text="Gravity Room Macro (Jank)",
            command=self.open_macro
        ).pack(pady=10, fill="x", padx=40)      

        ttk.Button(
            root,
            text="Exit",
            command=root.quit
        ).pack(side="bottom", pady=20)

    def open_macro(self):
        macro_win = tk.Toplevel(self.root)
        GameBotGUI(macro_win) 

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    root = tk.Tk()
    try:
        icon_path = resource_path("dbog.ico") #icon for the app
        root.iconbitmap(icon_path)
    except Exception as e:
        print("Icon could not be loaded:", e)
    app = DBOGToolsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
