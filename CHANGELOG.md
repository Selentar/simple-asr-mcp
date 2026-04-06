# Changelog

## 0.1.2

- Added CLI mode: `simple-asr-mcp transcribe <file>` and `simple-asr-mcp models`
- Added `--version` / `-v` and `--help` flags
- Added cross-platform support for huggingface cache path (Windows compatibility)
- Added ffmpeg installation instructions for Windows to README
- Added Russian README (`README.ru.md`)
- Added GitHub/PyPI links to README and pyproject.toml

## 0.1.1

- Fixed attribute name `avg_logprob` (was `avg_log_prob`) for faster-whisper Segment
- Fixed type hint for `format_transcription` segments parameter
- Updated README with correct MCP setup instructions (`--scope user`)

## 0.1.0

- Initial release
- MCP server with two tools: `transcribe_file` and `list_models`
- Lazy model loading with caching
- Configuration via environment variables (`WHISPER_MODEL`, `WHISPER_DEVICE`, `WHISPER_COMPUTE_TYPE`)
- Markdown-like output format with metadata and timestamped segments
- Model download status detection from huggingface cache
