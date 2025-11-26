"""Main FastAPI application with REST and MCP endpoints."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from httpx import HTTPStatusError

from orlwx.models import CurrentWeather, WeatherSummary
from orlwx.service import WeatherService

app = FastAPI(
    title="Orlando Weather API",
    description="REST API and MCP endpoints for Orlando weather data",
    version="0.1.0",
)


@app.get("/weather", response_model=CurrentWeather)
async def get_weather() -> CurrentWeather:
    """Get current weather data for Orlando.

    Returns:
        Full current weather data from OpenWeatherMap.
    """
    service = WeatherService()
    try:
        return await service.get_current_weather()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error") from e


@app.get("/weather/summary", response_model=WeatherSummary)
async def get_weather_summary() -> WeatherSummary:
    """Get a simplified weather summary for Orlando.

    Returns:
        Simplified weather summary with key information.
    """
    service = WeatherService()
    try:
        return await service.get_weather_summary()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error") from e


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status message indicating the API is running.
    """
    return {"status": "healthy"}


# Initialize MCP server with the FastAPI app
mcp = FastApiMCP(app)
mcp.mount_http()
