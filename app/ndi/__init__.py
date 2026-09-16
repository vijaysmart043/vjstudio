"""
NDI (Network Device Interface) integration package for VJ Studio.
Provides NDI source discovery, video/audio ingestion, and NDI Program broadcast output.
"""

from app.ndi.ndi_manager import NDIManager, ndi_manager
from app.ndi.ndi_source import NDISource
from app.ndi.ndi_output import NDIOutput, ndi_output

__all__ = ["NDIManager", "ndi_manager", "NDISource", "NDIOutput", "ndi_output"]
