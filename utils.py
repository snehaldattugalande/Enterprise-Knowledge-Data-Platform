import base64
import json
import logging
from pathlib import Path
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with path.open("r", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    logger.info("Loaded config from %s", config_path)
    return config


def decode_base64_content(content_base64: str) -> bytes:
    return base64.b64decode(content_base64)


def serialize_event(event: Any) -> str:
    return json.dumps(event, default=str)
