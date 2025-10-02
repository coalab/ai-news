import os, yaml, feedparser, html, pathlib
from datetime import datetime
from dateutil import tz
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
ARCHIVE = ROOT / "archive"
FEEDS_YAML = ROOT / "feeds.yaml"

cfg = yaml.safe_load(open(FEEDS_YAML, "r", encoding="utf-8"))
KST = tz.gettz(cfg.get("timezone", "Asia/Seoul"))
MAX_PER_FEED = int(cfg.get("max_items_per_feed", 5))

def shorten(text, n=220):
    t = " ".join(text.split())
    return (t[:n] + "…") if len(t) > n else t

items = []
for f in cfg["feeds"]:
    d = feedparser.parse(f["url"])
    for e in d.entries[:MAX_PER_FEED]:
        title = html.unescape(getattr(e, "title", "")).strip()
        link = getattr(e, "link", "")
        summary = html.unescape(getattr(e, "summary", getattr(e, "description", ""))).strip() or title
        dt = None
        for key in ("published_parsed","updated_parsed"):
            if hasattr(e, key) and getattr(e, key):
                dt = datetime(*getattr(e, key)[:6])
                break
        if not dt:
            dt = datetime.utcnow()
        dt = dt.replace(tzinfo=tz.tzutc()).astimezone(KST)

        items.append({
            "source": f["name"],
            "title": title,
            "summary": shorten(summary),
            "link": link,
            "dt": dt,
            "date_kr": dt.strftime("%Y-%m-%d"),
        })

items.sort(key=lambda x: x["dt"], reverse=True)
cards = items[:10]

env = Environment(loader=FileSystemLoader(str(TEMPLATES)),
                  autoescape=select_autoescape())
tmpl = env.get_template("page.html.j2")

today = datetime.now(tz=KST)
today_iso = today.strftime("%Y-%m-%d")
week_str = today.strftime("%Y년 %m월 %d일 (주)")
html_out = tmpl.render(
    today_kr=today.strftime("%Y년 %m월 %d일"),
    today_iso=today_iso,
    week_str=week_str,
    year=today.year,
    cards=cards
)

dst_dir = ARCHIVE / today_iso
dst_dir.mkdir(parents=True, exist_ok=True)
(dst_dir / "index.html").write_text(html_out, encoding="utf-8")
(ROOT / "index.html").write_text(html_out, encoding="utf-8")

print(f"Generated {len(cards)} cards → index.html and archive/{today_iso}/index.html")
