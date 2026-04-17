import asyncio
import subprocess

from morning_call.config import TARGET_WORD_COUNT

SYSTEM_PROMPT = f"""You are a morning news briefing host named "모닝콜" (Morning Call).
Your job is to write a podcast script for a ~20-minute audio news briefing.

Style guidelines:
- Conversational, warm, and clear. Like a knowledgeable friend catching someone up.
- Open with a brief greeting and date, then preview the top 2-3 stories.
- Organize into sections: "테크 & AI", "세계 뉴스", "한국 뉴스".
- For each section: pick the 3-5 most important/interesting stories, summarize each
  in 2-4 sentences, add brief context or analysis where useful.
- Use smooth transitions between sections and stories.
- End with a short sign-off.
- Total length: approximately {TARGET_WORD_COUNT} words (this produces ~20 minutes of audio at TTS pace).
- Write the entire script in Korean (한국어). Proper nouns and tech terms can stay in English.
- Do NOT include any stage directions, sound effect markers, or non-spoken text.
  Everything you write will be read aloud verbatim by TTS."""


async def generate_script(articles: list[dict], date_str: str) -> str:
    articles_text = "\n\n".join(
        f"[{a['source']}] {a['title']}\n{a['body']}" for a in articles
    )

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Today's date: {date_str}\n\n"
        f"Here are today's news articles:\n\n{articles_text}\n\n"
        f"Please write today's morning briefing script."
    )

    result = await asyncio.to_thread(
        subprocess.run,
        ["claude", "-p"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=600,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI failed: {result.stderr}")

    output = result.stdout.strip()

    # Claude CLI may include meta-commentary before/after the script.
    # Extract just the script between --- markers if present.
    if "---" in output:
        parts = output.split("---")
        # Take the largest block between markers (the actual script)
        script = max(parts, key=len).strip()
    else:
        script = output

    return script
