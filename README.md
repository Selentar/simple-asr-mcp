# simple-asr-mcp

Minimal MCP server for local speech recognition using [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Runs on CPU, no cloud required.

## Installation

```bash
pipx install simple-asr-mcp
```

Or with pip:

```bash
pip install simple-asr-mcp
```

## Usage

### Claude Code

Add to `~/.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "asr": {
      "command": "simple-asr-mcp"
    }
  }
}
```

Restart Claude Code. Then use:

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

```json
{
  "mcpServers": {
    "asr": {
      "command": "simple-asr-mcp",
      "env": {
        "WHISPER_MODEL": "medium",
        "WHISPER_DEVICE": "cuda"
      }
    }
  }
}
```

## Supported Audio Formats

Any format supported by ffmpeg: wav, mp3, flac, ogg, m4a, wma, etc.

## License

MIT
