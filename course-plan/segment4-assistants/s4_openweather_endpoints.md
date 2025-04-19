# OpenWeatherMap API Documentation
Version: 2.5
Base URL: `api.openweathermap.org/data/2.5`

## Authentication

All API requests require an API key passed as a query parameter:
```
?appid=your_api_key
```

Rate Limits:
- Free Tier: 60 calls/minute
- Pro Tier: 600 calls/minute
- Enterprise: Custom limits

## Core Endpoints

### 1. Current Weather Data
```http
GET /weather
```

Get current weather data for a location.

**Parameters:**
- `q` (string): City name, state code and country code (e.g., "London,UK")
- `lat` (float): Latitude
- `lon` (float): Longitude
- `id` (int): City ID
- `zip` (string): Zip code
- `units` (string): Units of measurement (standard, metric, imperial)
- `lang` (string): Language code

**Example Request:**
```http
GET /weather?q=London,UK&units=metric&appid={API_key}
```

**Example Response:**
```json
{
  "coord": {
    "lon": -0.1257,
    "lat": 51.5085
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 15.45,
    "feels_like": 14.78,
    "temp_min": 13.89,
    "temp_max": 16.67,
    "pressure": 1025,
    "humidity": 71
  },
  "visibility": 10000,
  "wind": {
    "speed": 4.12,
    "deg": 250
  },
  "clouds": {
    "all": 0
  },
  "dt": 1684927461,
  "sys": {
    "type": 2,
    "id": 2075535,
    "country": "GB",
    "sunrise": 1684901830,
    "sunset": 1684958903
  },
  "timezone": 3600,
  "id": 2643743,
  "name": "London",
  "cod": 200
}
```

### 2. 5 Day Weather Forecast
```http
GET /forecast
```

Get 5 day forecast with data every 3 hours.

**Parameters:**
Same as Current Weather Data endpoint

**Example Request:**
```http
GET /forecast?q=London,UK&units=metric&appid={API_key}
```

**Response Format:**
```json
{
  "cod": "200",
  "message": 0,
  "cnt": 40,
  "list": [
    {
      "dt": 1684936800,
      "main": {...},
      "weather": [...],
      "clouds": {...},
      "wind": {...},
      "visibility": 10000,
      "pop": 0,
      "sys": {...},
      "dt_txt": "2023-05-24 15:00:00"
    },
    // Additional time slots...
  ],
  "city": {
    "id": 2643743,
    "name": "London",
    "coord": {...},
    "country": "GB",
    "population": 1000000,
    "timezone": 3600,
    "sunrise": 1684901830,
    "sunset": 1684958903
  }
}
```

### 3. Weather Maps
```http
GET /maps/{layer}/{z}/{x}/{y}
```

Get weather map tiles.

**Layers:**
- `clouds_new`
- `precipitation_new`
- `pressure_new`
- `wind_new`
- `temp_new`

**Parameters:**
- `z` (int): Zoom level (0-18)
- `x` (int): X tile coordinate
- `y` (int): Y tile coordinate

### 4. Air Pollution
```http
GET /air_pollution
```

Get air pollution data.

**Parameters:**
- `lat` (float): Latitude
- `lon` (float): Longitude

**Example Response:**
```json
{
  "coord": {
    "lon": -0.1257,
    "lat": 51.5085
  },
  "list": [
    {
      "main": {
        "aqi": 1
      },
      "components": {
        "co": 201.94,
        "no": 0.89,
        "no2": 4.94,
        "o3": 67.23,
        "so2": 1.07,
        "pm2_5": 4.63,
        "pm10": 7.24,
        "nh3": 1.07
      },
      "dt": 1684927461
    }
  ]
}
```

## Common Parameters

### Units of Measurement

- `standard`: Kelvin (temperature), meter/sec (wind speed)
- `metric`: Celsius, meter/sec
- `imperial`: Fahrenheit, miles/hour

### Language Support

Supported language codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- (and many more...)

### Error Codes

- 200: Success
- 401: Invalid API key
- 404: Location not found
- 429: Too many requests
- 500: Server error

## Best Practices

1. **API Key Security**
   - Never expose API key in client-side code
   - Use environment variables
   - Implement key rotation

2. **Rate Limiting**
   - Implement exponential backoff
   - Cache responses when possible
   - Monitor usage

3. **Error Handling**
   - Handle all error codes
   - Implement retry logic
   - Validate responses

4. **Performance**
   - Use appropriate endpoints
   - Minimize request frequency
   - Implement caching

## Code Examples

### Python Request
```python
import requests
import os

API_KEY = os.getenv('OPENWEATHER_API_KEY')
city = 'London,UK'

response = requests.get(
    'https://api.openweathermap.org/data/2.5/weather',
    params={
        'q': city,
        'units': 'metric',
        'appid': API_KEY
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"Temperature in {city}: {data['main']['temp']}°C")
```

### Error Handling
```python
def get_weather(city):
    try:
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={
                'q': city,
                'units': 'metric',
                'appid': API_KEY
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
```

## Additional Resources

- [Official Documentation](https://openweathermap.org/api)
- [API Status Page](https://status.openweathermap.org)
- [Support Forum](https://openweathermap.org/forum)
- [API Subscription Plans](https://openweathermap.org/price) 