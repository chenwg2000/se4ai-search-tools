# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
source venv/bin/activate
source .env

# Run all tests
python run_tests.py

# Run a single test
python tests/test_tavily.py
python tests/test_serpapi.py
```

## Architecture

This project tests multiple web search API integrations. All tools follow a common pattern:

- `skills/base_search.py` — `BaseSearchTool` (ABC) and `SearchResult` dataclass. All tools must implement `search()` and `_get_api_key_env()`.
- `skills/<tool>_search.py` — Concrete implementations extending `BaseSearchTool`.
- `tests/test_<tool>.py` — Each test file exposes a `run_tests()` function (required by the test runner) and saves results to `outputs/` as timestamped JSON.
- `run_tests.py` — Discovers and runs all `tests/test_*.py` files by calling their `run_tests()` function.

API keys are loaded from `.env` (see `.env.example`). Each tool reads its key via `os.getenv()` using the name returned by `_get_api_key_env()`.

## Tool Status

| Tool | API Key Env | Status |
|------|-------------|--------|
| Tavily | `TAVILY_API_KEY` | Working |
| SerpAPI | `SERPAPI_API_KEY` | Working |
| Baidu | `BAIDU_API_KEY` | SSL timeout in this env |
| Metaso | `METASO_API_KEY` | SSL timeout in this env |
| Kimi | — | Kimi CLI environment only |

## Adding a New Search Tool

1. Create `skills/<name>_search.py` extending `BaseSearchTool`
2. Implement `_get_api_key_env()` and `search()`
3. Create `tests/test_<name>.py` with a `run_tests()` → `bool` function that saves output to `outputs/`
