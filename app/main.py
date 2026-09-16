"""
Package main entry point for VJ Studio.
"""

import sys
from app.core.application import VJStudioApplication


def main() -> int:
    app = VJStudioApplication(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
