"""macOS: hotkey screenshot/snip -> Gemini -> answer in a hidden-from-capture overlay.

Ctrl+Opt+Cmd+A  full screen    Ctrl+Opt+Cmd+S  snip region
Ctrl+Opt+Cmd+H  hide overlay   Ctrl+Opt+Cmd+Q  quit
Needs GEMINI_API_KEY, plus Screen Recording and Accessibility permission for your terminal.
"""
import io, os, queue, subprocess, tempfile, threading, tkinter as tk
from AppKit import NSApp, NSApplication
from PIL import Image
from pynput import keyboard
from google import genai
import models

MODEL = os.environ.get("SNIPAI_MODEL", "gemini-3.8-flash")
PROMPT = "Answer the question or solve the problem shown in this image. Be as brief as possible."

events: queue.Queue = queue.Queue()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"), http_options=genai.types.HttpOptions(timeout=models.TIMEOUT_MS))


VKS = {0: "full", 1: "snip", 4: "hide", 12: "quit"}  # macOS key codes for A S H Q
held = set()


def mod(k):
    n = getattr(k, "name", "") or ""
    return next((m for m in ("ctrl", "alt", "cmd") if n.startswith(m)), None)


def on_press(k):
    m = mod(k)
    if m:
        held.add(m)
    elif held >= {"ctrl", "alt", "cmd"} and getattr(k, "vk", None) in VKS:
        events.put(VKS[k.vk])


def on_release(k):
    held.discard(mod(k))


def grab(snip):
    """screencapture: -x silent, -i -s interactive region select. None if cancelled."""
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "s.png")
        subprocess.run(["screencapture", "-x"] + (["-i", "-s"] if snip else []) + [f])
        if not os.path.exists(f):
            return None
        img = Image.open(f)
        img.load()
        return img


def hide_from_capture():
    """No capture, click-through, above everything, on every Space."""
    for w in NSApp.windows():
        w.setSharingType_(0)  # NSWindowSharingNone
        w.setIgnoresMouseEvents_(True)
        w.setLevel_(25)  # NSStatusWindowLevel
        w.setCollectionBehavior_(1 | 256)  # all spaces | fullscreen auxiliary


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        NSApplication.sharedApplication().setActivationPolicy_(1)  # no Dock icon
        self.ov = tk.Toplevel(self.root)
        self.ov.overrideredirect(True)
        self.ov.attributes("-topmost", True, "-alpha", 0.8)
        self.ov.configure(bg="#111")
        self.txt = tk.Label(self.ov, bg="#111", fg="#ddd", font=("Menlo", 11),
                            justify="left", wraplength=420, anchor="nw", padx=8, pady=6)
        self.txt.pack()
        self.ov.geometry(f"+{self.root.winfo_screenwidth() - 450}+40")
        self.ov.withdraw()
        self.busy = False
        keyboard.Listener(on_press=on_press, on_release=on_release).start()
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
                    self.capture(ev == "snip")
        except queue.Empty:
            pass
        self.root.after(50, self.poll)

    def show(self, text):
        self.txt.config(text=text)
        self.ov.deiconify()
        self.ov.update_idletasks()
        hide_from_capture()

    def capture(self, snip):
        self.ov.withdraw()
        self.root.update()
        img = grab(snip)
        if img is None:
            return
        self.busy = True
        self.show("...")
        threading.Thread(target=self.ask, args=(img,), daemon=True).start()

    def ask(self, img):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "PNG")
        models.answer(client, MODEL, buf.getvalue(), PROMPT, lambda t: self.root.after(0, self.show, t))
        self.busy = False


if __name__ == "__main__":
    App().root.mainloop()
