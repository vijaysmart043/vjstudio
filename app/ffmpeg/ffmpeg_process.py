"""
Subprocess lifecycle manager for FFmpeg instances (recording, streaming).
"""

import os
import subprocess
from typing import List, Optional
from app.core.logger import logger, SensitiveDataFilter


class FFmpegProcess:
    """Manages an active FFmpeg streaming or recording subprocess."""

    def __init__(self, name: str = "FFmpegProcess") -> None:
        self.name = name
        self.process: Optional[subprocess.Popen] = None

    def start(self, args: List[str], stdin_pipe: bool = True) -> bool:
        """Start FFmpeg process with given arguments."""
        if self.is_running():
            logger.warning(f"Process {self.name} already running.")
            return False

        sanitized_cmd = " ".join(args)
        logger.info(f"Starting {self.name}: {SensitiveDataFilter.sanitize(sanitized_cmd)}")

        try:
            stdin_mode = subprocess.PIPE if stdin_pipe else None
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            self.process = subprocess.Popen(
                args,
                stdin=stdin_mode,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=creation_flags,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to start {self.name}: {e}")
            self.process = None
            return False

    def is_running(self) -> bool:
        if self.process is None:
            return False
        return self.process.poll() is None

    def stop(self, timeout_sec: float = 3.0) -> None:
        """Safely terminate FFmpeg subprocess."""
        if not self.is_running() or not self.process:
            return

        try:
            # Send 'q' to FFmpeg stdin to request clean quit
            if self.process.stdin:
                try:
                    self.process.stdin.write(b"q")
                    self.process.stdin.flush()
                except Exception:
                    pass
            self.process.wait(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            logger.warning(f"{self.name} did not stop gracefully, terminating.")
            self.process.terminate()
            try:
                self.process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                self.process.kill()
        finally:
            self.process = None
            logger.info(f"{self.name} stopped.")
