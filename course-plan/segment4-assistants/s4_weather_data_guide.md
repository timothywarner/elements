# Weather Data Guide

## Understanding Weather Data

### 1. Temperature
- **Main Temperature**: Current temperature
- **Feels Like**: Perceived temperature based on:
  - Humidity
  - Wind speed
  - Solar radiation
- **Min/Max**: Temperature range
- **Units**:
  - Kelvin (K): Standard
  - Celsius (°C): Metric
  - Fahrenheit (°F): Imperial

### 2. Atmospheric Pressure
- **Pressure**: Atmospheric pressure at sea level
- **Units**: 
  - hPa (hectopascals)
  - mb (millibars) - equivalent to hPa
- **Normal Range**: 970-1050 hPa
- **Interpretation**:
  - High pressure (>1013 hPa): Generally clear weather
  - Low pressure (<1013 hPa): Potential precipitation

### 3. Humidity
- **Relative Humidity**: Water vapor percentage
- **Range**: 0-100%
- **Comfort Levels**:
  - 30-50%: Comfortable
  - >60%: Humid
  - <30%: Dry

### 4. Wind
- **Speed**:
  - m/s (meters per second)
  - mph (miles per hour)
  - km/h (kilometers per hour)
- **Direction**: Degrees (meteorological)
  - 0° or 360°: North
  - 90°: East
  - 180°: South
  - 270°: West

### 5. Clouds
- **Coverage**: Percentage (0-100%)
- **Types**:
  - Clear: 0-10%
  - Few: 11-25%
  - Scattered: 26-50%
  - Broken: 51-84%
  - Overcast: 85-100%

### 6. Precipitation
- **Rain Volume**: mm (millimeters)
- **Probability**: Percentage
- **Types**:
  - Rain
  - Snow
  - Drizzle
  - Thunderstorm

## Data Analysis

### 1. Basic Calculations

#### Temperature Conversions
```python
def kelvin_to_celsius(k):
    return k - 273.15

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9
```

#### Wind Chill
```python
def wind_chill(temp_c, wind_speed_mps):
    wind_kph = wind_speed_mps * 3.6
    return 13.12 + 0.6215 * temp_c - 11.37 * wind_kph**0.16 + 0.3965 * temp_c * wind_kph**0.16
```

#### Heat Index
```python
def heat_index(temp_c, humidity):
    temp_f = celsius_to_fahrenheit(temp_c)
    hi = 0.5 * (temp_f + 61 + (temp_f - 68) * 1.2 + humidity * 0.094)
    return fahrenheit_to_celsius(hi)
```

### 2. Statistical Analysis

#### Daily Statistics
```python
def calculate_daily_stats(temperatures):
    return {
        'mean': sum(temperatures) / len(temperatures),
        'min': min(temperatures),
        'max': max(temperatures),
        'range': max(temperatures) - min(temperatures)
    }
```

#### Moving Averages
```python
def moving_average(data, window=3):
    return [sum(data[i:i+window])/window 
            for i in range(len(data)-window+1)]
```

## Data Visualization

### 1. Temperature Trends
```python
import matplotlib.pyplot as plt

def plot_temperature_trend(dates, temps):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, temps, marker='o')
    plt.title('Temperature Trend')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.show()
```

### 2. Wind Rose
```python
def plot_wind_rose(directions, speeds):
    # Using windrose package
    from windrose import WindroseAxes
    ax = WindroseAxes.from_ax()
    ax.bar(directions, speeds, normed=True, opening=0.8)
    ax.set_legend()
```

## Common Weather Patterns

### 1. High Pressure Systems
- Clear skies
- Light winds
- Stable conditions
- Summer: Hot and dry
- Winter: Cold and clear

### 2. Low Pressure Systems
- Cloudy conditions
- Stronger winds
- Potential precipitation
- More variable weather

### 3. Frontal Systems
- **Warm Front**:
  - Gradual temperature rise
  - Light, steady precipitation
  - Increasing humidity

- **Cold Front**:
  - Sharp temperature drop
  - Heavy, brief precipitation
  - Decreasing humidity

## Weather Alerts

### 1. Temperature Alerts
```python
def check_temperature_alerts(temp):
    alerts = []
    if temp > 35:
        alerts.append("Extreme heat warning")
    elif temp < 0:
        alerts.append("Freezing conditions")
    return alerts
```

### 2. Severe Weather
- **Thunderstorm Conditions**:
  - High humidity
  - Unstable air
  - Strong temperature gradients

- **Winter Storm Conditions**:
  - Temperature near freezing
  - High humidity
  - Low pressure system

## Best Practices

### 1. Data Collection
- Regular intervals
- Consistent units
- Quality checks
- Error handling

### 2. Data Storage
- Structured format
- Timestamp inclusion
- Backup systems
- Data validation

### 3. Analysis
- Handle missing data
- Account for seasonality
- Consider local factors
- Validate results

### 4. Visualization
- Clear labeling
- Appropriate scales
- Color accessibility
- Interactive elements

## Additional Resources
- [World Meteorological Organization](https://www.wmo.int)
- [National Weather Service](https://www.weather.gov)
- [MetPy Documentation](https://unidata.github.io/MetPy)
- [Climate Data Guide](https://climatedataguide.ucar.edu) 