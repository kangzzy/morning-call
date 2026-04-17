import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

from morning_call.config import FEEDS, ARTICLES_PER_FEED, OUTPUT_DIR
from morning_call.feeds import fetch_all_feeds
from morning_call.summarizer import generate_script
from morning_call.tts import generate_audio

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def run() -> None:
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"{date_str}_morning.mp3"
    script_path = OUTPUT_DIR / f"{date_str}_morning.txt"

    if output_path.exists():
        logger.info("Already generated: %s", output_path)
        return

    logger.info("[1/3] Fetching news articles...")
    articles = await fetch_all_feeds(FEEDS, ARTICLES_PER_FEED)
    logger.info("  Fetched %d articles", len(articles))

    if not articles:
        logger.error("No articles fetched. Aborting.")
        return

    logger.info("[2/3] Generating briefing script via Claude...")
    script = await generate_script(articles, date_str)
    script_path.write_text(script, encoding="utf-8")
    logger.info("  Script saved: %s (%d chars)", script_path, len(script))

    logger.info("[3/3] Converting to audio...")
    await generate_audio(script, str(output_path))
    logger.info("  Audio saved: %s", output_path)

    _cleanup_old(OUTPUT_DIR, days=7)


def _cleanup_old(directory: Path, days: int) -> None:
    cutoff = datetime.now() - timedelta(days=days)
    for f in directory.glob("*_morning.*"):
        date_part = f.stem.split("_")[0]
        try:
            file_date = datetime.strptime(date_part, "%Y-%m-%d")
            if file_date < cutoff:
                f.unlink()
                logger.info("Cleaned up old file: %s", f)
        except ValueError:
            pass


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
