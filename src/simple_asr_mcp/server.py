"""Minimal MCP server for local speech recognition using faster-whisper."""

import logging
import os
import time

from faster_whisper import WhisperModel

logger = logging.getLogger("simple-asr-mcp")

DEFAULT_MODEL = os.getenv("WHISPER_MODEL", "small")
DEFAULT_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
DEFAULT_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

_model: WhisperModel | None = None
_model_name: str | None = None


def format_transcription(segments: list, info, model_name: str) -> str:
    """Format transcription result as markdown-like text for LLMs."""
    seg_list = list(segments)
    full_text = " ".join(s.text.strip() for s in seg_list)

    lines = [
        f"Language: {info.language} (confidence: {info.language_probability:.2f})",
        f"Duration: {info.duration:.1f}s",
        f"Model: {model_name}",
        "",
        "## Transcription",
        "",
        full_text,
        "",
        "## Segments",
        "",
    ]
    for s in seg_list:
        lines.append(
            f"[{s.start:.1f}s - {s.end:.1f}s] {s.text.strip()} "
            f"(confidence: {s.avg_log_prob:.2f}, no_speech: {s.no_speech_prob:.2f})"
        )
    return "\n".join(lines)


def _get_model(model_name: str | None = None) -> WhisperModel:
    """Return cached model or create a new one."""
    global _model, _model_name
    name = model_name or DEFAULT_MODEL
    if _model is not None and _model_name == name:
        return _model
    logger.info("Loading Whisper model '%s' (device=%s, compute_type=%s)...",
                name, DEFAULT_DEVICE, DEFAULT_COMPUTE_TYPE)
    start = time.time()
    _model = WhisperModel(name, device=DEFAULT_DEVICE, compute_type=DEFAULT_COMPUTE_TYPE)
    _model_name = name
    logger.info("Model loaded in %.1fs", time.time() - start)
    return _model
