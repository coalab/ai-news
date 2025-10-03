from datetime import datetime, timezone, timedelta
from pathlib import Path
import feedparser

# 한국 시간대(KST) 적용
KST = timezone(timedelta(hours=9))
today = datetime.now(KST).date()
iso = today.isoformat()

# 프로젝트 루트와 아카이브 경로 설정
root = Path(__file__).resolve().parent.parent
archive_dir = root / "archive" / iso
archive_dir.mkdir(parents=True, exist_ok=True)

# -------- RSS 가져오기 --------
# Google 뉴스에서 "AI" 키워드 한국어 검색
feed = feedparser.parse("https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko")

cards_html = ""
for i, entry in enumerate(feed.entries[:10], start=1):  # 상위 10개 기사만
    title = entry.title
    summary = getattr(entry, "summary", "")[:200]  # 요약(최대 200자)
    link = entry.link

    cards_html += f"""
    <article class="card">
      <h3>{title}</h3>
      <p>{summary}</p>
      <div><a href="{link}" target="_blank">기사 보기</a></div>
    </article>
    """

# -------- HTML 생성 --------
html = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>AI 뉴스 카드뉴스 | {iso}</title>
  <meta name="description" content="오늘의 AI 뉴스 TOP 10을 카드뉴스 형태로 한눈에 정리합니다.">
  <style>
    body {{ font-family: system-ui, sans-serif; background:#f5f6fa; margin:0; }}
    header {{ padding:20px; background:#eef2ff; border-bottom:1px solid #ccc; }}
    h1 {{ margin:0; font-size:28px; }}
    .subtitle {{ color:#555; margin-top:6px; }}
    main {{ max-width:1000px; margin:20px auto; padding:10px;
           display:grid; gap:16px; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); }}
    .card {{ background:#fff; padding:16px; border-radius:12px;
             box-shadow:0 2px 8px rgba(0,0,0,0.1); }}
    .card h3 {{ margin:6px 0; font-size:18px; }}
    .card p {{ font-size:14px; color:#444; }}
    footer {{ text-align:center; color:#777; padding:20px; margin-top:30px; font-size:13px; }}
    a {{ color:#3057ff; text-decoration:none; }}
  </style>
</head>
<body>
<header>
  <h1>AI 뉴스 카드뉴스</h1>
  <p class="subtitle">오늘의 AI 이슈를 카드뉴스처럼 한 번에 훑어보기</p>
  <p><a href="/ai-news/archive/{iso}/">오늘 아카이브 바로가기</a></p>
</header>

<main>
  {cards_html}
</main>

<footer>© Daily AI News · {iso}</footer>
</body>
</html>"""

# -------- HTML 파일 저장 --------
(root / "index.html").write_text(html, encoding="utf-8")
(archive_dir / "index.html").write_text(html, encoding="utf-8")

print("✅ index.html 및 archive 페이지가 성공적으로 생성되었습니다.")
