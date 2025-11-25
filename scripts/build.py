# from datetime import datetime, timezone, timedelta
# from pathlib import Path
# import feedparser

# # 한국 시간대(KST) 적용
# KST = timezone(timedelta(hours=9))
# today = datetime.now(KST).date()
# iso = today.isoformat()

# # 프로젝트 루트와 아카이브 경로 설정
# root = Path(__file__).resolve().parent.parent
# archive_dir = root / "archive" / iso
# archive_dir.mkdir(parents=True, exist_ok=True)

# # -------- RSS 가져오기 --------
# # Google 뉴스에서 "AI" 키워드 한국어 검색
# feed = feedparser.parse("https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko")

# cards_html = ""
# for i, entry in enumerate(feed.entries[:10], start=1):  # 상위 10개 기사만
#     title = entry.title
#     summary = getattr(entry, "summary", "")[:200]  # 요약(최대 200자)
#     link = entry.link
#     published = getattr(entry, "published", "")  # 발행일 (있을 경우 표시)

#     cards_html += f"""
#     <article class="card">
#       <h3>{title}</h3>
#       <p>{summary}</p>
#       <p class="meta">발행일: {published}</p>
#       <div><a href="{link}" target="_blank">기사 보기</a></div>
#     </article>
#     """

# # -------- HTML 생성 --------
# html = f"""<!doctype html>
# <html lang="ko">
# <head>
#   <meta charset="utf-8">
#   <meta name="viewport" content="width=device-width,initial-scale=1">
#   <title>AI 뉴스 카드뉴스 | {iso}</title>
#   <meta name="description" content="오늘의 AI 뉴스 TOP 10을 카드뉴스 형태로 한눈에 정리합니다.">
#   <style>
#     body {{ font-family: system-ui, sans-serif; background:#f5f6fa; margin:0; }}
#     header {{ padding:20px; background:#eef2ff; border-bottom:1px solid #ccc; }}
#     h1 {{ margin:0; font-size:28px; }}
#     .subtitle {{ color:#555; margin-top:6px; }}
#     main {{ max-width:1000px; margin:20px auto; padding:10px;
#            display:grid; gap:16px; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); }}
#     .card {{ background:#fff; padding:16px; border-radius:12px;
#              box-shadow:0 2px 8px rgba(0,0,0,0.1); }}
#     .card h3 {{ margin:6px 0; font-size:18px; }}
#     .card p {{ font-size:14px; color:#444; }}
#     .card .meta {{ font-size:12px; color:#777; margin-top:8px; }}
#     footer {{ text-align:center; color:#777; padding:20px; margin-top:30px; font-size:13px; line-height:1.6; }}
#     a {{ color:#3057ff; text-decoration:none; }}
#   </style>
# </head>
# <body>
# <header>
#   <h1>AI 뉴스 카드뉴스</h1>
#   <p class="subtitle">오늘의 AI 이슈를 카드뉴스처럼 한 번에 훑어보기</p>
#   <p><a href="/ai-news/archive/{iso}/">오늘 아카이브 바로가기</a></p>
# </header>

# <main>
#   {cards_html}
# </main>

# <footer>
#   <p>© Daily AI News · {iso}</p>
#   <p>
#     본 서비스는 언론사에서 공개한 RSS 피드를 기반으로 기사 <strong>제목·요약·원문 링크</strong>만 제공합니다.<br>
#     모든 기사의 저작권은 원 저작권자(언론사 및 기자)에 있으며, 원문 열람은 해당 언론사 웹사이트에서 가능합니다.<br>
#     교육·연구 목적으로 일부 인용할 경우 반드시 <strong>언론사명·발행일·기자명·URL</strong>을 명시해 주시기 바랍니다.
#   </p>
# </footer>
# </body>
# </html>"""

# # -------- HTML 파일 저장 --------
# (root / "index.html").write_text(html, encoding="utf-8")
# (archive_dir / "index.html").write_text(html, encoding="utf-8")
from urllib.parse import urlparse

# print("✅ index.html 및 archive 페이지가 성공적으로 생성되었습니다.")
from urllib.parse import urlparse
# ... (기존 import 밑에 이어서)

# ===== RSS 수집 =====
# feed = feedparser.parse(FEED_URL)
# cards = []
# for entry in feed.entries[:CARDS_LIMIT]:
#     title = (entry.get("title") or "").strip()
#     link  = entry.get("link")
#     if not (title and link):
#         continue

#     summary   = clean_summary(entry.get("summary") or "")
#     published = entry.get("published", "")
#     source    = (getattr(entry, "source", {}) or {}).get("title") if hasattr(entry, "source") else None
#     source    = source or "Google 뉴스"

#     # ---- 썸네일 추출 (없으면 파비콘 폴백) ----
#     thumb = None
#     # 1) media:thumbnail
#     if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
#         thumb = entry.media_thumbnail[0].get("url")
#     # 2) media:content
#     if not thumb and hasattr(entry, "media_content") and entry.media_content:
#         thumb = entry.media_content[0].get("url")
#     # 3) 파비콘 폴백 (도메인 기반)
#     host = urlparse(link).netloc
#     favicon = f"https://www.google.com/s2/favicons?domain={host}&sz=128"
#     thumb = thumb or favicon

#     cards.append({
#         "title": title,
#         "summary": summary,
#         "link": link,
#         "date_kr": published,
#         "source": source,
#         "thumb": thumb,            # ✅ 추가
#     })

from datetime import datetime, timezone, timedelta
from pathlib import Path
import re
from html import unescape
import feedparser
from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlparse, parse_qs

# ===== 설정 =====
SITE_URL        = "https://coalab.github.io/ai-news"
CARDS_LIMIT     = 10
AD_INTERVAL     = 3
ADS_CLIENT      = "ca-pub-1841750816553239"  # 본인 Google AdSense Client ID
ADS_SLOT_TOP    = "1234567890"               # 상단 광고 슬롯 ID
ADS_SLOT_MID    = "1234567890"               # 중간 광고 슬롯 ID
FEED_URL        = "https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko"

# ===== HTML 정리 함수 =====
TAG_RE = re.compile(r"<[^>]+>")
def clean_summary(html_text: str, limit: int = 180) -> str:
    if not html_text:
        return ""
    text = TAG_RE.sub("", html_text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:limit] + "…") if len(text) > limit else text

# ===== 날짜/경로 =====
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
today_iso = now.date().isoformat()
today_kr  = now.strftime("%Y.%m.%d (%a)")
week_str  = now.strftime("Week %W")
year      = now.year

ROOT    = Path(__file__).resolve().parents[1]
TPL_DIR = ROOT / "templates"
OUT_DIR = ROOT
ARCHIVE = ROOT / "archive" / today_iso
ARCHIVE.mkdir(parents=True, exist_ok=True)

# ===== 템플릿 로드 =====
tpl_candidates = ["index.html", "page.html.j2", "index.j2", "index.htm"]
tpl_name = next((n for n in tpl_candidates if (TPL_DIR / n).exists()), None)
if not tpl_name:
    raise FileNotFoundError(
        f"템플릿 파일을 찾지 못했습니다. templates 폴더에 다음 중 하나를 만들어주세요: {', '.join(tpl_candidates)}"
    )

env = Environment(loader=FileSystemLoader(str(TPL_DIR)), autoescape=True)
template = env.get_template(tpl_name)

# ===== 유틸: Google News 링크 → 원문 링크 복원 =====
def resolve_original_link(gn_link: str) -> str:
    """
    news.google.com 중계 링크의 쿼리파라미터 ?url= 에 실제 원문 주소가 들어있으면 그걸 반환.
    그렇지 않으면 원본 링크를 그대로 반환.
    """
    try:
        p = urlparse(gn_link or "")
        if p.netloc.endswith("news.google.com"):
            q = parse_qs(p.query)
            return q.get("url", [gn_link])[0]
        return gn_link
    except Exception:
        return gn_link

def pick_source(entry) -> str:
    """
    RSS의 source.title 또는 링크 도메인을 이용해 소스를 추정.
    """
    src = None
    try:
        if hasattr(entry, "source") and isinstance(entry.source, dict):
            src = entry.source.get("title")
    except Exception:
        pass

    if src:
        return src

    # source가 비어 있으면 링크 도메인을 소스처럼 표기
    gn_link = entry.get("link", "")
    link = resolve_original_link(gn_link)
    host = urlparse(link).netloc or "Google 뉴스"
    return host

def parse_published(entry) -> str:
    """
    published(문자열)가 있으면 그대로 쓰되, 비면 공백 반환.
    추후 필요하면 datetime 파싱해 KST 포맷으로 바꿀 수 있음.
    """
    return entry.get("published", "") or ""

def pick_thumbnail(entry, cache_key: str) -> str:
    """
    1) media:thumbnail
    2) media:content
    3) 원문 도메인 파비콘
    순서로 선택. 캐시버스터를 붙여 새로고침 영향 최소화.
    """
    # 1) media:thumbnail
    try:
        if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
            u = entry.media_thumbnail[0].get("url")
            if u:
                return f"{u}?v={cache_key}"
    except Exception:
        pass

    # 2) media:content
    try:
        if hasattr(entry, "media_content") and entry.media_content:
            u = entry.media_content[0].get("url")
            if u:
                return f"{u}?v={cache_key}"
    except Exception:
        pass

    # 3) favicon (원문 도메인 기준)
    gn_link = entry.get("link", "")
    link = resolve_original_link(gn_link)
    host = urlparse(link).netloc or "news.google.com"
    return f"https://www.google.com/s2/favicons?domain={host}&sz=128&v={cache_key}"

# ===== RSS 수집 =====
feed = feedparser.parse(FEED_URL)
cards = []

for entry in feed.entries[:CARDS_LIMIT]:
    title = (entry.get("title") or "").strip()
    gn_link = entry.get("link")
    if not (title and gn_link):
        continue

    link      = resolve_original_link(gn_link)
    summary   = clean_summary(entry.get("summary") or "")
    published = parse_published(entry)
    source    = pick_source(entry)
    thumb     = pick_thumbnail(entry, cache_key=today_iso)

    cards.append({
        "title": title,
        "summary": summary,
        "link": link,          # 원문 링크
        "date_kr": published,  # 필요 시 포맷 변경 가능
        "source": source,
        "thumb": thumb,        # 카드별 썸네일
    })

# ===== 렌더링 =====
html = template.render(
    today_iso=today_iso,
    today_kr=today_kr,
    week_str=week_str,
    year=year,
    cards=cards,
    site_url=SITE_URL,
    ad_client=ADS_CLIENT,
    ad_slot_top=ADS_SLOT_TOP,
    ad_slot_mid=ADS_SLOT_MID,
    ad_interval=AD_INTERVAL,
)

# ===== 저장 =====
(OUT_DIR / "index.html").write_text(html, encoding="utf-8")
(ARCHIVE / "index.html").write_text(html, encoding="utf-8")

print("✅ index.html 및 COALAB archive 페이지 생성 완료:", today_iso)

