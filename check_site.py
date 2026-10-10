"""Run with python3 check_site.py before publishing the static blog."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import struct

ROOT = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links, self.images = set(), [], []
        self.move_images, self.current_move = {}, None
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.current_move = attrs.get("id", "")
            if self.current_move.startswith(("move-", "abs-")):
                self.move_images[self.current_move] = []
            else:
                self.current_move = None
        if "id" in attrs:
            assert attrs["id"] not in self.ids, ("duplicate id", attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs["href"])
        if tag == "img":
            assert attrs.get("alt"), "missing image description"
            self.images.append(attrs["src"])
            if self.current_move:
                self.move_images[self.current_move].append(attrs["src"])

    def handle_endtag(self, tag):
        if tag == "article":
            self.current_move = None


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
assert len(images) == 38
move_images = pages["workout-plan.html"].move_images
assert set(move_images) == {f"move-{day}-{move}" for day in range(1, 5) for move in range(1, 7)} | {"abs-crunch", "abs-pallof"}
assert all(move_images.values()), ("missing exercise illustration", [id for id, sources in move_images.items() if not sources])
assert {"assets/dumbbell-curl.png", "assets/triceps-pushdown.png"} <= set(move_images["move-3-6"])
assert {"assets/dead-bug.png", "assets/hanging-knee-raise.png"} <= set(move_images["move-4-5"])
assert move_images["abs-crunch"] == ["assets/kneeling-cable-crunch.png"]
assert move_images["abs-pallof"] == ["assets/pallof-press.png"]
assert "#abs" in pages["workout-plan.html"].links
workout = (ROOT / "workout-plan.html").read_text()
for day, move in ((2, "abs-crunch"), (4, "abs-pallof")):
    row = re.search(rf'<tr data-abs-day="{day}" data-base-sets="(\d+)" data-total-sets="(\d+)">', workout)
    article = re.search(rf'<article class="mv" id="{move}".*?</article>', workout, re.S).group()
    extra = int(re.search(r'<span class="sets">(\d+)', article).group(1))
    assert extra == 2 and tuple(map(int, row.groups())) == (14, 14 + extra), (day, "core volume differs")
for filename in images:
    data = (ROOT / filename).read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", data[16:24]) == (1536, 1024), filename
assert (ROOT / ".nojekyll").is_file()
assert "<script" not in (ROOT / "index.html").read_text(), "Homepage does not need JavaScript"
print("PASS: 3 pages, 38 illustrations, all 24 main slots illustrated, 2 optional core guides and their volume, links, anchors and Pages entry.")
