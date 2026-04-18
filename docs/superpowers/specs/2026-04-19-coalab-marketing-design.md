# coalab 마케팅 & 수익화 설계

**날짜:** 2026-04-19  
**사이트:** ai-news.coalab.co.kr → www.coalab.co.kr  
**목표:** 트래픽 회복 + 애드센스 수익화 + 교육 사업 문의 유입

---

## 배경

- ai-news.coalab.co.kr: 매일 07:30 KST 자동 업데이트되는 AI 뉴스 카드뉴스 사이트
- 2주+ 페이지 오류로 트래픽 급감 → 2026-04-18 오류 해결 완료
- 수익 구조 미설정 (애드센스 없음, SEO 없음)
- SNS 채널: 네이버 블로그(가장 활성), 인스타그램(332명), 유튜브, 페이스북
- 네이버 블로그가 현재 유일하게 작동하는 유입 경로 (개인 수업 문의 발생 중)

## coalab 교육 사업 현황

| 영역 | 현황 |
|------|------|
| 기업교육 (내일배움카드 포함) | 주력, 진행중 |
| 대학 전문교육 | 진행중 |
| 학교 지역연계 (파주시) | 진행중, 6월 본격 시작 |
| 지역지원사업 (파주시) | 진행중 |
| 평생교육원 | 진행중 |
| 온라인 강의 | 준비중 |
| 교재 출판 (GPT×SQL 최적화 외 2권) | 준비중 |
| 전자책 | 예정 |

**연락처:** https://open.kakao.com/o/sZhJVf7 (카카오톡 오픈채팅)  
**메인 사이트:** www.coalab.co.kr

---

## 유입 경로 목표

```
현재:
네이버 블로그 → 개인 수업 문의 (유일하게 작동)

목표:
ai-news (트래픽+애드센스) → coalab.co.kr → 5개 사업 문의
네이버 블로그 → coalab.co.kr → 더 많은 사업 문의
인스타/유튜브/페이스북 → ai-news / coalab.co.kr
```

---

## 구현 순서

### 1단계: ai-news 수익화 (지금 바로)

#### 1-1. SEO 세팅
- `sitemap.xml` 생성 (index + 전체 archive 페이지)
- `robots.txt` 생성
- 모든 페이지 `<head>` 메타태그: description, keywords, og:title, og:description, og:image, canonical

#### 1-2. 애드센스 준비
- `privacy.html` 신규 생성 (애드센스 승인 필수)
- `<head>`에 애드센스 스크립트 자리 마련
- 광고 배치 위치: 헤더 아래, 카드 그리드 중간(6번째), 푸터 위
- 네비게이션/푸터에 privacy.html 링크 추가

#### 1-3. coalab 연결 CTA
- 상단 헤더에 coalab.co.kr 로고/링크
- 사이트 중단 배너: "coalab 강의 문의 → 카카오톡 오픈채팅"
- 사이트 하단 배너: "📘 출판 예정: GPT를 활용한 SQL 최적화방안"
- 푸터에 www.coalab.co.kr 링크

### 2단계: coalab.co.kr 개편 (ai-news 완료 후)

- 메인 페이지에 5개 교육 영역 카드 형태로 명확하게 표시
- 각 영역별 문의 CTA (카카오톡 오픈채팅)
- ai-news 링크 추가 ("매일 AI 뉴스 보기")
- 네이버 블로그 링크 강화

---

## 비기능 요구사항

- 기존 사이트 스타일(dark newspaper) 유지
- 모바일 반응형 유지
- GitHub Pages 정적 사이트 (서버 사이드 없음)
- 매일 지속적으로 개선 진행

---

## Google Search Console / 애드센스 신청 (직접 진행)

코드 작업 완료 후 사용자가 직접 해야 할 것:
1. Google Search Console에 ai-news.coalab.co.kr 등록 + sitemap 제출
2. Google AdSense 신청 (사이트 URL: ai-news.coalab.co.kr)
3. 애드센스 승인 후 광고 코드 삽입
