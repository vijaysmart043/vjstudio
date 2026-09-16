#!/usr/bin/env python3
"""
VJ Studio — Professional Live Video Production & Streaming Application.
Main executable startup script.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.application import VJStudioApplication


def main() -> int:
    app = VJStudioApplication(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
