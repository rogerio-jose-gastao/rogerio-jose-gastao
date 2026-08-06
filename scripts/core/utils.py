"""
Utility functions for configuration loading, logging, and environment helpers.
"""

from __future__ import annotations

import datetime
import logging
import os
from pathlib import Path
import tomllib
from typing import Any, Dict

# Configure logger
logger = logging.getLogger("readme_engine")


def setup_logging(verbose: bool = False) -> None:
    """Configure system logging level and format."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )


def get_project_root() -> Path:
    """Return absolute path to root directory of project."""
    return Path(__file__).resolve().parent.parent.parent


def load_toml_config(file_path: str | Path) -> Dict[str, Any]:
    """
    Load TOML configuration file securely using Python standard tomllib.

    Args:
        file_path: Path to the TOML file relative to root or absolute.

    Returns:
        Dict representation of the TOML file.
    """
    path = Path(file_path)
    if not path.is_absolute():
        path = get_project_root() / path

    if not path.exists():
        logger.warning("Config file %s does not exist. Returning empty dict.", path)
        return {}

    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception as exc:
        logger.error("Failed to parse TOML file %s: %s", path, exc)
        return {}


def get_current_date_str() -> str:
    """Return current date formatted as YYYY-MM-DD."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
