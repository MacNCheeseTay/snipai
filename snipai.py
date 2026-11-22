"""Hotkey screenshot/snip -> Gemini -> answer in a hidden-from-capture overlay.

Ctrl+Alt+A  full screen    Ctrl+Alt+S  snip region
Ctrl+Alt+H  hide overlay   Ctrl+Alt+Q  quit
Needs GEMINI_API_KEY. Optional SNIPAI_MODEL.
"""
import ctypes, io, os, queue, threading, tkinter as tk
from ctypes import wintypes
from PIL import Image, ImageGrab, ImageTk
from google import genai
from google.genai import types

MODEL = os.environ.get("SNIPAI_MODEL", "gemini-2.5-flash")
PROMPT = "Answer the question or solve the problem shown in this image. Be as brief as possible."
MOD = 0x0002 | 0x0001 | 0x4000  # ctrl | alt | norepeat
HOTKEYS = {1: (0x41, "full"), 2: (0x53, "snip"), 3: (0x48, "hide"), 4: (0x51, "quit")}

u32 = ctypes.windll.user32
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

events: queue.Queue = queue.Queue()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def hotkey_thread():
    for i, (vk, _) in HOTKEYS.items():
        if not u32.RegisterHotKey(None, i, MOD, vk):
            print(f"hotkey {i} already taken")
    msg = wintypes.MSG()
    while u32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
        if msg.message == 0x0312:
            events.put(HOTKEYS[msg.wParam][1])


def style_hidden(win):
    """No taskbar, no focus, click-through, excluded from screen capture."""
    win.update_idletasks()
    hwnd = u32.GetParent(win.winfo_id()) or win.winfo_id()
    ex = u32.GetWindowLongW(hwnd, -20)
    u32.SetWindowLongW(hwnd, -20, ex | 0x80 | 0x08000000 | 0x20 | 0x80000)  # toolwindow noactivate transparent layered
    u32.SetWindowDisplayAffinity(hwnd, 0x11)  # WDA_EXCLUDEFROMCAPTURE


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.ov = tk.Toplevel(self.root)
        self.ov.overrideredirect(True)
        self.ov.attributes("-topmost", True, "-alpha", 0.8)
        self.ov.configure(bg="#111")
        self.txt = tk.Label(self.ov, bg="#111", fg="#ddd", font=("Consolas", 10),
                            justify="left", wraplength=420, anchor="nw", padx=8, pady=6)
        self.txt.pack()
        sw = self.root.winfo_screenwidth()
        self.ov.geometry(f"+{sw - 450}+20")
        style_hidden(self.ov)
        self.ov.withdraw()
        self.busy = False
        threading.Thread(target=hotkey_thread, daemon=True).start()
        self.root.after(50, self.poll)

    def poll(self):
        try:
            while True:
                ev = events.get_nowait()
                if ev == "quit":
                    self.root.destroy()
                    return
                if ev == "hide":
                    self.ov.withdraw()
                elif not self.busy:
                    self.capture(ev)
        except queue.Empty:
            pass
        self.root.after(50, self.poll)

    def show(self, text):
        self.txt.config(text=text)
        self.ov.deiconify()

    def capture(self, mode):
        self.ov.withdraw()
        self.root.update()
        img = ImageGrab.grab(all_screens=True)
        if mode == "snip":
            box = self.snip(img)
            if not box:
                return
            img = img.crop(box)
        self.busy = True
        self.show("...")
        threading.Thread(target=self.ask, args=(img,), daemon=True).start()

    def snip(self, img):
        x0, y0 = u32.GetSystemMetrics(76), u32.GetSystemMetrics(77)
        w, h = img.size
        top = tk.Toplevel(self.root)
        top.overrideredirect(True)
        top.attributes("-topmost", True)
        top.geometry(f"{w}x{h}+{x0}+{y0}")
        cv = tk.Canvas(top, width=w, height=h, highlightthickness=0, cursor="crosshair")
        cv.pack()
        photo = ImageTk.PhotoImage(img)
        cv.create_image(0, 0, image=photo, anchor="nw")
        sel, rect = {}, [None]

        def down(e):
            sel["a"] = (e.x, e.y)
            rect[0] = cv.create_rectangle(e.x, e.y, e.x, e.y, outline="red", width=2)

        def drag(e):
            cv.coords(rect[0], *sel["a"], e.x, e.y)

        def up(e):
            sel["b"] = (e.x, e.y)
            top.destroy()

        cv.bind("<ButtonPress-1>", down)
        cv.bind("<B1-Motion>", drag)
        cv.bind("<ButtonRelease-1>", up)
        top.bind("<Escape>", lambda e: top.destroy())
        top.focus_force()
        self.root.wait_window(top)
        if "b" not in sel:
            return None
        (ax, ay), (bx, by) = sel["a"], sel["b"]
        box = (min(ax, bx), min(ay, by), max(ax, bx), max(ay, by))
        return box if box[2] - box[0] > 4 and box[3] - box[1] > 4 else None

    def ask(self, img):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "PNG")
        out = ""
        try:
            for ch in client.models.generate_content_stream(
                model=MODEL,
                contents=[types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png"), PROMPT],
            ):
                out += ch.text or ""
                self.root.after(0, self.show, out)
        except Exception as e:
            self.root.after(0, self.show, f"error: {e}")
        self.busy = False


if __name__ == "__main__":
    App().root.mainloop()
