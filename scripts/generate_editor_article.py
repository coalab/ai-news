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
today_slug_prefix = f'ai-news-{today.strftime("%Y%m%d")}'

TAG_RE = re.compile(r'<[^>]+>')

AI_KEYWORDS = [
    'AI', '인공지능', '머신러닝', '딥러닝', 'GPT', 'LLM', '챗봇',
    '생성형', '자율주행', '로봇', '빅데이터', '알고리즘', '신경망',
    'ChatGPT', 'Claude', 'Gemini', '오픈AI', 'OpenAI', '구글AI',
]

QUERIES = [
    'AI 인공지능 최신 뉴스',
    'GPT 인공지능 기술',
    '생성형 AI 서비스',
    '인공지능 산업 동향',
]

def clean(text):
    return unescape(TAG_RE.sub('', text or '')).strip()

def is_ai_article(title, desc):
    text = (title + ' ' + desc).upper()
    return any(kw.upper() in text for kw in AI_KEYWORDS)

def fetch_top_news(query, display=10):
    url = 'https://openapi.naver.com/v1/search/news.json'
    hdrs = {
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
    }
    params = {'query': query, 'display': display, 'sort': 'date'}
    r = requests.get(url, headers=hdrs, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get('items', [])

def fetch_ai_articles():
    """여러 쿼리로 시도해 AI 관련 기사 5개 반환."""
    for query in QUERIES:
        items = fetch_top_news(query, display=10)
        ai_items = [
            it for it in items
            if is_ai_article(clean(it.get('title', '')), clean(it.get('description', '')))
        ]
        if len(ai_items) >= 3:
            print(f'쿼리 "{query}"로 AI 기사 {len(ai_items)}개 발견')
            return ai_items[:5]
    print('경고: AI 기사 필터 통과 미달, 첫 번째 쿼리 결과 사용')
    return fetch_top_news(QUERIES[0], display=5)

def today_article_exists():
    """오늘 이미 기사가 생성됐는지 확인."""
    r = requests.get(
        f'{SUPABASE_URL}/rest/v1/articles',
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
        },
        params={
            'slug': f'like.{today_slug_prefix}%',
            'select': 'id',
            'limit': '1',
        },
        timeout=10,
    )
    return len(r.json()) > 0

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
    import random
    seed = random.randint(1, 1000)
    return f"https://picsum.photos/seed/{seed}/800/450"

def build_content(items, link, domain, date_str):
    main = items[0]
    main_desc = clean(main.get('description', ''))

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
            f'<h3 style="margin-bottom:16px">오늘의 AI 뉴스 브리핑</h3>'
            f'<ul style="list-style:none;padding:0">{brief_rows}</ul>'
        )

    return (
        f'<p style="font-size:16px;line-height:1.8">{main_desc}</p>'
        f'<p><a href="{link}" target="_blank" rel="noopener">원문 기사 보기</a></p>'
        f'{related_section}'
        f'<hr><p><small>출처: {domain} | {date_str}</small></p>'
    )

# 메인 로직
if today_article_exists():
    print(f'오늘({today.strftime("%Y-%m-%d")}) 기사 이미 존재. 종료.')
    exit(0)

items = fetch_ai_articles()
if not items:
    print('기사 없음')
    exit(1)

item     = items[0]
title    = clean(item.get('title', ''))
desc     = clean(item.get('description', ''))
link     = item.get('originallink') or item.get('link', '')
domain   = link.split('/')[2] if link.startswith('http') else 'news.naver.com'
date_str = today.strftime('%Y년 %m월 %d일')

content   = build_content(items, link, domain, date_str)
image_url = fetch_unsplash_image('artificial intelligence technology')
slug      = f'{today_slug_prefix}-{str(uuid.uuid4())[:8]}'

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

r = requests.post(
    f'{SUPABASE_URL}/rest/v1/articles',
    headers={
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    },
    json=article,
    timeout=10,
)
r.raise_for_status()
print(f'완료: {title[:60]}')
print(f'슬러그: {slug}')
print(f'이미지: {image_url[:60]}')
