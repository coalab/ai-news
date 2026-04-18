# ai-news 수익화 & SEO 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ai-news.coalab.co.kr에 SEO, 애드센스 준비, coalab 강의 CTA를 추가해 트래픽 회복과 수익화 기반을 구축한다.

**Architecture:** 정적 GitHub Pages 사이트. index.html(현재 날짜 페이지)과 templates/page.html.j2(자동 빌드 템플릿) 두 곳을 동일하게 수정해야 매일 빌드 후에도 변경사항이 유지된다. sitemap.xml은 build.py에서 archive 폴더를 읽어 자동 재생성한다.

**Tech Stack:** HTML/CSS, Jinja2 템플릿, Python(sitemap 생성), GitHub Actions

---

## 파일 목록

| 파일 | 작업 |
|------|------|
| `privacy.html` | 신규 생성 — 개인정보처리방침 |
| `robots.txt` | 신규 생성 — 크롤러 허용 + sitemap 경로 |
| `scripts/build.py` | 수정 — sitemap.xml 자동 생성 추가 |
| `index.html` | 수정 — SEO 메타태그, 애드센스 준비, CTA 배너, 푸터, 네비게이션 |
| `templates/page.html.j2` | 수정 — index.html과 동일한 변경사항 (자동 빌드용) |

---

## Task 1: privacy.html 생성

**Files:**
- Create: `privacy.html`

- [ ] **Step 1: privacy.html 생성**

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>개인정보처리방침 | COALAB AI뉴스</title>
  <meta name="description" content="COALAB AI뉴스 개인정보처리방침">
  <style>
    body{margin:0;background:#f4f6f8;color:#111827;font-family:system-ui,-apple-system,"Noto Sans KR",sans-serif;line-height:1.8}
    .wrap{max-width:800px;margin:0 auto;padding:40px 24px}
    h1{font-size:26px;font-weight:800;margin-bottom:8px}
    h2{font-size:18px;font-weight:700;margin-top:36px;margin-bottom:8px;border-bottom:2px solid #e5e7eb;padding-bottom:6px}
    p,li{font-size:15px;color:#374151}
    a{color:#2d8659}
    .site-header{background:#fff;border-bottom:1px solid rgba(0,0,0,.08);padding:12px 24px}
    .site-header a{font-size:22px;font-weight:800;color:#111827;text-decoration:none}
    .site-header span{color:#2d8659}
    .site-footer{text-align:center;color:#6b7280;padding:40px 0 60px;font-size:13px;border-top:1px solid rgba(0,0,0,.08);margin-top:40px}
  </style>
</head>
<body>
<header class="site-header">
  <a href="/index.html">COALAB <span>AI뉴스</span></a>
</header>
<div class="wrap">
  <h1>개인정보처리방침</h1>
  <p>시행일: 2026년 4월 19일</p>

  <h2>1. 수집하는 개인정보 항목</h2>
  <p>본 사이트(ai-news.coalab.co.kr)는 회원가입 없이 이용 가능하며, 다음과 같은 정보를 자동으로 수집할 수 있습니다.</p>
  <ul>
    <li>방문 기록, IP 주소, 브라우저 정보, 쿠키(Google AdSense 포함)</li>
  </ul>

  <h2>2. 개인정보 수집 및 이용 목적</h2>
  <ul>
    <li>서비스 이용 통계 및 품질 개선</li>
    <li>광고 서비스 제공 (Google AdSense)</li>
  </ul>

  <h2>3. 쿠키(Cookie) 사용</h2>
  <p>본 사이트는 Google AdSense를 통한 광고 표시를 위해 쿠키를 사용합니다. Google의 광고 쿠키 사용에 관한 자세한 내용은 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google 광고 정책</a>을 참고하세요.</p>
  <p>브라우저 설정에서 쿠키를 거부할 수 있으나, 일부 서비스 이용이 제한될 수 있습니다.</p>

  <h2>4. 개인정보 보유 및 이용 기간</h2>
  <p>수집된 방문 로그는 서비스 통계 목적으로 최대 1년간 보관 후 파기합니다.</p>

  <h2>5. 제3자 제공</h2>
  <p>수집된 정보는 법령에 따른 경우를 제외하고 제3자에게 제공하지 않습니다. 다만, Google AdSense 서비스 운영을 위해 Google에 광고 관련 쿠키 데이터가 전달될 수 있습니다.</p>

  <h2>6. 이용자의 권리</h2>
  <p>이용자는 언제든지 개인정보 처리에 관한 문의를 아래 연락처로 요청할 수 있습니다.</p>

  <h2>7. 문의</h2>
  <p>개인정보 처리에 관한 문의: <a href="https://open.kakao.com/o/sZhJVf7" target="_blank" rel="noopener">카카오톡 오픈채팅</a></p>
  <p>운영사: COALAB · <a href="https://www.coalab.co.kr" target="_blank" rel="noopener">www.coalab.co.kr</a></p>
</div>
<footer class="site-footer">
  &copy; 2026 COALAB AI뉴스 &middot; <a href="/privacy.html">개인정보처리방침</a>
</footer>
</body>
</html>
```

- [ ] **Step 2: 커밋**

```bash
cd Desktop/ai-news
git add privacy.html
git commit -m "feat: 개인정보처리방침 페이지 추가 (애드센스 준비)"
```

---

## Task 2: robots.txt 생성

**Files:**
- Create: `robots.txt`

- [ ] **Step 1: robots.txt 생성**

```
User-agent: *
Allow: /

Sitemap: https://ai-news.coalab.co.kr/sitemap.xml
```

- [ ] **Step 2: 커밋**

```bash
git add robots.txt
git commit -m "feat: robots.txt 추가 (SEO)"
```

---

## Task 3: sitemap.xml 자동 생성 (build.py 수정)

**Files:**
- Modify: `scripts/build.py`
- Create: `sitemap.xml` (빌드 결과물)

- [ ] **Step 1: build.py에 sitemap 생성 함수 추가**

`scripts/build.py` 하단(또는 메인 빌드 로직 끝)에 아래 함수를 추가하고 호출한다.

```python
from pathlib import Path
from datetime import datetime, timezone, timedelta

def generate_sitemap(root: Path):
    base = "https://ai-news.coalab.co.kr"
    today = datetime.now(timezone(timedelta(hours=9))).date().isoformat()

    urls = [
        f'  <url><loc>{base}/index.html</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>',
        f'  <url><loc>{base}/about.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>',
        f'  <url><loc>{base}/archive-list.html</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>',
        f'  <url><loc>{base}/privacy.html</loc><lastmod>{today}</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>',
    ]

    archive_dir = root / "archive"
    if archive_dir.exists():
        for d in sorted(archive_dir.iterdir()):
            if d.is_dir() and (d / "index.html").exists():
                urls.append(
                    f'  <url><loc>{base}/archive/{d.name}/index.html</loc>'
                    f'<lastmod>{d.name}</lastmod>'
                    f'<changefreq>never</changefreq><priority>0.4</priority></url>'
                )

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += '\n'.join(urls)
    sitemap += '\n</urlset>\n'

    (root / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"sitemap.xml 생성 완료 ({len(urls)}개 URL)")


# 기존 build.py 메인 실행 블록 맨 끝에 호출 추가:
# root = Path(__file__).resolve().parent.parent
# generate_sitemap(root)
```

> 주의: build.py의 실제 main 실행 블록 위치를 확인하고 `generate_sitemap(root)` 호출을 끝에 추가한다. `root` 변수가 없으면 `root = Path(__file__).resolve().parent.parent`를 먼저 정의한다.

- [ ] **Step 2: 로컬에서 빌드 실행해 sitemap.xml 생성 확인**

```bash
cd Desktop/ai-news
python scripts/build.py
```

Expected: `sitemap.xml 생성 완료 (143개 URL)` 출력 및 `sitemap.xml` 파일 생성

- [ ] **Step 3: 커밋**

```bash
git add scripts/build.py sitemap.xml
git commit -m "feat: sitemap.xml 자동 생성 추가 (SEO)"
```

---

## Task 4: index.html SEO 메타태그 강화

**Files:**
- Modify: `index.html` (1~10번째 줄 `<head>` 영역)

- [ ] **Step 1: index.html head 영역 교체**

기존 `<head>` 내 메타태그 부분(1~10번째 줄)을 아래로 교체:

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>AI 뉴스 | 2026.04.18 (Sat) | COALAB</title>
  <meta name="description" content="매일 아침 최신 AI 뉴스를 한눈에. COALAB AI 교육 전문가가 큐레이팅하는 국내외 AI 주요 이슈.">
  <meta name="keywords" content="AI뉴스, 인공지능뉴스, AI교육, COALAB, 코아랩, GPT, 머신러닝">
  <meta name="author" content="COALAB">
  <link rel="canonical" href="https://ai-news.coalab.co.kr/index.html">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="COALAB AI뉴스">
  <meta property="og:title" content="AI 뉴스 | 2026.04.18 (Sat) | COALAB">
  <meta property="og:description" content="매일 아침 최신 AI 뉴스를 한눈에. COALAB AI 교육 전문가가 큐레이팅하는 국내외 AI 주요 이슈.">
  <meta property="og:url" content="https://ai-news.coalab.co.kr/index.html">
  <meta property="og:image" content="https://ai-news.coalab.co.kr/ai-news-img1.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="AI 뉴스 | COALAB">
  <meta name="twitter:description" content="매일 아침 최신 AI 뉴스를 한눈에.">
```

- [ ] **Step 2: 커밋**

```bash
git add index.html
git commit -m "feat: index.html SEO 메타태그 강화"
```

---

## Task 5: index.html — 애드센스 준비 + CTA 배너 + 푸터 개선

**Files:**
- Modify: `index.html`

- [ ] **Step 1: `<head>` 스타일 영역에 CTA 배너 CSS 추가**

`index.html`의 `<style>` 블록 끝(`</style>` 바로 앞)에 추가:

```css
    /* 애드센스 광고 자리 */
    .ad-slot{width:100%;min-height:90px;background:#f0f4f8;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:13px;margin:24px 0}

    /* coalab CTA 배너 */
    .cta-banner{background:linear-gradient(135deg,#1a4d3a 0%,#2d8659 100%);border-radius:14px;padding:20px 28px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin:32px 0}
    .cta-banner .cta-text{color:#fff}
    .cta-banner .cta-text strong{display:block;font-size:16px;font-weight:800;margin-bottom:4px}
    .cta-banner .cta-text span{font-size:13px;opacity:.85}
    .cta-banner .cta-btn{display:inline-flex;align-items:center;gap:6px;background:#fff;color:#1a4d3a;font-size:14px;font-weight:700;padding:10px 20px;border-radius:8px;text-decoration:none;white-space:nowrap;transition:opacity .2s}
    .cta-banner .cta-btn:hover{opacity:.9}

    /* 교재 예고 배너 */
    .book-banner{background:#fff;border:2px solid #2d8659;border-radius:14px;padding:18px 24px;display:flex;align-items:center;gap:16px;margin:24px 0;flex-wrap:wrap}
    .book-banner .book-icon{font-size:32px;flex-shrink:0}
    .book-banner .book-text strong{display:block;font-size:15px;font-weight:800;color:#111827;margin-bottom:4px}
    .book-banner .book-text span{font-size:13px;color:#6b7280}
    .book-banner .book-btn{margin-left:auto;display:inline-flex;align-items:center;background:#2d8659;color:#fff;font-size:13px;font-weight:700;padding:8px 16px;border-radius:8px;text-decoration:none;white-space:nowrap;flex-shrink:0}
```

- [ ] **Step 2: 헤더 네비게이션에 coalab.co.kr 링크 추가**

`index.html` 106~111번째 줄의 `<nav class="site-nav">` 부분을 아래로 교체:

```html
    <nav class="site-nav">
      <a href="/index.html" class="active">홈</a>
      <a href="/board.html">기사 게시판</a>
      <a href="/archive-list.html">아카이브</a>
      <a href="https://www.coalab.co.kr" target="_blank" rel="noopener" style="background:#2d8659;color:#fff;padding:6px 14px;border-radius:8px">COALAB</a>
    </nav>
```

- [ ] **Step 3: `<main>` 시작 직후 CTA 배너 삽입**

`index.html`의 `<main class="wrap">` 바로 다음 줄에 추가:

```html
<!-- coalab 강의 문의 CTA -->
<div class="cta-banner">
  <div class="cta-text">
    <strong>AI · SQL · 코딩 교육 문의</strong>
    <span>기업교육 · 대학강의 · 파주시 지역연계 · 평생교육원</span>
  </div>
  <a href="https://open.kakao.com/o/sZhJVf7" target="_blank" rel="noopener" class="cta-btn">💬 카카오톡 문의</a>
</div>

<!-- 교재 출판 예고 -->
<div class="book-banner">
  <div class="book-icon">📘</div>
  <div class="book-text">
    <strong>출판 예정: GPT를 활용한 SQL 최적화방안</strong>
    <span>내일배움카드 과정 교재 · 사전 관심 등록</span>
  </div>
  <a href="https://open.kakao.com/o/sZhJVf7" target="_blank" rel="noopener" class="book-btn">관심 등록</a>
</div>

<!-- 상단 광고 (애드센스 승인 후 코드 교체) -->
<div class="ad-slot">광고 영역</div>
```

- [ ] **Step 4: 푸터 개선**

`index.html` 252~254번째 줄의 `<footer>` 부분을 아래로 교체:

```html
<footer class="site-footer">
  <div style="margin-bottom:12px">
    <a href="https://www.coalab.co.kr" target="_blank" rel="noopener" style="font-weight:700;color:#2d8659">COALAB</a>
    &nbsp;·&nbsp;AI 교육 전문 · 기업/대학/지역연계
    &nbsp;·&nbsp;<a href="https://open.kakao.com/o/sZhJVf7" target="_blank" rel="noopener">강의 문의</a>
  </div>
  &copy; 2026 COALAB AI뉴스 &middot; 자동 생성 (GitHub Actions)
  &middot; <a href="/privacy.html">개인정보처리방침</a>
</footer>
```

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat: 애드센스 준비 + coalab CTA 배너 + 푸터 개선"
```

---

## Task 6: templates/page.html.j2 동일 변경

**Files:**
- Modify: `templates/page.html.j2`

index.html에 적용한 변경사항을 page.html.j2에도 동일하게 적용한다. 단, Jinja2 템플릿 변수(`{{ today_kr }}` 등)는 그대로 유지한다.

- [ ] **Step 1: page.html.j2 head 메타태그 교체**

기존 1~10번째 줄을 아래로 교체 (날짜 부분만 Jinja2 변수 사용):

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>AI 뉴스 | {{ today_kr }} | COALAB</title>
  <meta name="description" content="매일 아침 최신 AI 뉴스를 한눈에. COALAB AI 교육 전문가가 큐레이팅하는 국내외 AI 주요 이슈.">
  <meta name="keywords" content="AI뉴스, 인공지능뉴스, AI교육, COALAB, 코아랩, GPT, 머신러닝">
  <meta name="author" content="COALAB">
  <link rel="canonical" href="https://ai-news.coalab.co.kr/index.html">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="COALAB AI뉴스">
  <meta property="og:title" content="AI 뉴스 | {{ today_kr }} | COALAB">
  <meta property="og:description" content="매일 아침 최신 AI 뉴스를 한눈에. COALAB AI 교육 전문가가 큐레이팅하는 국내외 AI 주요 이슈.">
  <meta property="og:url" content="https://ai-news.coalab.co.kr/index.html">
  <meta property="og:image" content="https://ai-news.coalab.co.kr/ai-news-img1.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="AI 뉴스 | COALAB">
  <meta name="twitter:description" content="매일 아침 최신 AI 뉴스를 한눈에.">
```

- [ ] **Step 2: page.html.j2에 CSS, 배너, 푸터 적용**

Task 5의 Step 1~4와 동일한 CSS/HTML을 page.html.j2에도 적용한다.
- `</style>` 앞에 Task 5 Step 1의 CSS 추가
- `<main class="wrap">` 다음에 Task 5 Step 3의 배너 HTML 추가
- `<footer>` 부분을 Task 5 Step 4로 교체

- [ ] **Step 3: 커밋**

```bash
git add templates/page.html.j2
git commit -m "feat: 템플릿에 SEO + CTA 배너 + 푸터 동기화"
```

---

## Task 7: 최종 확인 및 배포

- [ ] **Step 1: 변경사항 로컬 확인**

브라우저에서 `index.html`을 직접 열어 확인:
- CTA 배너 표시 여부
- 교재 예고 배너 표시 여부
- 푸터에 coalab 링크 + 개인정보처리방침 링크
- 네비게이션에 COALAB 버튼

- [ ] **Step 2: GitHub push**

```bash
git push origin main
```

Expected: GitHub Actions가 트리거되어 사이트 자동 배포

- [ ] **Step 3: 라이브 사이트 확인**

https://ai-news.coalab.co.kr 에서 변경사항 확인

---

## 배포 후 직접 해야 할 작업 (코드 아님)

1. **Google Search Console** 등록
   - https://search.google.com/search-console
   - ai-news.coalab.co.kr 속성 추가 → sitemap.xml 제출

2. **Google AdSense 신청**
   - https://www.google.com/adsense
   - 사이트 URL: ai-news.coalab.co.kr
   - 승인 후 `<head>`의 `<!-- 애드센스 코드 삽입 위치 -->` 자리에 코드 추가
