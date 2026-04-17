# Morning Call

매일 아침 주요 뉴스를 20분 분량의 한국어 오디오 브리핑으로 만들어주는 도구입니다.

## 구조

```
RSS 뉴스 수집 → Claude CLI로 팟캐스트 대본 생성 → edge-tts로 음성 변환 → MP3 출력
```

뉴스 소스:
- **테크/AI**: TechCrunch, The Verge, Ars Technica, Hacker News
- **세계 뉴스**: BBC World, AP News
- **한국 뉴스**: 조선일보, 한겨레, 연합뉴스

## 요구사항

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg`)
- [Claude Code CLI](https://claude.ai/code) (대본 생성에 사용)

## 설치

```bash
git clone <repo-url>
cd morning-call
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 실행

```bash
source .venv/bin/activate
python -m morning_call.main
```

`output/` 디렉토리에 파일이 생성됩니다:
- `YYYY-MM-DD_morning.mp3` - 오디오 브리핑
- `YYYY-MM-DD_morning.txt` - 대본 텍스트

오디오 재생:

```bash
afplay output/YYYY-MM-DD_morning.mp3
```

## 매일 자동 실행 (cron)

```bash
# 매일 오전 6:30 실행 + 자동 재생
crontab -e
30 6 * * * /path/to/morning-call/scripts/run.sh >> /path/to/morning-call/output/cron.log 2>&1
```

## 설정

`src/morning_call/config.py`에서 변경 가능:

| 항목 | 기본값 | 설명 |
|------|--------|------|
| `FEEDS` | 9개 소스 | RSS 피드 URL 목록 |
| `ARTICLES_PER_FEED` | 3 | 피드당 가져올 기사 수 |
| `TARGET_WORD_COUNT` | 3000 | 대본 목표 단어 수 (~20분) |
| `TTS_VOICE` | `ko-KR-SunHiNeural` | TTS 음성 (한국어 여성) |
| `TTS_RATE` | `+5%` | 음성 속도 |
