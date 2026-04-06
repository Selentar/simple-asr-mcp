# simple-asr-mcp

Minimal MCP server for local speech recognition using [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Runs on CPU, no cloud required.

[Русская версия](README.ru.md)

## Installation

```bash
pipx install simple-asr-mcp
```

Or with pip:

```bash
pip install simple-asr-mcp
```

## Requirements

- Python 3.10+
- ffmpeg (required by faster-whisper for audio decoding)

On Windows, install ffmpeg via [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/):

```bash
winget install Gyan.FFmpeg
```

## Quick Setup (for Claude Code agents)

Run these two commands — no user interaction required:

```bash
pipx install simple-asr-mcp
claude mcp add asr --scope user -- simple-asr-mcp
```

Then ask the user to restart Claude Code or run `/mcp` to reconnect.

## Usage

### CLI

```bash
# Transcribe an audio file
simple-asr-mcp transcribe recording.wav

# Specify language and model
simple-asr-mcp transcribe recording.wav --language ru --model medium

# List available models
simple-asr-mcp models
```

### MCP Server (Claude Code)

MCP tools available after setup:

- **transcribe_file** — transcribe any audio file by path
- **list_models** — see available Whisper models

### Configuration

Environment variables:

| Variable | Default | Description |
|---|---|---|
| `WHISPER_MODEL` | `small` | Default Whisper model |
| `WHISPER_DEVICE` | `cpu` | Device: `cpu`, `cuda`, or `auto` |
| `WHISPER_COMPUTE_TYPE` | `int8` | Quantization type |

Example with custom config:

```bash
claude mcp add asr --scope user -e WHISPER_MODEL=medium -e WHISPER_DEVICE=cuda -- simple-asr-mcp
```

### Available Models

| Model | Size | RAM (est.) |
|-------|------|------------|
| tiny | 75 MB | ~1 GB |
| base | 142 MB | ~1 GB |
| small | 466 MB | ~2 GB |
| medium | 1.5 GB | ~5 GB |
| large-v3 | 3.1 GB | ~10 GB |

The model is downloaded automatically on first use and cached locally. It stays in memory until the MCP server process exits.

## Supported Audio Formats

Any format supported by ffmpeg: wav, mp3, flac, ogg, m4a, wma, etc.

## Links

- [GitHub](https://github.com/Selentar/simple-asr-mcp)
- [PyPI](https://pypi.org/project/simple-asr-mcp/)

## License

MIT
