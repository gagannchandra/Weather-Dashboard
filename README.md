# Weather Dashboard

A Python-based desktop application built with Tkinter to display real-time weather data and a 5-day temperature forecast for any city using the OpenWeatherMap API. It includes an auto-location feature via IP geolocation and a clean, responsive UI.

## Features

- **Current Weather**: Displays temperature, humidity, weather description, and an icon.
- **5-Day Forecast**: Visualizes daily noon temperatures in a Matplotlib chart.
- **City Search**: Input any city name to fetch its weather data.
- **Auto Location**: Detects user's city based on IP and loads weather automatically.
- **Responsive Design**: Weather icon scales with window size.
- **Error Handling**: Shows user-friendly messages for API or network issues.

## Requirements

- Python 3.6 or higher
- Required packages (listed in `requirements.txt`):
  - `requests` (for API requests)
  - `Pillow` (for image processing)
  - `matplotlib` (for forecast charts)
  - `tkinter` (included with Python for GUI)

## Installation

1. Clone or download the repository/script.
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:

   ```
   python weather_dashboard.py
   ```

   (Replace `weather_dashboard.py` with your script's filename.)

2. On launch, the app auto-detects your city and displays its weather.

3. To search manually:

   - Enter a city (e.g., "Tokyo") in the input field and click "🔍 Search".
   - Click "📍 Auto" to refresh weather for your detected location.

4. Resize the window to adjust the weather icon dynamically.

5. The forecast chart plots temperatures at local noon for the next 5 days.

## API Usage

- **Weather Data**: Fetched from `https://api.openweathermap.org/data/2.5/weather`.
- **Forecast Data**: Uses `https://api.openweathermap.org/data/2.5/forecast` (3-hour data, filtered to noon).
- **Location**: Uses `https://ipinfo.io/json` for IP-based city detection (no key required).
- **Icons**: Retrieved from OpenWeatherMap's icon server.

Note: API calls include timeouts for reliability. The free OpenWeatherMap plan limits to 60 calls/minute.

## Troubleshooting

- **Invalid API Key**: Verify your OpenWeatherMap key is correct and active.
- **Network Issues**: Check your internet; errors are displayed in pop-ups.
- **Empty Forecast**: Retry if the API returns no data (rare).
- **Chart Issues**: Ensure `matplotlib` is installed (`pip install matplotlib`).
- **Location Failure**: Use manual city entry if auto-detection fails.

## Limitations

- Supports only metric units (°C).
- Forecast selects the 3-hour data point closest to local noon.
- Icon resizing avoids excessive API calls, so it may not update on every resize.
- Tested on Python 3.12 across Windows, macOS, and Linux; Tkinter behavior may vary.

## License

MIT License. Free to use, modify, and distribute.
