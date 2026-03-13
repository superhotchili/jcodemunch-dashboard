import json
import os
import platform
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

PRICING = {
    "Claude Opus 4.6": 5.00 / 1_000_000,
    "Claude Sonnet 4.6": 3.00 / 1_000_000,
    "Gemini 2.5 Pro": 1.25 / 1_000_000,
    "GPT-5 (latest)": 1.25 / 1_000_000,
}

CLIENT_LABELS = {
    "claude": "Claude Code",
    "codex": "Codex CLI",
    "gemini": "Gemini CLI",
    "vscode": "VS Code",
    "unknown": "Other / Untagged",
}


def load_data():
    savings_file = Path.home() / ".code-index" / "_savings.json"
    data = {
        "total_tokens_saved": 0,
        "history": {},
        "by_client": {},
    }

    if savings_file.exists():
        try:
            with open(savings_file, "r") as f:
                saved = json.load(f)
                data.update(saved)
        except Exception as e:
            print(f"Error loading savings file: {e}")

    # Cost avoidance per model
    costs = {}
    for model, rate in PRICING.items():
        costs[model] = round(data["total_tokens_saved"] * rate, 4)
    data["costs_avoided"] = costs

    # Per-client enrichment
    clients = []
    for key, info in data.get("by_client", {}).items():
        tokens = info.get("total_tokens_saved", 0)
        clients.append({
            "id": key,
            "label": CLIENT_LABELS.get(key, key),
            "tokens": tokens,
            "cost_opus": round(tokens * PRICING["Claude Opus 4.6"], 4),
            "cost_sonnet": round(tokens * PRICING["Claude Sonnet 4.6"], 4),
            "history": info.get("history", {}),
        })
    clients.sort(key=lambda c: c["tokens"], reverse=True)
    data["clients"] = clients

    # Summary stats
    history = data.get("history", {})
    days_active = len(history)
    if days_active > 0:
        avg_daily = data["total_tokens_saved"] / days_active
        peak_day = max(history, key=history.get) if history else None
        peak_tokens = history.get(peak_day, 0) if peak_day else 0
    else:
        avg_daily = 0
        peak_day = None
        peak_tokens = 0

    data["stats"] = {
        "days_active": days_active,
        "avg_daily_tokens": round(avg_daily),
        "peak_day": peak_day,
        "peak_tokens": peak_tokens,
        "active_clients": sum(1 for c in clients if c["tokens"] > 0),
        "total_clients": len(clients),
    }

    # Machine info
    data["machine"] = {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    return data


def main():
    dashboard_dir = Path(__file__).parent.absolute()
    data = load_data()

    data_js_path = dashboard_dir / "data.js"
    data_js_content = f"window.JCodeMunchData = {json.dumps(data, indent=2)};\n"
    with open(data_js_path, "w") as f:
        f.write(data_js_content)

    index_path = dashboard_dir / "index.html"
    print(f"Opening jCodeMunch Executive Dashboard from {index_path}...")
    print(f"  Total tokens saved: {data['total_tokens_saved']:,}")
    print(f"  Opus cost avoided:  ${data['costs_avoided']['Claude Opus 4.6']:.2f}")
    print(f"  Active days:        {data['stats']['days_active']}")
    print(f"  Active clients:     {data['stats']['active_clients']}/{data['stats']['total_clients']}")
    webbrowser.open(f"file://{index_path}")


if __name__ == "__main__":
    main()
