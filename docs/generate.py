"""Generate API documentation from docstrings using pdoc.

Usage:
    python docs/generate.py          # Build static HTML into docs/api/
    python docs/generate.py --live   # Start live server on http://localhost:8080
"""

import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Setup Django before importing any project module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

import pdoc  # noqa: E402
import pdoc.web  # noqa: E402

MODULES = [
    "domain.entities.assignment",
    "domain.entities.indicator",
    "domain.entities.trend",
    "domain.entities.wellness_entry",
    "domain.ports.assignment_repository",
    "domain.ports.indicator_repository",
    "domain.ports.wellness_entry_repository",
    "domain.services.tracking_service",
    "infrastructure.app",
]

OUTPUT_DIR = project_root / "docs" / "api"


def build():
    """Generate static HTML documentation into docs/api/."""
    pdoc.pdoc(*MODULES, output_directory=OUTPUT_DIR)
    print(f"Documentation generated in {OUTPUT_DIR}")


def live(host="localhost", port=8080):
    """Start a live-reloading documentation server."""
    httpd = pdoc.web.DocServer((host, port), MODULES)
    print(f"Live docs at http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


def main():
    """Dispatch to build or live mode based on CLI arguments."""
    if "--live" in sys.argv:
        live()
    else:
        build()


if __name__ == "__main__":
    main()
