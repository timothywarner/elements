"""
OpenWeatherMap API Examples
==========================
This module provides examples and utilities for working with the OpenWeatherMap API.
"""

import os
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import logging
from dataclasses import dataclass
from functools import lru_cache
import pandas as pd
import matplotlib.pyplot as plt

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WeatherConfig:
    """Configuration for weather API calls."""
    api_key: str
    base_url: str = "https://api.openweathermap.org/data/2.5"
    units: str = "metric"
    language: str = "en"
    timeout: int = 10

class WeatherAPI:
    """Wrapper class for OpenWeatherMap API."""
    
    def __init__(self, config: WeatherConfig):
        """Initialize with configuration."""
        self.config = config
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make API request with error handling and retries."""
        params['appid'] = self.config.api_key
        params['units'] = self.config.units
        params['lang'] = self.config.language
        
        retries = 3
        for attempt in range(retries):
            try:
                response = self.session.get(
                    f"{self.config.base_url}/{endpoint}",
                    params=params,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    logger.error(f"Failed to fetch data: {str(e)}")
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
    
    @lru_cache(maxsize=100)
    def get_current_weather(self, city: str) -> Dict:
        """Get current weather for a city with caching."""
        return self._make_request('weather', {'q': city})
    
    def get_forecast(self, city: str) -> List[Dict]:
        """Get 5-day weather forecast."""
        data = self._make_request('forecast', {'q': city})
        return data['list']
    
    def get_air_pollution(self, lat: float, lon: float) -> Dict:
        """Get air pollution data for coordinates."""
        return self._make_request('air_pollution', {
            'lat': lat,
            'lon': lon
        })

class WeatherAnalytics:
    """Analytics and data processing for weather data."""
    
    @staticmethod
    def calculate_daily_averages(forecast_data: List[Dict]) -> pd.DataFrame:
        """Calculate daily temperature averages from forecast data."""
        df = pd.DataFrame(forecast_data)
        df['dt'] = pd.to_datetime(df['dt'], unit='s')
        df['temp'] = df['main'].apply(lambda x: x['temp'])
        
        daily_avg = df.groupby(df['dt'].dt.date)['temp'].agg(['mean', 'min', 'max'])
        return daily_avg
    
    @staticmethod
    def plot_temperature_trend(daily_avg: pd.DataFrame, city: str):
        """Plot temperature trends."""
        plt.figure(figsize=(10, 6))
        daily_avg.plot(kind='line', marker='o')
        plt.title(f"Temperature Trend - {city}")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.legend(['Average', 'Minimum', 'Maximum'])
        return plt

class WeatherAlerts:
    """Weather alert system."""
    
    def __init__(self, api: WeatherAPI):
        self.api = api
        self.alert_conditions = []
    
    def add_alert_condition(self, city: str, condition: callable, callback: callable):
        """Add an alert condition with callback."""
        self.alert_conditions.append({
            'city': city,
            'condition': condition,
            'callback': callback
        })
    
    def check_alerts(self):
        """Check all alert conditions."""
        for alert in self.alert_conditions:
            try:
                weather = self.api.get_current_weather(alert['city'])
                if alert['condition'](weather):
                    alert['callback'](weather)
            except Exception as e:
                logger.error(f"Error checking alert for {alert['city']}: {str(e)}")

def example_usage():
    """Example usage of the weather API wrapper."""
    
    # Initialize with configuration
    config = WeatherConfig(
        api_key=os.getenv('OPENWEATHER_API_KEY'),
        units='metric'
    )
    
    api = WeatherAPI(config)
    analytics = WeatherAnalytics()
    alerts = WeatherAlerts(api)
    
    try:
        # Get current weather
        london_weather = api.get_current_weather('London,UK')
        print(f"Current temperature in London: {london_weather['main']['temp']}°C")
        
        # Get forecast and analyze
        forecast = api.get_forecast('London,UK')
        daily_avg = analytics.calculate_daily_averages(forecast)
        print("\nDaily averages:")
        print(daily_avg)
        
        # Plot temperature trend
        plt = analytics.plot_temperature_trend(daily_avg, 'London')
        plt.savefig('temperature_trend.png')
        
        # Setup weather alert
        def high_temp_alert(weather_data: Dict) -> bool:
            return weather_data['main']['temp'] > 30
        
        def alert_callback(weather_data: Dict):
            print(f"High temperature alert: {weather_data['main']['temp']}°C")
        
        alerts.add_alert_condition('London,UK', high_temp_alert, alert_callback)
        alerts.check_alerts()
        
    except Exception as e:
        logger.error(f"Error in example usage: {str(e)}")

class WeatherUtils:
    """Utility functions for weather data."""
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius."""
        return kelvin - 273.15
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def format_weather_summary(weather_data: Dict) -> str:
        """Format weather data as human-readable summary."""
        main = weather_data['main']
        weather = weather_data['weather'][0]
        
        return (
            f"Temperature: {main['temp']}°C\n"
            f"Feels like: {main['feels_like']}°C\n"
            f"Humidity: {main['humidity']}%\n"
            f"Conditions: {weather['description']}\n"
            f"Pressure: {main['pressure']} hPa"
        )
    
    @staticmethod
    def is_daytime(weather_data: Dict) -> bool:
        """Check if it's daytime based on sunrise/sunset."""
        dt = datetime.fromtimestamp(weather_data['dt'])
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset'])
        return sunrise <= dt <= sunset

if __name__ == "__main__":
    example_usage() 