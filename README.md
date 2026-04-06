# simple-asr-mcp

[English](#english) | [Русский](#русский)

## Русский

Минимальный MCP-сервер для распознавания речи, работающий локально на CPU. Использует [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2) без тяжёлого PyTorch.

### Установка

```bash
pipx install simple-asr-mcp
```

Или через pip:

```bash
pip install simple-asr-mcp
```

### Требования

- Python 3.10+
- ffmpeg (нужен faster-whisper для декодирования аудио)

### Быстрая настройка (для агентов Claude Code)

Выполните две команды — участие пользователя не требуется:

```bash
pipx install simple-asr-mcp
claude mcp add asr --scope user -- simple-asr-mcp
```

Затем попросите пользователя перезапустить Claude Code или выполнить `/mcp` для переподключения.

### Использование

#### Инструменты

- **transcribe_file** — транскрибация аудиофайла по пути
- **list_models** — список доступных моделей Whisper

#### Конфигурация

Переменные окружения:

| Переменная | По умолчанию | Описание |
|---|---|---|
| `WHISPER_MODEL` | `small` | Модель по умолчанию |
| `WHISPER_DEVICE` | `cpu` | Устройство: `cpu`, `cuda` или `auto` |
| `WHISPER_COMPUTE_TYPE` | `int8` | Тип квантизации |

Пример с кастомной конфигурацией:

```bash
claude mcp add asr --scope user -e WHISPER_MODEL=medium -e WHISPER_DEVICE=cuda -- simple-asr-mcp
```

#### Доступные модели

| Модель | Размер | RAM (прим.) |
|--------|--------|-------------|
| tiny | 75 MB | ~1 GB |
| base | 142 MB | ~1 GB |
| small | 466 MB | ~2 GB |
| medium | 1.5 GB | ~5 GB |
| large-v3 | 3.1 GB | ~10 GB |

Модель скачивается автоматически при первом использовании и кешируется локально. Остаётся в памяти до завершения процесса MCP-сервера.

### Поддерживаемые форматы аудио

Любой формат, который поддерживает ffmpeg: wav, mp3, flac, ogg, m4a, wma и др.

---

## English

Minimal MCP server for local speech recognition using [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Runs on CPU, no cloud required.

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

## Quick Setup (for Claude Code agents)

Run these two commands — no user interaction required:

```bash
pipx install simple-asr-mcp
claude mcp add asr --scope user -- simple-asr-mcp
```

Then ask the user to restart Claude Code or run `/mcp` to reconnect.

## Usage

### Tools

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

## License

MIT
