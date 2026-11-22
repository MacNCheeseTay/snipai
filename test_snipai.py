"""Smoke test: real hotkeys, real capture, real snip drag, capture-exclusion flag. Gemini call is mocked."""
import ctypes, os, time
os.environ.setdefault("GEMINI_API_KEY", "x")
import snipai

u32 = ctypes.windll.user32
KEYUP = 2


def press(*vks):
    for v in vks:
        u32.keybd_event(v, 0, 0, 0)
    for v in reversed(vks):
        u32.keybd_event(v, 0, KEYUP, 0)


def pump(app, secs):
    end = time.time() + secs
    while time.time() < end:
        app.root.update()
        time.sleep(0.02)


app = snipai.App()
got = []
app.ask = lambda img: (got.append(img.size), setattr(app, "busy", False))
pump(app, 0.5)

press(0x11, 0x12, 0x41)  # ctrl alt A
pump(app, 1.5)
assert got, "full-screen hotkey did nothing"
print("full", got[-1])

def drag():
    u32.SetCursorPos(100, 100); time.sleep(0.2)
    u32.mouse_event(2, 0, 0, 0, 0); time.sleep(0.2)
    u32.SetCursorPos(400, 300); time.sleep(0.2)
    u32.mouse_event(4, 0, 0, 0, 0)

app.root.after(1000, drag)
press(0x11, 0x12, 0x53)  # ctrl alt S
pump(app, 3)
assert len(got) == 2 and got[-1] == (300, 200), f"snip wrong: {got}"
print("snip", got[-1])

app.show("x"); app.root.update()
hwnd = u32.GetParent(app.ov.winfo_id()) or app.ov.winfo_id()
aff = ctypes.c_uint(); u32.GetWindowDisplayAffinity(hwnd, ctypes.byref(aff))
assert aff.value == 0x11, f"affinity {aff.value:#x}"
print("affinity ok")
press(0x11, 0x12, 0x48); pump(app, 0.5)
assert not app.ov.winfo_viewable(), "hide failed"
print("ALL OK")
