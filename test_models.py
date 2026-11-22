"""Fallback logic against a fake client."""
import models


class M:
    def __init__(s, name, acts=("generateContent",)): s.name, s.supported_actions = name, list(acts)


class Chunk:
    def __init__(s, t): s.text = t


class Fake:
    def __init__(s, dead): s.dead, s.tried = dead, []
    @property
    def models(s): return s
    def list(s):
        return [M("models/gemini-2.5-flash"), M("models/gemini-3.8-flash"), M("models/gemini-3.5-flash-lite"),
                M("models/gemini-3.7-flash"), M("models/gemini-3.8-flash-image"), M("models/gemini-3.8-pro"),
                M("models/gemini-3.7-flash-live", acts=("bidiGenerateContent",))]
    def generate_content_stream(s, model, contents):
        s.tried.append(model)
        if model in s.dead:
            raise RuntimeError("503 UNAVAILABLE" if "3.8" in model else "404 NOT_FOUND")
        yield Chunk("ok ")
        yield Chunk(model)


c = Fake(dead={"gemini-3.8-flash", "gemini-3.7-flash"})
import os, tempfile
models.SAVED = os.path.join(tempfile.mkdtemp(), ".last_model")
models._chain = []
assert models.flash_models(c, "gemini-3.8-flash") == [
    "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite"], models.flash_models(c, "gemini-3.8-flash")
assert "gemini-2.5-flash" not in models.flash_models(c, "gemini-2.5-flash")  # old saved model ignored
got = []
models.answer(c, "gemini-3.8-flash", b"x", "p", got.append)
assert got[-1] == "ok gemini-3.5-flash-lite" and "gemini-2.5-flash" not in c.tried, (got, c.tried)

c.tried.clear()
models.answer(c, "gemini-3.8-flash", b"x", "p", got.append)
assert c.tried == ["gemini-3.5-flash-lite"], c.tried  # remembers the working model, no re-probing
models._chain = []
assert open(models.SAVED).read() == "gemini-3.5-flash-lite"

bad = Fake(dead=set())
models._chain = []
bad.generate_content_stream = lambda model, contents: (_ for _ in ()).throw(RuntimeError("400 API key not valid"))
got = []
models.answer(bad, "gemini-3.8-flash", b"x", "p", got.append)
assert got[-1] == "error: 400 API key not valid" and len(got) == 2, got
print("ALL OK")
