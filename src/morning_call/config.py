from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

FEEDS = {
    # Tech / AI
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "Hacker News": "https://hnrss.org/frontpage?count=10",
    # World News
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "AP News": "https://rsshub.app/apnews/topics/apf-topnews",
    # Korean News
    "조선일보": "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
    "한겨레": "https://www.hani.co.kr/rss/",
    "연합뉴스": "https://www.yna.co.kr/RSS/news.xml",
}

ARTICLES_PER_FEED = 3
TARGET_WORD_COUNT = 3000
TTS_VOICE = "ko-KR-SunHiNeural"
TTS_RATE = "+5%"
SECTION_PAUSE_MS = 1500
