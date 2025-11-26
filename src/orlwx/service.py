"""OpenWeatherMap API service."""

from __future__ import annotations

import httpx

from orlwx.config import settings
from orlwx.models import CurrentWeather, WeatherSummary

OPENWEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize the weather service.

        Args:
            api_key: OpenWeatherMap API key. Defaults to settings value.
        """
        self.api_key = api_key or settings.openweathermap_api_key
        self.lat = settings.orlando_lat
        self.lon = settings.orlando_lon

    async def get_current_weather(self) -> CurrentWeather:
        """Fetch current weather data for Orlando.

        Returns:
            CurrentWeather model with full weather data.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
            ValueError: If API key is not configured.
        """
        if not self.api_key:
            msg = "OpenWeatherMap API key is not configured"
            raise ValueError(msg)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPENWEATHERMAP_BASE_URL}/weather",
                params={
                    "lat": self.lat,
                    "lon": self.lon,
                    "appid": self.api_key,
                    "units": "imperial",
                },
            )
            response.raise_for_status()
            return CurrentWeather.model_validate(response.json())

    async def get_weather_summary(self) -> WeatherSummary:
        """Fetch a simplified weather summary for Orlando.

        Returns:
            WeatherSummary with key weather information.
        """
        weather = await self.get_current_weather()
        return WeatherSummary(
            location=weather.name,
            temperature=weather.main.temp,
            feels_like=weather.main.feels_like,
            description=weather.weather[0].description if weather.weather else "",
            humidity=weather.main.humidity,
            wind_speed=weather.wind.speed,
            visibility=weather.visibility,
            timestamp=weather.dt,
        )
