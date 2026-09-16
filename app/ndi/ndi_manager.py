"""
NDI Manager for discovering, enumerating, and connecting to NDI sources on the local network.
"""

from typing import List, Optional
from app.core.logger import logger

try:
    import NDIlib as ndi
    HAS_NDI = True
except ImportError:
    HAS_NDI = False


class NDIManager:
    """Manages NDI SDK runtime initialization, discovery, and active instances."""

    _instance = None

    def __init__(self) -> None:
        self._initialized = False
        self._find_instance = None
        self._available_sources: List[str] = []
        self._init_sdk()

    @classmethod
    def get_instance(cls) -> "NDIManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _init_sdk(self) -> bool:
        if HAS_NDI:
            try:
                if not ndi.initialize():
                    logger.warning("Failed to initialize NDI SDK.")
                    return False
                self._initialized = True
                logger.info("NDI SDK initialized successfully.")
                return True
            except Exception as e:
                logger.warning(f"Error initializing NDI SDK: {e}")
                return False
        else:
            logger.info("NDI SDK runtime not present in environment; NDI emulation mode active.")
            return False

    @property
    def is_available(self) -> bool:
        return self._initialized and HAS_NDI

    def discover_sources(self) -> List[str]:
        """Discovers NDI transmitters on the local network subnet."""
        if not self.is_available:
            # Provide sample available sources when in simulation/standby
            return ["STUDIO-MAIN (OBS Studio)", "GUEST-LAPTOP (NDI Screen Capture)", "MOBILE-CAM (NDI HX)"]

        sources = []
        try:
            find_create_desc = ndi.FindCreate()
            find = ndi.find_create_v2(find_create_desc)
            if find:
                ndi.find_wait_for_sources(find, 1000)
                raw_sources = ndi.find_get_current_sources(find)
                for s in raw_sources:
                    sources.append(s.ndi_name)
                ndi.find_destroy(find)
        except Exception as e:
            logger.error(f"Error during NDI source discovery: {e}")

        self._available_sources = sources
        return sources


ndi_manager = NDIManager.get_instance()
