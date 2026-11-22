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
assert models.flash_models(c, "gemini-3.8-flash") == [
    "gemini-3.8-flash", "gemini-3.7-flash", "gemini-2.5-flash", "gemini-3.5-flash-lite"], models.flash_models(c, "gemini-3.8-flash")
got = []
models.answer(c, "gemini-3.8-flash", b"x", "p", got.append)
assert got[-1] == "ok gemini-2.5-flash" and c.tried == ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-2.5-flash"], (got, c.tried)

bad = Fake(dead=set())
bad.generate_content_stream = lambda model, contents: (_ for _ in ()).throw(RuntimeError("400 API key not valid"))
got = []
models.answer(bad, "gemini-3.8-flash", b"x", "p", got.append)
assert got == ["error: 400 API key not valid"], got
print("ALL OK")
