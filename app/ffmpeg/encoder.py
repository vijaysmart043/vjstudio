"""
Hardware and software video/audio encoder profiles and detector.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class EncoderType(str, Enum):
    CPU_X264 = "libx264"
    NVIDIA_NVENC = "h264_nvenc"
    INTEL_QSV = "h264_qsv"
    AMD_AMF = "h264_amf"
    APPLE_VIDEOTOOLBOX = "h264_videotoolbox"
    AAC = "aac"


@dataclass
class EncoderCapability:
    name: str
    codec: str
    is_hardware: bool
    description: str
    available: bool = False


DEFAULT_ENCODERS = [
    EncoderCapability("NVIDIA NVENC (H.264)", EncoderType.NVIDIA_NVENC.value, True, "NVIDIA GPU Hardware Encoder"),
    EncoderCapability("Intel QuickSync (H.264)", EncoderType.INTEL_QSV.value, True, "Intel iGPU Hardware Encoder"),
    EncoderCapability("AMD AMF (H.264)", EncoderType.AMD_AMF.value, True, "AMD Radeon GPU Hardware Encoder"),
    EncoderCapability("x264 (Software CPU)", EncoderType.CPU_X264.value, False, "High-Quality Software CPU Encoder"),
]
