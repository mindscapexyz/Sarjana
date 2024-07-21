import os
import sys
from pathlib import Path

VERSION = f"0.0.{os.environ.get('BUILD_VERSION', '0')}"

PRODUCT_NAME = "Sarjana"
TARGET_NAME = "Sarjana.exe"
if sys.platform.startswith("win"):
    INSTALL_DIR = Path(os.environ["PROGRAMFILES"]) / PRODUCT_NAME
    USER_DATA_DIR = Path(os.environ["ALLUSERSPROFILE"]) / PRODUCT_NAME
else:
    INSTALL_DIR = Path(os.path.expanduser("~")) / PRODUCT_NAME
    USER_DATA_DIR = Path(os.path.expanduser("~")) / "userdata" / PRODUCT_NAME
VERSION_CONTROL_DIR = USER_DATA_DIR / "versions"
METADATA_DIR = VERSION_CONTROL_DIR / "metadata"
TARGET_DIR = VERSION_CONTROL_DIR / "target"
MODULE_DIR = Path(sys.executable).parent
