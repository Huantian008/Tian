from __future__ import annotations

import json
from pathlib import Path

from api.air_quality import generate_dashboard, latest_available_range


def main() -> None:
    api_dir = Path(__file__).resolve().parent
    output = api_dir / "data" / "air_quality_dashboard.json"
    date_range = latest_available_range(days=7)
    dashboard = generate_dashboard(
        start=date_range.start,
        end=date_range.end,
        cache_dir=api_dir / "data" / "raw",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {output}")
    print(f"Date range: {date_range.start} 至 {date_range.end}")


if __name__ == "__main__":
    main()
