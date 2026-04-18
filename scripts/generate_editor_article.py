import os, re, requests, uuid
from datetime import datetime, timezone, timedelta
from html import unescape

NAVER_CLIENT_ID     = os.environ['NAVER_CLIENT_ID']
NAVER_CLIENT_SECRET = os.environ['NAVER_CLIENT_SECRET']
SUPABASE_URL        = 'https://onfddgmyzkeaxidpdwra.supabase.co'
SUPABASE_KEY        = os.environ['SUPABASE_SERVICE_KEY']

KST   = timezone(timedelta(hours=9))
today = datetime.now(KST)

TAG_RE = re.compile(r'<[^>]+>')

def clean(text):
    return unescape(TAG_RE.sub('', text or '')).strip()

def fetch_top_news():
    url = 'https://openapi.naver.com/v1/search/news.json'
    hdrs = {
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
    }
    params = {'query': 'AI 인공지능 기술', 'display': 5, 'sort': 'date'}
    r = requests.get(url, headers=hdrs, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get('items', [])

def post_to_supabase(article):
    url = f'{SUPABASE_URL}/rest/v1/articles'
    hdrs = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    r = requests.post(url, headers=hdrs, json=article, timeout=10)
    r.raise_for_status()

items = fetch_top_news()
if not items:
    print('기사 없음')
    exit(0)

item   = items[0]
title  = clean(item.get('title', ''))
desc   = clean(item.get('description', ''))
link   = item.get('originallink') or item.get('link', '')
domain = link.split('/')[2] if link.startswith('http') else 'news.naver.com'
date_str = today.strftime('%Y년 %m월 %d일')

content = (
    f'<p>{desc}</p>'
    f'<p>더 자세한 내용은 <a href="{link}" target="_blank" rel="noopener">원문 기사</a>에서 확인하세요.</p>'
    f'<hr><p><small>출처: {domain} | {date_str}</small></p>'
)

slug = f'ai-news-{today.strftime("%Y%m%d")}-{str(uuid.uuid4())[:8]}'

article = {
    'title':         title,
    'content':       content,
    'summary':       desc,
    'author':        'COALAB AI뉴스',
    'category':      'AI',
    'thumbnail_url': f'https://www.google.com/s2/favicons?domain={domain}&sz=128',
    'slug':          slug,
    'published':     True,
}

post_to_supabase(article)
print(f'완료: {title[:50]}')
