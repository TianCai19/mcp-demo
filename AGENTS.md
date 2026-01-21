# Repository Guidelines

## Project Structure & Module Organization
- `weather/` hosts the MCP server implementation (`weather.py`) plus learning docs like `CODE_EXPLAINED.md` and `TRANSPORT_EXPLAINED.md`.
- `mcp-client/` contains the interactive client (`client.py`) and test scripts (`test_client.py`, `test_openrouter.py`).
- `docs-site/` is the documentation site source, and `MCP_CLIENTS_SETUP.md` explains client configuration.
- Root docs (`README.md`, `CLAUDE.md`, `mcpClient.md`, `mcpServer.md`) describe usage and architecture.

## Build, Test, and Development Commands
This repo uses `uv` for Python environments.
- Create server env and deps:
  - `cd weather && uv venv && uv add "mcp[cli]" httpx`
- Create client env and deps:
  - `cd mcp-client && uv venv && uv add mcp anthropic python-dotenv requests`
- Run the interactive client:
  - `cd mcp-client && uv run python client.py ../weather/weather.py`
- Run the client test script:
  - `cd mcp-client && uv run python test_client.py ../weather/weather.py`

## Coding Style & Naming Conventions
- Python code uses 4-space indentation and standard PEP 8 conventions.
- Prefer `snake_case` for functions/variables and `CapWords` for classes.
- Keep module names lowercase (e.g., `weather.py`, `client.py`).
- No formatter or linter is configured; keep diffs small and readable.

## Testing Guidelines
- Tests are lightweight scripts in `mcp-client/` (`test_*.py`).
- Name new tests `test_<purpose>.py` and keep them runnable via `uv run python`.
- Focus on real API flows (OpenRouter + MCP). Mocking is optional but document it if added.

## Commit & Pull Request Guidelines
- Commit history uses a conventional pattern like `docs: ...`, `fix: ...`, `chore: ...`.
- Keep commits scoped to one logical change and include a short, descriptive summary.
- PRs should include: purpose, how to run/verify (commands), and any new env/config steps.

## Configuration & Security Notes
- Client requires `mcp-client/.env` with `OPENROUTER_API_KEY=...`.
- Avoid committing real keys or secrets; use example values in docs.
- The server calls the NWS API (`api.weather.gov`), which is US-only.
