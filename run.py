import json
import os
import webbrowser
from pathlib import Path

PRICING = {
    "Claude Sonnet 4.6": 3.00 / 1_000_000,
    "Claude Opus 4.6": 5.00 / 1_000_000,
    "Gemini 2.5 Pro": 1.25 / 1_000_000,
    "GPT-5 (latest)": 1.25 / 1_000_000,
}

def load_data():
    savings_file = Path.home() / ".code-index" / "_savings.json"
    data = {
        "total_tokens_saved": 0,
        "history": {}
    }

    if savings_file.exists():
        try:
            with open(savings_file, "r") as f:
                saved = json.load(f)
                data.update(saved)
        except Exception as e:
            print(f"Error loading savings file: {e}")

    # Calculate costs avoided for the UI
    costs = {}
    for model, rate in PRICING.items():
        costs[model] = round(data["total_tokens_saved"] * rate, 2)

    data["costs_avoided"] = costs
    return data

def main():
    dashboard_dir = Path(__file__).parent.absolute()
    data = load_data()

    # Write the data.js file
    data_js_path = dashboard_dir / "data.js"
    data_js_content = f"window.JCodeMunchData = {json.dumps(data)};\n"
    with open(data_js_path, "w") as f:
        f.write(data_js_content)

    # Open the index.html file in the default browser
    index_path = dashboard_dir / "index.html"
    print(f"Opening JCodeMunch Dashboard from {index_path}...")
    webbrowser.open(f"file://{index_path}")

if __name__ == "__main__":
    main()
