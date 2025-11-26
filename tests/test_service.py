"""Tests for the weather service."""

import pytest
from pytest_httpx import HTTPXMock

from orlwx.models import CurrentWeather, WeatherSummary
from orlwx.service import WeatherService

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


@pytest.mark.asyncio
async def test_get_current_weather(httpx_mock: HTTPXMock) -> None:
    """Test fetching current weather data."""
    httpx_mock.add_response(json=MOCK_WEATHER_RESPONSE)

    service = WeatherService(api_key="test_api_key")
    weather = await service.get_current_weather()

    assert isinstance(weather, CurrentWeather)
    assert weather.name == "Orlando"
    assert weather.main.temp == 75.5
    assert weather.main.humidity == 65
    assert weather.weather[0].description == "clear sky"


@pytest.mark.asyncio
async def test_get_weather_summary(httpx_mock: HTTPXMock) -> None:
    """Test fetching weather summary."""
    httpx_mock.add_response(json=MOCK_WEATHER_RESPONSE)

    service = WeatherService(api_key="test_api_key")
    summary = await service.get_weather_summary()

    assert isinstance(summary, WeatherSummary)
    assert summary.location == "Orlando"
    assert summary.temperature == 75.5
    assert summary.description == "clear sky"
    assert summary.humidity == 65


@pytest.mark.asyncio
async def test_missing_api_key() -> None:
    """Test that missing API key raises ValueError."""
    service = WeatherService(api_key="")

    with pytest.raises(ValueError, match="OpenWeatherMap API key is not configured"):
        await service.get_current_weather()
