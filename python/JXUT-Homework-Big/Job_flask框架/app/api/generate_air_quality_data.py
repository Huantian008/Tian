from __future__ import annotations

import json
from pathlib import Path

from api.air_quality import generate_dashboard


def main() -> None:
    api_dir = Path(__file__).resolve().parent
    output = api_dir / "data" / "air_quality_dashboard.json"
    dashboard = generate_dashboard(
        start="2026-04-01",
        end="2026-04-07",
        cache_dir=api_dir / "data" / "raw",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
