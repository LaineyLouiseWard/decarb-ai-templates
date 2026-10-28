"""Make poster.pdf (A0, ready to print) and poster.png (a preview), and stop if anything spills off the page.

    pip install -r requirements.txt
    playwright install chromium     # skip this if Google Chrome is already installed
    python render.py                # writes poster.pdf and poster.png next to poster.html
    python render.py --check        # only looks for problems; writes nothing

You don't need this to print: opening poster.html in Chrome and choosing Print → Save as PDF gives the same PDF.
"""
import argparse
import sys
from pathlib import Path

from playwright.sync_api import Error, sync_playwright

HERE = Path(__file__).resolve().parent

PROBLEMS_JS = """() => {
  const poster = document.querySelector('.poster');
  const bottom = poster.getBoundingClientRect().bottom - parseFloat(getComputedStyle(poster).paddingBottom);
  const problems = [];
  for (const card of document.querySelectorAll('.card')) {
    const name = card.querySelector('h2')?.innerText.trim();
    const pastPage = card.getBoundingClientRect().bottom - bottom;
    const pastCard = card.scrollHeight - card.clientHeight;
    if (pastPage > 1) problems.push(`"${name}" runs ${Math.round(pastPage / 0.75)} mm past the bottom of the page`);
    else if (pastCard > 1) problems.push(`"${name}" has ${Math.round(pastCard / 0.75)} mm more content than fits in its box`);
  }
  for (const img of document.images) {
    if (!img.complete || img.naturalWidth === 0) problems.push(`image not found: ${img.getAttribute('src')}`);
  }
  return problems;
}"""


def open_browser(p):
    try:
        return p.chromium.launch()
    except Error:
        return p.chromium.launch(channel="chrome")  # use the installed Google Chrome instead


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="look for problems only")
    parser.add_argument("html", nargs="?", default=str(HERE / "poster.html"))
    args = parser.parse_args()
    html = Path(args.html).resolve()

    with sync_playwright() as p:
        browser = open_browser(p)
        page = browser.new_page(viewport={"width": 700, "height": 950}, device_scale_factor=2)
        page.goto(html.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        problems = page.evaluate(PROBLEMS_JS)
        if not args.check:
            page.locator(".poster").screenshot(path=html.with_suffix(".png"))
            page.pdf(path=html.with_suffix(".pdf"), prefer_css_page_size=True, print_background=True)
            print(f"wrote {html.with_suffix('.pdf').name} and {html.with_suffix('.png').name}")
        browser.close()

    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
