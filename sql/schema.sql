-- AI 뉴스 게시판 Supabase 스키마
-- Supabase 대시보드 > SQL Editor에서 실행하세요.

-- 1. articles 테이블 생성
CREATE TABLE articles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  summary TEXT,
  author TEXT DEFAULT '관리자',
  category TEXT DEFAULT '일반',
  thumbnail_url TEXT,
  slug TEXT UNIQUE,
  published BOOLEAN DEFAULT true,
  view_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. 인덱스 생성 (검색 성능 향상)
CREATE INDEX idx_articles_published ON articles (published);
CREATE INDEX idx_articles_created_at ON articles (created_at DESC);
CREATE INDEX idx_articles_category ON articles (category);
CREATE INDEX idx_articles_slug ON articles (slug);

-- 3. Row Level Security (RLS) 활성화
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

-- 4. RLS 정책: 공개 기사는 누구나 조회 가능
CREATE POLICY "Public can read published articles" ON articles
  FOR SELECT
  USING (published = true);

-- 5. RLS 정책: 인증된 사용자(관리자)는 모든 기사에 대해 CRUD 가능
CREATE POLICY "Authenticated users have full access" ON articles
  FOR ALL
  USING (auth.role() = 'authenticated')
  WITH CHECK (auth.role() = 'authenticated');

-- 6. 조회수 증가를 위한 함수 (RLS를 우회하는 서버 함수)
-- 비인증 사용자도 조회수를 증가시킬 수 있도록 합니다.
CREATE OR REPLACE FUNCTION increment_view_count(article_id UUID)
RETURNS void AS $$
BEGIN
  UPDATE articles
  SET view_count = view_count + 1
  WHERE id = article_id AND published = true;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===================================
-- 설정 완료 후 할 일:
-- ===================================
-- 1. Supabase 대시보드 > Authentication > Users에서 관리자 계정 생성
--    (이메일/비밀번호 방식)
-- 2. Project Settings > API에서 Project URL과 anon key 복사
-- 3. js/supabase-config.js 파일에 URL과 key 붙여넣기
