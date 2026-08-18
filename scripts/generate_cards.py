"""오늘의 AI 뉴스를 네이버 블로그용 카드뉴스 이미지로 생성한다.

data/ai-articles.json 을 읽어 상위 기사들을 카드 이미지(PNG)로 렌더링하고,
블로그에 바로 붙여넣을 수 있는 제목/본문 초안(blog-post.md)을 함께 만든다.
실제 네이버 블로그 게시는 공식 API가 없어 자동화하지 않으며, 생성된 이미지와
글 초안을 사람이 직접 업로드하는 것을 전제로 한다.
"""
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

CARDS_LIMIT = 7
CARD_WIDTH = 1000
CARD_HEIGHT = 1250

# 헤드라인에서 강조색으로 표시할 키워드 (먼저 매칭되는 것 하나만 강조)
HIGHLIGHT_KEYWORDS = [
    "ChatGPT", "GPT", "Claude", "Gemini", "오픈AI", "OpenAI", "구글", "메타",
    "삼성", "LG", "네이버", "카카오", "엔비디아", "테슬라", "애플", "SpaceX",
    "인공지능", "생성형AI", "AI",
]

KST = timezone(timedelta(hours=9))
ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "ai-articles.json"
TPL_DIR = ROOT / "templates"


def load_today_articles():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE} 없음. generate_articles.py를 먼저 실행하세요.")
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return data.get("articles", [])[:CARDS_LIMIT]


def highlight(title: str) -> str:
    for kw in HIGHLIGHT_KEYWORDS:
        idx = title.find(kw)
        if idx != -1:
            before, after = title[:idx], title[idx + len(kw):]
            return f"{before}<span class=\"hl\">{kw}</span>{after}"
    return title


def headline_font_size(title: str) -> int:
    length = len(title)
    if length <= 22:
        return 68
    if length <= 34:
        return 58
    if length <= 48:
        return 48
    return 40


def shorten(text: str, limit: int = 70) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return (text[: limit - 1] + "…") if len(text) > limit else text


def render_cards(articles, today_iso: str, today_kr: str, out_dir: Path):
    env = Environment(loader=FileSystemLoader(str(TPL_DIR)), autoescape=False)
    template = env.get_template("card.html.j2")
    out_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CARD_WIDTH, "height": CARD_HEIGHT})
        for i, art in enumerate(articles, start=1):
            title = art.get("title", "").strip()
            html = template.render(
                rank=i,
                headline=highlight(title),
                headline_size=headline_font_size(title),
                desc=shorten(art.get("summary", "")),
                date_kr=today_kr,
            )
            page.set_content(html, wait_until="load")
            out_path = out_dir / f"card-{i}.png"
            page.screenshot(path=str(out_path))
            paths.append(out_path)
        browser.close()
    return paths


def write_blog_draft(articles, today_iso: str, today_kr: str, out_dir: Path):
    n = len(articles)
    title = f"오늘의 AI 뉴스 {n}가지 ({today_kr})"
    lines = [f"# {title}", ""]
    for i, art in enumerate(articles, start=1):
        headline = art.get("title", "").strip()
        summary = shorten(art.get("summary", ""), 120)
        link = art.get("link", "")
        lines.append(f"## {i}. {headline}")
        if summary:
            lines.append(summary)
        if link:
            lines.append(f"원문: {link}")
        lines.append("")
    lines.append("#AI뉴스 #인공지능 #오늘의AI소식 #코아랩")
    draft_path = out_dir / "blog-post.md"
    draft_path.write_text("\n".join(lines), encoding="utf-8")
    return draft_path


def main():
    now = datetime.now(KST)
    today_iso = now.date().isoformat()
    today_kr = now.strftime("%Y.%m.%d")

    articles = load_today_articles()
    if not articles:
        print("오늘 생성된 기사가 없습니다. 종료.")
        return

    out_dir = ROOT / "cards" / today_iso
    card_paths = render_cards(articles, today_iso, today_kr, out_dir)
    draft_path = write_blog_draft(articles, today_iso, today_kr, out_dir)

    print(f"완료: 카드 {len(card_paths)}장 생성 -> {out_dir}")
    print(f"블로그 초안: {draft_path}")


if __name__ == "__main__":
    main()
