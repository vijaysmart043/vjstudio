"""
Program output recording engine with timestamped file naming and safety guards.
"""

import datetime
import time
from pathlib import Path
from typing import Optional
from app.core.constants import RecordState
from app.core.events import events, EVENT_RECORD_STATE_CHANGED
from app.core.logger import logger
from app.ffmpeg.ffmpeg_manager import ffmpeg_manager
from app.ffmpeg.ffmpeg_process import FFmpegProcess
from app.recording.recording_config import RecordingProfile


class Recorder:
    """Manages recording the live Program output bus to local disk."""

    _instance = None

    def __init__(self) -> None:
        self.state: RecordState = RecordState.STOPPED
        self._process = FFmpegProcess("ProgramRecorder")
        self._profile: Optional[RecordingProfile] = None
        self._active_file: Optional[Path] = None
        self._start_time: float = 0.0

    @classmethod
    def get_instance(cls) -> "Recorder":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def generate_filename(format_ext: str = "mp4") -> str:
        """Generate safe, standard broadcast timestamped filename."""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"VJStudio_{now_str}.{format_ext.lstrip('.')}"

    def start_recording(self, profile: RecordingProfile) -> bool:
        if self.state == RecordState.RECORDING:
            return True

        self._profile = profile
        out_dir = Path(profile.output_dir)
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"Cannot create recordings directory {out_dir}: {e}")
            return False

        filename = self.generate_filename(profile.format)
        self._active_file = out_dir / filename
        self._start_time = time.time()

        # Build FFmpeg recording command if available
        if ffmpeg_manager.ffmpeg_path:
            enc = ffmpeg_manager.get_best_h264_encoder() if profile.encoder == "auto" else profile.encoder
            args = [
                str(ffmpeg_manager.ffmpeg_path),
                "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-pix_fmt", "bgr24",
                "-s", f"{profile.width}x{profile.height}",
                "-r", str(profile.fps),
                "-i", "-",  # pipe input from Program bus
                "-c:v", enc,
                "-b:v", f"{profile.video_bitrate_kbps}k",
                "-pix_fmt", "yuv420p",
                str(self._active_file),
            ]
            self._process.start(args, stdin_pipe=True)

        self.state = RecordState.RECORDING
        events.publish(EVENT_RECORD_STATE_CHANGED, self.state)
        logger.info(f"Recording started -> {self._active_file}")
        return True

    def stop_recording(self) -> None:
        if self.state == RecordState.STOPPED:
            return

        self._process.stop()
        self.state = RecordState.STOPPED
        events.publish(EVENT_RECORD_STATE_CHANGED, self.state)
        logger.info(f"Recording saved to: {self._active_file}")
        self._active_file = None

    @property
    def elapsed_seconds(self) -> float:
        if self.state == RecordState.RECORDING:
            return time.time() - self._start_time
        return 0.0

    @property
    def current_file(self) -> Optional[Path]:
        return self._active_file


recorder = Recorder.get_instance()
