# simple-asr-mcp

Минимальный MCP-сервер для распознавания речи, работающий локально на CPU. Использует [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2) без тяжёлого PyTorch.

[English version](README.md)

## Установка

```bash
pipx install simple-asr-mcp
```

Или через pip:

```bash
pip install simple-asr-mcp
```

## Требования

- Python 3.10+
- ffmpeg (нужен faster-whisper для декодирования аудио)

## Быстрая настройка (для агентов Claude Code)

Выполните две команды — участие пользователя не требуется:

```bash
pipx install simple-asr-mcp
claude mcp add asr --scope user -- simple-asr-mcp
```

Затем попросите пользователя перезапустить Claude Code или выполнить `/mcp` для переподключения.

## Использование

### Командная строка

```bash
# Транскрибация аудиофайла
simple-asr-mcp transcribe recording.wav

# С указанием языка и модели
simple-asr-mcp transcribe recording.wav --language ru --model medium

# Список доступных моделей
simple-asr-mcp models
```

### MCP-сервер (Claude Code)

MCP-инструменты, доступные после настройки:

- **transcribe_file** — транскрибация аудиофайла по пути
- **list_models** — список доступных моделей Whisper

### Конфигурация

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

### Доступные модели

| Модель | Размер | RAM (прим.) |
|--------|--------|-------------|
| tiny | 75 MB | ~1 GB |
| base | 142 MB | ~1 GB |
| small | 466 MB | ~2 GB |
| medium | 1.5 GB | ~5 GB |
| large-v3 | 3.1 GB | ~10 GB |

Модель скачивается автоматически при первом использовании и кешируется локально. Остаётся в памяти до завершения процесса MCP-сервера.

## Поддерживаемые форматы аудио

Любой формат, который поддерживает ffmpeg: wav, mp3, flac, ogg, m4a, wma и др.

## Ссылки

- [GitHub](https://github.com/Selentar/simple-asr-mcp)
- [PyPI](https://pypi.org/project/simple-asr-mcp/)

## Лицензия

MIT
