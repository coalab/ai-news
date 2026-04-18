import os, re, requests, uuid
from datetime import datetime, timezone, timedelta
from html import unescape

NAVER_CLIENT_ID      = os.environ['NAVER_CLIENT_ID']
NAVER_CLIENT_SECRET  = os.environ['NAVER_CLIENT_SECRET']
UNSPLASH_ACCESS_KEY  = os.environ.get('UNSPLASH_ACCESS_KEY', '')
SUPABASE_URL         = 'https://onfddgmyzkeaxidpdwra.supabase.co'
SUPABASE_KEY         = os.environ['SUPABASE_SERVICE_KEY']

KST   = timezone(timedelta(hours=9))
today = datetime.now(KST)

TAG_RE = re.compile(r'<[^>]+>')

def clean(text):
    return unescape(TAG_RE.sub('', text or '')).strip()

def fetch_top_news(query='AI 인공지능 기술', display=5):
    url = 'https://openapi.naver.com/v1/search/news.json'
    hdrs = {
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
    }
    params = {'query': query, 'display': display, 'sort': 'date'}
    r = requests.get(url, headers=hdrs, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get('items', [])

def fetch_unsplash_image(keyword: str) -> str:
    if UNSPLASH_ACCESS_KEY:
        try:
            r = requests.get(
                'https://api.unsplash.com/photos/random',
                params={'query': keyword, 'orientation': 'landscape', 'client_id': UNSPLASH_ACCESS_KEY},
                timeout=10,
            )
            if r.status_code == 200:
                return r.json()['urls']['regular']
        except Exception as e:
            print(f'Unsplash 오류: {e}')
    return f"https://source.unsplash.com/800x450/?{keyword.replace(' ', ',')}"

def build_content(items, link, domain, date_str):
    """여러 기사 요약을 엮어 풍부한 본문 HTML을 생성합니다."""
    paragraphs = []
    for item in items:
        desc = clean(item.get('description', ''))
        if desc:
            paragraphs.append(f'<p>{desc}</p>')

    related_links = ''
    if len(items) > 1:
        related_items = ''.join(
            f'<li><a href="{it.get("originallink") or it.get("link","")}" target="_blank" rel="noopener">'
            f'{clean(it.get("title",""))}</a></li>'
            for it in items[1:]
        )
        related_links = f'<h3>관련 기사</h3><ul>{related_items}</ul>'

    body = '\n'.join(paragraphs)
    return (
        f'{body}\n'
        f'<p>더 자세한 내용은 <a href="{link}" target="_blank" rel="noopener">원문 기사</a>에서 확인하세요.</p>\n'
        f'{related_links}\n'
        f'<hr><p><small>출처: {domain} | {date_str}</small></p>'
    )

# 메인 로직
items = fetch_top_news(display=5)
if not items:
    print('기사 없음')
    exit(0)

item   = items[0]
title  = clean(item.get('title', ''))
desc   = clean(item.get('description', ''))
link   = item.get('originallink') or item.get('link', '')
domain = link.split('/')[2] if link.startswith('http') else 'news.naver.com'
date_str = today.strftime('%Y년 %m월 %d일')

content = build_content(items, link, domain, date_str)

image_url = fetch_unsplash_image('artificial intelligence technology')

slug = f'ai-news-{today.strftime("%Y%m%d")}-{str(uuid.uuid4())[:8]}'

article = {
    'title':         title,
    'content':       content,
    'summary':       desc,
    'author':        'COALAB AI뉴스',
    'category':      'AI',
    'thumbnail_url': image_url,
    'slug':          slug,
    'published':     True,
}

post_to_supabase = lambda a: requests.post(
    f'{SUPABASE_URL}/rest/v1/articles',
    headers={
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    },
    json=a,
    timeout=10,
).raise_for_status()

post_to_supabase(article)
print(f'완료: {title[:50]}')
print(f'이미지: {image_url[:60]}')
