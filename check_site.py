"""Run with python3 check_site.py before publishing the static blog."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import struct

ROOT = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links, self.images = set(), [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, ("duplicate id", attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs["href"])
        if tag == "img":
            assert attrs.get("alt"), "missing image description"
            self.images.append(attrs["src"])


pages = {name: Page(ROOT / name) for name in ("index.html", "diet-plan.html", "workout-plan.html")}
images = set()
for name, page in pages.items():
    for reference in page.links + page.images:
        url = urlsplit(reference)
        if url.scheme:
            assert url.scheme == "https", (name, "unexpected external URL", reference)
            continue
        path = unquote(url.path)
        assert not path.startswith("/") and ".." not in Path(path).parts, (name, "use relative site links", reference)
        target = path or name
        assert (ROOT / target).is_file(), (name, "missing file", reference)
        if url.fragment:
            assert target in pages and unquote(url.fragment) in pages[target].ids, (name, "broken anchor", reference)
    images.update(page.images)

assert {"diet-plan.html", "workout-plan.html"} <= set(pages["index.html"].links)
assert all("index.html" in pages[name].links for name in ("diet-plan.html", "workout-plan.html"))
assert len(images) == 16
for filename in images:
    data = (ROOT / filename).read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", data[16:24]) == (1536, 1024), filename
assert (ROOT / ".nojekyll").is_file()
assert "<script" not in (ROOT / "index.html").read_text(), "Homepage does not need JavaScript"
print("PASS: 3 pages, 16 illustrations, all relative links and anchors, home navigation and Pages entry.")
