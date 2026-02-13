// Supabase 설정
// 아래 값을 본인의 Supabase 프로젝트 URL과 anon key로 교체하세요.
const SUPABASE_URL = 'https://onfddgmyzkeaxidpdwra.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9uZmRkZ215emtlYXhpZHBkd3JhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2NzgwMDcsImV4cCI6MjA3ODI1NDAwN30.pwzxOD_6TEQT-KWZzvvlIXCnR6qr_9kN6jFf57FtAwo';

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 현재 로그인 사용자 확인
async function getCurrentUser() {
  const { data: { user } } = await supabase.auth.getUser();
  return user;
}

// 로그인
async function signIn(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
  return data;
}

// 로그아웃
async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

// 인증 상태 변경 리스너
function onAuthStateChange(callback) {
  supabase.auth.onAuthStateChange((_event, session) => {
    callback(session?.user || null);
  });
}
