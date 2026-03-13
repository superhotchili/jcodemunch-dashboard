# jCodeMunch Savings Dashboard

A local HTML+Chart.js dashboard that visualizes token savings from [jcodemunch-mcp](https://pypi.org/project/jcodemunch-mcp/) — the code-indexing MCP server that returns pre-indexed, token-efficient summaries instead of full file contents.

## Quick Start

```bash
# Install the data source (if not already installed)
pipx install jcodemunch-mcp

# Generate data and open the dashboard
python3 run.py
```

## How It Works

1. **jcodemunch-mcp** tracks token savings in `~/.code-index/_savings.json` as you use its MCP tools
2. **`run.py`** reads that file, calculates cost avoidance at current model pricing, and writes `data.js`
3. **`index.html`** loads `data.js` and renders the dashboard with Tailwind CSS + Chart.js

## Files

| File | Purpose |
|---|---|
| `index.html` | Dashboard UI (Tailwind CSS + Chart.js, standalone) |
| `run.py` | Data generator — reads `_savings.json`, writes `data.js`, opens browser |
| `data.js` | Generated at runtime (gitignored) |
| `.gitignore` | Excludes `data.js` and `_savings.json` |

## Cost Models

The dashboard shows avoided costs for:
- Claude Opus 4.6 ($5.00/MTok input)
- Claude Sonnet 4.6 ($3.00/MTok input)
- Gemini 2.5 Pro ($1.25/MTok input)
- GPT-5 ($1.25/MTok input)

## Data Location

Token savings are stored per-machine at `~/.code-index/_savings.json`. No cross-machine sync — each machine tracks its own usage independently.
