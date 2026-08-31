"""Validate the static showcase without network access or third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.errors = []
        self.h1 = 0
        self.title = False
        self.description = False
        self.viewport = False
        self.lang = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                self.errors.append("Duplicate id: " + a["id"])
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = bool(a.get("lang"))
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.title = True
        if tag == "meta":
            self.description |= a.get("name") == "description" and bool(a.get("content"))
            self.viewport |= a.get("name") == "viewport"
        if tag == "img" and "alt" not in a:
            self.errors.append("Image missing alt text")
        for key in ("href", "src"):
            if key in a:
                self.references.append(a[key])


def main():
    page = Page()
    page.feed((DOCS / "index.html").read_text(encoding="utf-8"))
    errors = page.errors
    for ok, name in [(page.h1 == 1, "exactly one h1"), (page.title, "title"),
                     (page.description, "description"), (page.viewport, "viewport"),
                     (page.lang, "document language")]:
        if not ok:
            errors.append("Missing or invalid " + name)
    for ref in page.references:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            if url.scheme and url.scheme not in {"https", "http", "mailto", "tel"}:
                errors.append("Unexpected URL scheme: " + ref)
            continue
        if not url.path:
            if url.fragment and unquote(url.fragment) not in page.ids:
                errors.append("Broken anchor: " + ref)
            continue
        target = (DOCS / unquote(url.path)).resolve()
        if not target.is_relative_to(DOCS.resolve()):
            errors.append("Asset escapes docs directory: " + ref)
        elif not target.exists():
            errors.append("Missing local asset: " + ref)
    for svg in DOCS.rglob("*.svg"):
        ET.parse(svg)
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: page structure, local links, image alt attributes and SVG syntax")
    print("Scope: static checks only; backend and visual behavior are not tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
