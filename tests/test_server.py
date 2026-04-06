import os
import pytest
from unittest.mock import patch

from simple_asr_mcp.server import format_transcription, format_model_list, WHISPER_MODELS, transcribe_file


def test_format_transcription():
    """Transcription output matches expected markdown-like format."""
    class Seg:
        def __init__(self, start, end, text, avg_logprob, no_speech_prob):
            self.start = start
            self.end = end
            self.text = text
            self.avg_logprob = avg_logprob
            self.no_speech_prob = no_speech_prob

    class Info:
        language = "ru"
        language_probability = 0.97
        duration = 5.3

    segments = [
        Seg(0.0, 2.1, "Привет.", -0.08, 0.01),
        Seg(2.1, 5.3, "Как дела?", -0.12, 0.02),
    ]
    info = Info()
    result = format_transcription(segments, info, "small")

    assert "Language: ru (confidence: 0.97)" in result
    assert "Duration: 5.3s" in result
    assert "Model: small" in result
    assert "## Transcription" in result
    assert "Привет. Как дела?" in result
    assert "## Segments" in result
    assert "[0.0s - 2.1s] Привет." in result
    assert "[2.1s - 5.3s] Как дела?" in result
    assert "confidence:" in result
    assert "no_speech:" in result


def test_default_config():
    """Default config values when no env vars are set."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("WHISPER_MODEL", "WHISPER_DEVICE", "WHISPER_COMPUTE_TYPE")}
    with patch.dict(os.environ, env, clear=True):
        import importlib
        import simple_asr_mcp.server as srv
        importlib.reload(srv)
        assert srv.DEFAULT_MODEL == "small"
        assert srv.DEFAULT_DEVICE == "cpu"
        assert srv.DEFAULT_COMPUTE_TYPE == "int8"


def test_format_model_list():
    """Model list output contains table with download status."""
    result = format_model_list(downloaded={"small"}, default_model="small")
    assert "## Available Whisper Models" in result
    assert "| small" in result
    assert "Yes" in result
    assert "Current default: small" in result


def test_whisper_models_has_expected_entries():
    """All standard Whisper models are present."""
    names = [m["name"] for m in WHISPER_MODELS]
    assert "tiny" in names
    assert "base" in names
    assert "small" in names
    assert "medium" in names
    assert "large-v3" in names


def test_config_from_env():
    """Config picks up env vars."""
    env = {
        "WHISPER_MODEL": "medium",
        "WHISPER_DEVICE": "cuda",
        "WHISPER_COMPUTE_TYPE": "float16",
    }
    with patch.dict(os.environ, env):
        import importlib
        import simple_asr_mcp.server as srv
        importlib.reload(srv)
        assert srv.DEFAULT_MODEL == "medium"
        assert srv.DEFAULT_DEVICE == "cuda"
        assert srv.DEFAULT_COMPUTE_TYPE == "float16"


def test_server_has_tools():
    """MCP server exposes transcribe_file and list_models tools."""
    from simple_asr_mcp.server import mcp
    # FastMCP stores tools in _tool_manager
    tool_names = list(mcp._tool_manager._tools.keys())
    assert "transcribe_file" in tool_names
    assert "list_models" in tool_names


def test_transcribe_file_not_found():
    """transcribe_file raises FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError, match="File not found"):
        transcribe_file("/nonexistent/audio.wav")


def test_cli_transcribe_missing_file(capsys):
    """CLI transcribe prints error for missing file."""
    from simple_asr_mcp.server import main
    with pytest.raises(SystemExit, match="1"):
        main(["transcribe", "/nonexistent/audio.wav"])
    captured = capsys.readouterr()
    assert "File not found" in captured.err


def test_cli_models(capsys):
    """CLI models prints model list."""
    from simple_asr_mcp.server import main
    main(["models"])
    captured = capsys.readouterr()
    assert "Available Whisper Models" in captured.out
    assert "small" in captured.out


def test_cli_no_args_returns_none():
    """main() with no args returns None (would start MCP server)."""
    from simple_asr_mcp.server import main
    from unittest.mock import patch as mock_patch
    with mock_patch("simple_asr_mcp.server.mcp") as mock_mcp:
        main([])
        mock_mcp.run.assert_called_once()


def test_cli_version(capsys):
    """CLI --version prints version string."""
    from simple_asr_mcp.server import main
    from simple_asr_mcp import __version__
    with pytest.raises(SystemExit, match="0"):
        main(["--version"])
    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_cli_help(capsys):
    """CLI --help prints usage info."""
    from simple_asr_mcp.server import main
    with pytest.raises(SystemExit, match="0"):
        main(["--help"])
    captured = capsys.readouterr()
    assert "transcribe" in captured.out
    assert "models" in captured.out
