import os, json, time, requests, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from html import unescape

NAVER_CLIENT_ID     = os.environ["NAVER_CLIENT_ID"]
NAVER_CLIENT_SECRET = os.environ["NAVER_CLIENT_SECRET"]

KST      = timezone(timedelta(hours=9))
today    = datetime.now(KST).date().isoformat()
ROOT     = Path(__file__).resolve().parents[1]
OUT_FILE = ROOT / "data" / "ai-articles.json"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

QUERIES = ["AI 인공지능", "AI 기술", "생성형AI", "AI 산업", "AI 교육"]

TAG_RE = re.compile(r"<[^>]+>")

def clean(text):
    return unescape(TAG_RE.sub("", text)).strip()

def fetch_news(query):
    url = "https://openapi.naver.com/v1/search/news.json"
    hdrs = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    params = {"query": query, "display": 1, "sort": "date"}
    r = requests.get(url, headers=hdrs, params=params, timeout=10)
    r.raise_for_status()
    items = r.json().get("items", [])
    return items[0] if items else None

articles = []
for i, query in enumerate(QUERIES):
    item = fetch_news(query)
    if not item:
        continue
    title   = clean(item.get("title", ""))
    summary = clean(item.get("description", ""))
    link    = item.get("originallink") or item.get("link", "")
    articles.append({
        "id":      f"naver-{int(time.time()*1000)}-{i}",
        "title":   title,
        "summary": summary,
        "body":    summary,
        "image":   "https://www.google.com/s2/favicons?domain=news.naver.com&sz=128",
        "topic":   query,
        "date":    today,
        "source":  "Naver 뉴스",
        "link":    link,
    })
    time.sleep(0.3)

result = {"updated": datetime.now(KST).isoformat(), "articles": articles}
OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"완료: {len(articles)}개 기사 생성")
