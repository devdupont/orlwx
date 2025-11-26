"""Tests for the FastAPI endpoints."""

from collections.abc import AsyncIterator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from orlwx.main import app
from orlwx.models import CurrentWeather, WeatherSummary

MOCK_WEATHER_RESPONSE = {
    "coord": {"lon": -81.3792, "lat": 28.5383},
    "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
    "base": "stations",
    "main": {
        "temp": 75.5,
        "feels_like": 76.2,
        "temp_min": 72.0,
        "temp_max": 78.0,
        "pressure": 1015,
        "humidity": 65,
    },
    "visibility": 10000,
    "wind": {"speed": 5.5, "deg": 180},
    "clouds": {"all": 0},
    "dt": 1700000000,
    "sys": {"type": 2, "id": 2000, "country": "US", "sunrise": 1699960000, "sunset": 1700000000},
    "timezone": -18000,
    "id": 4167147,
    "name": "Orlando",
    "cod": 200,
}


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    """Create an async HTTP client for testing the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient) -> None:
    """Test the health check endpoint."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_get_weather_endpoint(async_client: AsyncClient) -> None:
    """Test the /weather endpoint."""
    mock_weather = CurrentWeather.model_validate(MOCK_WEATHER_RESPONSE)

    with patch("orlwx.main.WeatherService") as mock_service_class:
        mock_service = AsyncMock()
        mock_service.get_current_weather.return_value = mock_weather
        mock_service_class.return_value = mock_service

        response = await async_client.get("/weather")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Orlando"
        assert data["main"]["temp"] == 75.5


@pytest.mark.asyncio
async def test_get_weather_summary_endpoint(async_client: AsyncClient) -> None:
    """Test the /weather/summary endpoint."""
    mock_summary = WeatherSummary(
        location="Orlando",
        temperature=75.5,
        feels_like=76.2,
        description="clear sky",
        humidity=65,
        wind_speed=5.5,
        visibility=10000,
        timestamp=1700000000,
    )

    with patch("orlwx.main.WeatherService") as mock_service_class:
        mock_service = AsyncMock()
        mock_service.get_weather_summary.return_value = mock_summary
        mock_service_class.return_value = mock_service

        response = await async_client.get("/weather/summary")

        assert response.status_code == 200
        data = response.json()
        assert data["location"] == "Orlando"
        assert data["temperature"] == 75.5
        assert data["description"] == "clear sky"


@pytest.mark.asyncio
async def test_get_weather_api_key_error(async_client: AsyncClient) -> None:
    """Test that missing API key returns 500 error."""
    with patch("orlwx.main.WeatherService") as mock_service_class:
        mock_service = AsyncMock()
        mock_service.get_current_weather.side_effect = ValueError("API key is not configured")
        mock_service_class.return_value = mock_service

        response = await async_client.get("/weather")

        assert response.status_code == 500
        assert "API key is not configured" in response.json()["detail"]
