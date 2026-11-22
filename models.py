"""Gemini call shared by both platforms: tries every available flash model, newest first."""
import os, re, time
from google.genai import types

SKIP = ("image", "tts", "live", "audio", "embedding", "robotics", "computer")
STATIC = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-3-flash-preview"]
RETRYABLE = ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "timed out", "Timeout")
TIMEOUT_MS = 8000  # per request, so a hung model can't freeze the app


SAVED = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".last_model")


def _saved():
    try:
        return open(SAVED).read().strip() or None
    except OSError:
        return None


def flash_models(client, first):
    try:
        names = [m.name.removeprefix("models/") for m in client.models.list()
                 if "generateContent" in (m.supported_actions or []) and "flash" in m.name
                 and not any(s in m.name for s in SKIP)]
    except Exception:
        names = []
    names = sorted({n for n in names or STATIC if gen3(n)}, key=lambda n: ("lite" in n, [-int(x) for x in re.findall(r"\d+", n)]))
    return ([first] if gen3(first) else []) + [n for n in names if n != first]


def gen3(name):
    """Gemini 3 or newer only: older models are closed to new users and just waste a request."""
    v = re.findall(r"\d+", name)
    return not v or int(v[0]) >= 3


_chain = []


def answer(client, first, png, prompt, show):
    global _chain
    if not _chain:
        _chain = flash_models(client, _saved() or first)[:6]
    chain = _chain
    err = ""
    for rnd in range(2):
        for m in chain:
            out = ""
            show(f"trying {m}...")
            try:
                for ch in client.models.generate_content_stream(
                    model=m, contents=[types.Part.from_bytes(data=png, mime_type="image/png"), prompt]
                ):
                    out += ch.text or ""
                    show(out)
                _chain = [m] + [x for x in chain if x != m]
                open(SAVED, "w").write(m)
                return
            except Exception as e:
                if out:
                    show(f"{out}\n[cut off: {e}]")
                    return
                err = str(e)
                if "API key" in err or "UNAUTHENTICATED" in err:
                    show(f"error: {err}")
                    return
        if not any(c in err for c in RETRYABLE) or rnd == 1:
            break
        show("all flash models busy, retrying...")
        time.sleep(3)
    show(f"error: {err}")
