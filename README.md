# 📰 AI 뉴스 카드뉴스 (Daily, 07:30 KST)

[![Site](https://img.shields.io/badge/Live%20Site-https://coalab.github.io/ai--news-2ea44f?logo=google-chrome&color=2ea44f)](https://coalab.github.io/ai-news/)
![Build](https://img.shields.io/github/actions/workflow/status/coalab/ai-news/daily-build.yml?label=daily%20build)
![Schedule](https://img.shields.io/badge/Schedule-07%3A30%20KST%20daily-blue)

매일 아침 **07:30 (KST)**, GitHub Actions가 RSS에서 최신 AI 뉴스를 수집해  
자동으로 `index.html`과 `/archive/YYYY-MM-DD/`를 생성합니다.  

👉 항상 최신판은 [https://coalab.github.io/ai-news/](https://coalab.github.io/ai-news/) 에서 볼 수 있습니다.

---

## 📌 주요 기능
- 매일 아침 07:30(KST) 자동 업데이트
- 전 세계 + 국내 AI 뉴스 소스 수집 (Reuters, The Verge, MIT Tech Review, 연합뉴스 등)
- 10개 주요 뉴스를 카드 형식으로 요약 표시
- 날짜별 아카이브 제공: `/archive/YYYY-MM-DD/`
- 네이버 블로그/카카오톡 공유에 적합한 메타 태그 포함

---

## 📂 저장소 구조
```
ai-news/
├─ index.html                 # 항상 최신판 (GitHub Pages 기본 진입점)
├─ feeds.yaml                 # 뉴스 소스(RSS) 목록
├─ requirements.txt           # 파이썬 의존성
├─ templates/
│   └─ page.html.j2           # 카드뉴스 HTML 템플릿
├─ scripts/
│   └─ build.py               # RSS→HTML 생성 스크립트
└─ .github/
    └─ workflows/
        └─ daily-build.yml    # 매일 아침 07:30(KST) 자동 빌드
```

---

## ⚙️ 커스터마이즈
- **뉴스 소스 변경**: `feeds.yaml`
- **스타일 변경**: `templates/page.html.j2`
- **업데이트 시간 변경**: `.github/workflows/daily-build.yml` → `cron` 수정  
  (예: 한국시간 06:00 = `21 21 * * *` UTC)

---

## 🚀 사용 방법
1. 저장소 클론  
2. 로컬에서 실행하려면:
   ```bash
   pip install -r requirements.txt
   python scripts/build.py
   ```
3. 결과물은 `index.html` + `archive/YYYY-MM-DD/index.html` 로 생성  
4. GitHub Pages가 자동으로 배포

---

## 📌 링크
- **Live Site:** [https://coalab.github.io/ai-news/](https://coalab.github.io/ai-news/)
- **Archive Example:** [https://coalab.github.io/ai-news/archive/2025-10-03/](https://coalab.github.io/ai-news/archive/2025-10-03/)

---

© 2025 COALAB · Daily AI News
