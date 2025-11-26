# orlwx

Orlando weather REST API and MCP endpoints using FastAPI-MCP.

## Features

- **REST API**: Get current weather data for Orlando via HTTP endpoints
- **MCP Endpoints**: Model Context Protocol support via FastAPI-MCP
- **OpenWeatherMap Integration**: Real-time weather data from OpenWeatherMap API

## Requirements

- Python 3.14+
- [Hatch](https://hatch.pypa.io/) for project management
- OpenWeatherMap API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/devdupont/orlwx.git
cd orlwx
```

2. Create a `.env` file with your OpenWeatherMap API key:

```bash
cp .env.example .env
# Edit .env and add your API key
```

3. Install dependencies with Hatch:

```bash
hatch env create
```

## Usage

### Development Server

```bash
hatch run dev
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- `GET /health` - Health check endpoint
- `GET /weather` - Full current weather data for Orlando
- `GET /weather/summary` - Simplified weather summary

### MCP Endpoints

The MCP server is mounted at `/mcp` and exposes the same endpoints for Model Context Protocol clients.

## Development

### Running Tests

```bash
hatch test
```

### Formatting

```bash
hatch fmt
```

### Type Checking

```bash
hatch run types:check
```

## Docker

Build and run with Docker:

```bash
docker build -t orlwx .
docker run -p 8000:8000 -e OPENWEATHERMAP_API_KEY=your_key orlwx
```

## License

MIT License - see [LICENSE](LICENSE) for details.