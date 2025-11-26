"""Pydantic models for weather data."""

from __future__ import annotations

from pydantic import BaseModel


class WeatherCondition(BaseModel):
    """Weather condition details."""

    id: int
    main: str
    description: str
    icon: str


class MainWeather(BaseModel):
    """Main weather measurements."""

    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int | None = None
    grnd_level: int | None = None


class Wind(BaseModel):
    """Wind measurements."""

    speed: float
    deg: int
    gust: float | None = None


class Clouds(BaseModel):
    """Cloud coverage data."""

    all: int


class Sys(BaseModel):
    """System data including sunrise/sunset."""

    type: int | None = None
    id: int | None = None
    country: str
    sunrise: int
    sunset: int


class Coord(BaseModel):
    """Coordinate data."""

    lon: float
    lat: float


class CurrentWeather(BaseModel):
    """Current weather response from OpenWeatherMap."""

    coord: Coord
    weather: list[WeatherCondition]
    base: str
    main: MainWeather
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int


class WeatherSummary(BaseModel):
    """Simplified weather summary for Orlando."""

    location: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    wind_speed: float
    visibility: int
    timestamp: int
