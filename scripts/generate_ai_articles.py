import os
import json
import time
import requests
import anthropic
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ===== 설정 =====
ANTHROPIC_API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).date().isoformat()

ROOT     = Path(__file__).resolve().parents[1]
OUT_FILE = ROOT / "data" / "ai-articles.json"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

TOPICS = [
    "생성형 AI 최신 기술 동향",
    "AI와 의료 산업의 변화",
    "자율주행 AI 기술 현황",
    "AI 반도체 산업 전망",
    "교육 분야 AI 활용 사례",
]

KEYWORDS = [
    "artificial intelligence",
    "medical technology",
    "self driving car",
    "semiconductor chip",
    "education technology",
]

# ===== Unsplash 이미지 =====
def fetch_unsplash_image(keyword: str, index: int) -> str:
    if not UNSPLASH_ACCESS_KEY:
        import random; seed = random.randint(1, 1000)
    return f"https://picsum.photos/seed/{seed}/800/450"
    try:
        url = "https://api.unsplash.com/photos/random"
        params = {"query": keyword, "orientation": "landscape", "client_id": UNSPLASH_ACCESS_KEY}
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.json()["urls"]["regular"]
    except Exception as e:
        print(f"Unsplash 오류 ({keyword}): {e}")
    import random; seed = random.randint(1, 1000)
    return f"https://picsum.photos/seed/{seed}/800/450"

# ===== Claude API로 기사 생성 =====
def generate_article(client: anthropic.Anthropic, topic: str) -> dict:
    prompt = f"""다음 주제로 AI 뉴스 기사를 한국어로 작성해주세요.

주제: {topic}

아래 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.

{{
  "title": "기사 제목 (15자 이내)",
  "summary": "한 줄 요약 (30자 이내)",
  "body": "기사 본문 (300자 내외, 자연스러운 문장으로)"
}}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    text = message.content[0].text.strip()
    # JSON 블록만 추출
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

# ===== 메인 =====
def main():
    if not ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 환경변수가 없습니다.")
        return

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    articles = []

    for i, (topic, keyword) in enumerate(zip(TOPICS, KEYWORDS)):
        print(f"[{i+1}/{len(TOPICS)}] 생성 중: {topic}")
        try:
            data = generate_article(client, topic)
            image_url = fetch_unsplash_image(keyword, i)
            articles.append({
                "id": f"ai-{int(time.time() * 1000)}-{i}",
                "title": data.get("title", topic),
                "summary": data.get("summary", ""),
                "body": data.get("body", ""),
                "image": image_url,
                "topic": topic,
                "date": today,
                "source": "AI 자동 생성"
            })
            time.sleep(1)
        except Exception as e:
            print(f"  오류: {e}")

    result = {"updated": datetime.now(KST).isoformat(), "articles": articles}
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {len(articles)}개 기사 생성 완료 → data/ai-articles.json")

if __name__ == "__main__":
    main()
