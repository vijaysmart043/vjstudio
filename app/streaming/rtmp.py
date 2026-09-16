"""
RTMP streaming controller wrapping managed FFmpeg encoder pipeline.
"""

from typing import Optional
from app.core.constants import StreamState
from app.core.events import events, EVENT_STREAM_STATE_CHANGED
from app.core.logger import logger, SensitiveDataFilter
from app.ffmpeg.ffmpeg_manager import ffmpeg_manager
from app.ffmpeg.ffmpeg_process import FFmpegProcess
from app.streaming.stream_config import StreamProfile


class RTMPStreamer:
    """Controls RTMP broadcast stream transmission via FFmpeg."""

    def __init__(self) -> None:
        self.state: StreamState = StreamState.STOPPED
        self._process = FFmpegProcess("RTMPStreamer")
        self._profile: Optional[StreamProfile] = None

    def start(self, profile: StreamProfile) -> bool:
        if self.state == StreamState.LIVE:
            return True

        self._profile = profile
        self.state = StreamState.STARTING
        events.publish(EVENT_STREAM_STATE_CHANGED, self.state)

        target_url = f"{profile.server_url.rstrip('/')}/{profile.stream_key}"
        logger.info(f"Connecting to RTMP destination: {SensitiveDataFilter.sanitize(target_url)}")

        # Build FFmpeg command if FFmpeg available
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
                "-i", "-",  # pipe input
                "-c:v", enc,
                "-b:v", f"{profile.video_bitrate_kbps}k",
                "-maxrate", f"{profile.video_bitrate_kbps}k",
                "-bufsize", f"{profile.video_bitrate_kbps * 2}k",
                "-pix_fmt", "yuv420p",
                "-g", str(profile.fps * profile.keyframe_interval),
                "-f", "flv",
                target_url,
            ]
            self._process.start(args, stdin_pipe=True)

        self.state = StreamState.LIVE
        events.publish(EVENT_STREAM_STATE_CHANGED, self.state)
        logger.info("RTMP stream is now LIVE.")
        return True

    def stop(self) -> None:
        if self.state == StreamState.STOPPED:
            return

        self.state = StreamState.STOPPING
        events.publish(EVENT_STREAM_STATE_CHANGED, self.state)

        self._process.stop()
        self.state = StreamState.STOPPED
        events.publish(EVENT_STREAM_STATE_CHANGED, self.state)
        logger.info("RTMP stream stopped.")
