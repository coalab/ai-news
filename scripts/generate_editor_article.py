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
    # picsum.photos: 무료, 안정적인 플레이스홀더 이미지
    import random
    seed = random.randint(1, 1000)
    return f"https://picsum.photos/seed/{seed}/800/450"

def build_content(items, link, domain, date_str):
    """메인 기사 1개 + 관련 뉴스 브리핑 형식으로 본문 HTML 생성."""
    main = items[0]
    main_desc = clean(main.get('description', ''))

    # 관련 뉴스 브리핑 (나머지 기사)
    brief_rows = ''
    for it in items[1:]:
        t = clean(it.get('title', ''))
        d = clean(it.get('description', ''))
        href = it.get('originallink') or it.get('link', '')
        brief_rows += (
            f'<li style="margin-bottom:12px">'
            f'<strong><a href="{href}" target="_blank" rel="noopener" style="color:#1a56db">{t}</a></strong>'
            f'<br><span style="color:#555;font-size:14px">{d}</span>'
            f'</li>'
        )

    related_section = ''
    if brief_rows:
        related_section = (
            f'<hr style="margin:24px 0">'
            f'<h3 style="margin-bottom:16px">📰 오늘의 AI 뉴스 브리핑</h3>'
            f'<ul style="list-style:none;padding:0">{brief_rows}</ul>'
        )

    return (
        f'<p style="font-size:16px;line-height:1.8">{main_desc}</p>'
        f'<p><a href="{link}" target="_blank" rel="noopener">▶ 원문 기사 보기</a></p>'
        f'{related_section}'
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
