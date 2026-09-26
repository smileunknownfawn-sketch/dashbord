"""Windows launcher: accepts installer-selected data directory before opening UI."""
from __future__ import annotations

import sys
from pathlib import Path


def _data_folder_argument() -> Path | None:
    for arg in sys.argv[1:]:
        if arg.lower().startswith("/datafolder="):
            raw = arg.split("=", 1)[1].strip().strip('"')
            if raw:
                return Path(raw).expanduser().resolve()
    return None


def main() -> None:
    root = _data_folder_argument()
    if root:
        root.mkdir(parents=True, exist_ok=True)
        (Path.home() / ".vom_dashboard_root").write_text(str(root), encoding="utf-8")
    from desktop_release import main as app_main
    app_main()


if __name__ == "__main__":
    main()
