import logging
import os
import tempfile

import edge_tts
from pydub import AudioSegment

from morning_call.config import TTS_VOICE, TTS_RATE, SECTION_PAUSE_MS

logger = logging.getLogger(__name__)


async def generate_audio(script: str, output_path: str) -> None:
    sections = [s.strip() for s in script.split("\n\n") if s.strip()]
    silence = AudioSegment.silent(duration=SECTION_PAUSE_MS)
    audio_segments: list[AudioSegment] = []

    for i, section_text in enumerate(sections):
        tmp_path = os.path.join(tempfile.gettempdir(), f"mc_section_{i}.mp3")
        try:
            communicate = edge_tts.Communicate(section_text, TTS_VOICE, rate=TTS_RATE)
            await communicate.save(tmp_path)
            segment = AudioSegment.from_mp3(tmp_path)
            audio_segments.append(segment)
            audio_segments.append(silence)
        except Exception as e:
            logger.warning("TTS failed for section %d, skipping: %s", i, e)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    if not audio_segments:
        raise RuntimeError("No audio segments generated")

    final = audio_segments[0]
    for seg in audio_segments[1:]:
        final += seg

    final.export(output_path, format="mp3", bitrate="128k")
