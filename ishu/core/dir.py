# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import os
import shutil
import urllib.request
import zipfile
from pathlib import Path

from ishu import logger


def ensure_binaries():
    """
    Ensure FFmpeg and Deno are installed and in PATH.
    If missing (e.g. on cloud platforms like Heroku), download static binaries automatically.
    """
    bin_dir = Path("/tmp/bin")
    bin_dir.mkdir(parents=True, exist_ok=True)
    bin_dir_str = str(bin_dir)
    
    if bin_dir_str not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{bin_dir_str}:{os.environ.get('PATH', '')}"

    if not shutil.which("ffmpeg"):
        ffmpeg_bin = bin_dir / "ffmpeg"
        if not ffmpeg_bin.exists():
            logger.info("FFmpeg missing from PATH. Downloading static FFmpeg binary...")
            try:
                url = "https://github.com/eugeny/static-ffmpeg-binaries/raw/master/ffmpeg-linux-x64"
                urllib.request.urlretrieve(url, ffmpeg_bin)
                ffmpeg_bin.chmod(0o755)
                logger.info("FFmpeg downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download FFmpeg: {e}")

    if not shutil.which("deno"):
        deno_bin = bin_dir / "deno"
        if not deno_bin.exists():
            logger.info("Deno missing from PATH. Downloading Deno binary...")
            try:
                url = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip"
                zip_path = bin_dir / "deno.zip"
                urllib.request.urlretrieve(url, zip_path)
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(bin_dir)
                if zip_path.exists():
                    zip_path.unlink()
                deno_bin.chmod(0o755)
                logger.info("Deno downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download Deno: {e}")


def ensure_dirs():
    """
    Ensure that the necessary directories exist.
    """
    ensure_binaries()

    if not shutil.which("deno") or not shutil.which("ffmpeg"):
        raise RuntimeError("Deno and FFmpeg must be installed and accessible in the system PATH.")

    for dir in ["cache", "downloads"]:
        Path(dir).mkdir(parents=True, exist_ok=True)

    # Ensure cookies dir exists for COOKIES_DATA base64 decoding
    Path("ishu/cookies").mkdir(parents=True, exist_ok=True)
    logger.info("Cache directories updated.")
