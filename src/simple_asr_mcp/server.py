"""Minimal MCP server for local speech recognition using faster-whisper."""

import logging
import os
import time
from collections.abc import Iterable
from pathlib import Path

from faster_whisper import WhisperModel
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger("simple-asr-mcp")

mcp = FastMCP("simple-asr-mcp")

DEFAULT_MODEL = os.getenv("WHISPER_MODEL", "small")
DEFAULT_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
DEFAULT_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

_model: WhisperModel | None = None
_model_name: str | None = None


WHISPER_MODELS = [
    {"name": "tiny", "size": "75 MB", "ram": "~1 GB"},
    {"name": "base", "size": "142 MB", "ram": "~1 GB"},
    {"name": "small", "size": "466 MB", "ram": "~2 GB"},
    {"name": "medium", "size": "1.5 GB", "ram": "~5 GB"},
    {"name": "large-v3", "size": "3.1 GB", "ram": "~10 GB"},
]


def _get_downloaded_models() -> set[str]:
    """Check huggingface cache for downloaded faster-whisper models."""
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    downloaded = set()
    if cache_dir.exists():
        for d in cache_dir.iterdir():
            if d.is_dir() and d.name.startswith("models--Systran--faster-whisper-"):
                model_name = d.name.split("faster-whisper-")[-1]
                downloaded.add(model_name)
    return downloaded


def format_model_list(downloaded: set[str], default_model: str) -> str:
    """Format model list as markdown table."""
    lines = [
        "## Available Whisper Models",
        "",
        "| Model | Size | RAM (est.) | Downloaded |",
        "|-------|------|------------|------------|",
    ]
    for m in WHISPER_MODELS:
        dl = "Yes" if m["name"] in downloaded else "No"
        lines.append(f"| {m['name']} | {m['size']} | {m['ram']} | {dl} |")
    lines.append("")
    lines.append(f"Current default: {default_model}")
    return "\n".join(lines)


def format_transcription(segments: Iterable, info, model_name: str) -> str:
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
            f"(confidence: {s.avg_logprob:.2f}, no_speech: {s.no_speech_prob:.2f})"
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


@mcp.tool()
def transcribe_file(file_path: str, language: str | None = None, model: str | None = None) -> str:
    """Transcribe an audio file at the given path.

    Supports any format that ffmpeg can decode (wav, mp3, flac, ogg, etc.).
    Returns transcription with metadata and timestamped segments.

    Args:
        file_path: Path to the audio file.
        language: Language code (e.g. "ru", "en"). None for auto-detect.
        model: Whisper model name (e.g. "small", "medium"). None for default.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        whisper = _get_model(model)
        logger.info("Transcribing: %s", file_path)
        segments, info = whisper.transcribe(file_path, language=language)
        return format_transcription(segments, info, _model_name)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe: {e}") from e


@mcp.tool()
def list_models() -> str:
    """List available Whisper models with sizes and download status."""
    downloaded = _get_downloaded_models()
    return format_model_list(downloaded, DEFAULT_MODEL)


def main(argv: list[str] | None = None):
    """Run as CLI tool or MCP server.

    If called with arguments, runs as CLI. Otherwise starts MCP server.
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="simple-asr-mcp",
        description="Local speech recognition using faster-whisper",
    )
    sub = parser.add_subparsers(dest="command")

    t = sub.add_parser("transcribe", help="Transcribe an audio file")
    t.add_argument("file_path", help="Path to audio file")
    t.add_argument("--language", "-l", default=None, help="Language code (e.g. ru, en)")
    t.add_argument("--model", "-m", default=None, help="Whisper model name")

    sub.add_parser("models", help="List available Whisper models")

    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    logging.basicConfig(level=logging.INFO, format="%(name)s - %(message)s")

    if args.command == "transcribe":
        try:
            result = transcribe_file(args.file_path, args.language, args.model)
            print(result)
        except (FileNotFoundError, RuntimeError) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
    elif args.command == "models":
        print(list_models())
    else:
        mcp.run()
