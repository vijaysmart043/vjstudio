"""
Automated unit and integration test for the Canonical ProgramOutput pipeline,
multi-consumer dispatch (Recording, RTMP, SRT, NDI, Virtual Cam), and frame broadcast.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.media.camera import CameraSource
from app.media.frame import VideoFrame
from app.media.ndi_source import NDISource
from app.media.network_stream_source import NetworkStreamSource
from app.media.screen_capture import ScreenCaptureSource
from app.production.input_manager import input_manager
from app.production.program_output import ProgramOutput, program_output


def test_canonical_program_pipeline():
    # 1. Register sources
    cam = CameraSource(name="Studio Cam 1", device_index=0)
    ndi = NDISource(name="NDI Remote", source_name="REMOTE-STUDIO")
    stream = NetworkStreamSource(name="SRT Guest", stream_url="srt://127.0.0.1:9000")

    input_manager.add_source(cam)
    input_manager.add_source(ndi)
    input_manager.add_source(stream)

    # 2. Air Camera on Program pipeline
    assert program_output.set_source(cam.id) is True
    assert program_output.current_source_id == cam.id
    assert program_output.current_source.name == "Studio Cam 1"

    # 3. Test downstream consumer registration
    received_frames = []

    def test_consumer(frame: VideoFrame):
        received_frames.append(frame)

    program_output.register_consumer(test_consumer)

    # 4. Trigger frame pull from Program pipeline
    frame = program_output.get_frame()
    # In headless testing without opencv/camera, frame is either valid or simulated VideoFrame
    assert len(received_frames) == 1
    assert received_frames[0] == frame

    # 5. Test unregister consumer
    program_output.unregister_consumer(test_consumer)
    program_output.get_frame()
    assert len(received_frames) == 1  # count should not increase

    # 6. Test NDI & Virtual Cam flags
    program_output.set_ndi_output_enabled(True)
    assert program_output.is_ndi_output_enabled is True
    program_output.set_virtual_camera_enabled(True)
    assert program_output.is_virtual_camera_enabled is True

    # 7. Switch Program to NDI source
    program_output.set_source(ndi.id)
    assert program_output.current_source_id == ndi.id


if __name__ == "__main__":
    test_canonical_program_pipeline()
    print("test_program_pipeline passed!")
