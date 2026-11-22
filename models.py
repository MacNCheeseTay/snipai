"""Gemini call shared by both platforms: tries every available flash model, newest first."""
import re, time
from google.genai import types

SKIP = ("image", "tts", "live", "audio", "embedding", "robotics", "computer")
STATIC = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-3-flash-preview", "gemini-2.5-flash"]
RETRYABLE = ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")


def flash_models(client, first):
    try:
        names = [m.name.removeprefix("models/") for m in client.models.list()
                 if "generateContent" in (m.supported_actions or []) and "flash" in m.name
                 and not any(s in m.name for s in SKIP)]
    except Exception:
        names = []
    names = sorted(set(names or STATIC), key=lambda n: ("lite" in n, [-int(x) for x in re.findall(r"\d+", n)]))
    return [first] + [n for n in names if n != first]


def answer(client, first, png, prompt, show):
    chain = flash_models(client, first)
    err = ""
    for rnd in range(3):
        for m in chain:
            out = ""
            try:
                for ch in client.models.generate_content_stream(
                    model=m, contents=[types.Part.from_bytes(data=png, mime_type="image/png"), prompt]
                ):
                    out += ch.text or ""
                    show(out)
                return
            except Exception as e:
                if out:
                    show(f"{out}\n[cut off: {e}]")
                    return
                err = str(e)
                if "API key" in err or "UNAUTHENTICATED" in err:
                    show(f"error: {err}")
                    return
        if not any(c in err for c in RETRYABLE) or rnd == 2:
            break
        show(f"all flash models busy, retrying ({rnd + 1}/2)...")
        time.sleep(3 * (rnd + 1))
    show(f"error: {err}")
