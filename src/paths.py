"""Shared path resolution for running both from the source tree (dev mode)
and from a Debian package install (under /usr/lib, /usr/share, ~/.config)."""

import json
import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
INSTALLED_SHARE_CONF_DIR = Path("/usr/share/cpu-cooler-lcd/conf")
INSTALLED_ICON_PATH = Path("/usr/share/icons/hicolor/256x256/apps/cpu-cooler-lcd.png")


def get_share_conf_dir():
    """Directory containing the read-only device layout JSON files."""
    local = PACKAGE_DIR.parent / "conf"
    if local.exists():
        return local
    return INSTALLED_SHARE_CONF_DIR


def get_user_config_dir():
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "cpu-cooler-lcd"


def get_user_config_path():
    return get_user_config_dir() / "config.json"


def ensure_user_config():
    """Return the user's config.json path, creating it from the default
    config if it doesn't exist yet."""
    config_path = get_user_config_path()
    if not config_path.exists():
        from config import default_config
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)
    return config_path


def get_icon_path():
    local = PACKAGE_DIR.parent / "assets" / "icon.png"
    if local.exists():
        return local
    return INSTALLED_ICON_PATH
