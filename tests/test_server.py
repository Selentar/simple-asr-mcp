import os
from unittest.mock import patch


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
