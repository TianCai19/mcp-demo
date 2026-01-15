# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a complete MCP (Model Context Protocol) demo project showcasing a weather service system with three main components:

1. **MCP Server** (`weather/`) - Provides weather tools using FastMCP
2. **MCP Client** (`mcp-client/`) - Python client that connects to MCP Server
3. **Documentation Site** (`docs-site/`) - Astro + Starlight documentation site

## Development Commands

### MCP Server (weather/)
```bash
cd weather
uv venv                    # Create virtual environment
uv add "mcp[cli]" httpx   # Install dependencies
uv run weather.py          # Run the server
```

### MCP Client (mcp-client/)
```bash
cd mcp-client
uv venv                    # Create virtual environment
uv add mcp anthropic python-dotenv requests  # Install dependencies

# Interactive client
uv run python client.py ../weather/weather.py

# Automated test
uv run python test_client.py ../weather/weather.py
```

### Documentation Site (docs-site/)
```bash
cd docs-site
npm install                # Install dependencies
npm run dev                # Start dev server (localhost:4321)
npm run build              # Build for production
./sync-docs.sh             # Sync docs from main project
```

### Vercel Deployment
```bash
# From project root
vercel --prod --yes        # Deploy to production

# From docs-site
vercel --prod --yes        # Deploy docs site only
```

## Architecture

### MCP Communication Flow
```
User Query → MCP Client (Claude 3.5 via OpenRouter)
           → MCP Server (stdio transport: stdin/stdout)
           → NWS API (weather data)
           → Client → User (natural language response)
```

### Key Components

**MCP Server** (`weather/weather.py`)
- Uses `FastMCP` to register tools via `@mcp.tool()` decorator
- Two tools: `get_alerts(state)` and `get_forecast(latitude, longitude)`
- Communicates via stdio (`transport="stdio"`)
- **Important**: Do not use `print()` in server code - it breaks MCP communication. Use `logging` instead.

**MCP Client** (`mcp-client/client.py`)
- Connects to server via `stdio_client()` and `StdioServerParameters`
- Uses OpenRouter API (base URL: `https://openrouter.ai/api/v1`)
- Model: `anthropic/claude-3.5-sonnet`
- Converts MCP tool format to OpenAI-compatible format for the API

**Documentation** (`docs-site/`)
- Astro 5.6.1 + Starlight 0.37.2
- Static output (`output: 'static'`)
- Syncs documentation from main project via `sync-docs.sh`
- All MD files need frontmatter with `title` and `description`

## Configuration

### MCP Server Configuration
Servers are configured in JSON format for various clients (Cherry Studio, Claude Desktop, etc.):

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["--directory", "/path/to/weather", "run", "weather.py"]
    }
  }
}
```

**Key points**:
- `command` is the executable (uv, python, node, npx)
- `args` is an array of command-line arguments
- Always use absolute paths for reliability

### Environment Variables
- **mcp-client/.env**: `OPENROUTER_API_KEY` (required)
- Add `.env` to `.gitignore` (already configured)

## Learning Resources

The codebase includes extensive educational materials:

- `weather/CODE_EXPLAINED.md` - Line-by-line code analysis
- `weather/TRANSPORT_EXPLAINED.md` - stdio transport deep dive
- `weather/weather_commented.py` - Code with detailed Chinese comments
- `MCP_CONFIG_EXPLAINED.md` - JSON configuration breakdown
- `MCP_CLIENTS_SETUP.md` - Integration guide for various AI clients

## Important Constraints

### MCP Server Development
- **Never use `print()`** - it corrupts stdio communication
- Use `logging.info()` or `logging.error()` instead
- All tool functions must be async when using async operations
- Use `@mcp.tool()` decorator to register functions

### Python Version
- Requires Python 3.10+
- Uses `uv` package manager (not pip)

### Documentation Site
- All MD files require frontmatter: `title` and `description`
- Frontmatter must be at the very top of the file
- Build output: `docs-site/dist/`

## Deployment Workflow

1. **MCP Server/Client**: Deployed locally, not to cloud
2. **Documentation Site**: Deployed to Vercel via GitHub integration
3. **Vercel Configuration**: `vercel.json` at project root specifies docs-site build

## File Structure Notes

- `.vercel` directory is ignored (auto-generated)
- Virtual environments (`.venv`) are excluded
- Test files (`test_*.py`, `*_test.py`) are excluded
- Documentation sync: `docs-site/sync-docs.sh` copies main project docs to docs-site
