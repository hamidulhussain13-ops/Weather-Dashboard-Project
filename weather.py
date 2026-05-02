import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Page Configuration
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin: 10px 0;
        color: white;
    }
    .temp-big {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
    .city-name {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 10px;
    }
    .forecast-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin: 5px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🌤️ Weather Dashboard</div>', unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # City input
    city = st.text_input("🌍 Enter City Name", "London")
    
    # Temperature unit
    unit = st.radio("🌡️ Temperature Unit", ["Celsius (°C)", "Fahrenheit (°F)"])
    
    # Get weather button
    get_weather = st.button("🔍 Get Weather", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📍 Quick Cities")
    
    # Quick city buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("New York", use_container_width=True):
            city = "New York"
            get_weather = True
    with col2:
        if st.button("Tokyo", use_container_width=True):
            city = "Tokyo"
            get_weather = True
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Paris", use_container_width=True):
            city = "Paris"
            get_weather = True
    with col4:
        if st.button("Delhi", use_container_width=True):
            city = "Delhi"
            get_weather = True

# Function to get weather data
def get_weather_data(city_name):
    """Get weather data for a city using Open-Meteo API"""
    try:
        # Step 1: Get coordinates from city name
        geo_url = "https://nominatim.openstreetmap.org/search"
        geo_params = {
            "q": city_name,
            "format": "json",
            "limit": 1
        }
        geo_headers = {'User-Agent': 'WeatherApp/1.0'}
        
        geo_response = requests.get(geo_url, params=geo_params, headers=geo_headers, timeout=10)
        
        if geo_response.status_code != 200 or not geo_response.json():
            return None
        
        location_data = geo_response.json()[0]
        lat = float(location_data["lat"])
        lon = float(location_data["lon"])
        location_name = location_data["display_name"]
        
        # Step 2: Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,is_day",
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "timezone": "auto",
            "forecast_days": 5
        }
        
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        
        if weather_response.status_code != 200:
            return None
        
        weather_data = weather_response.json()
        
        return {
            "city": city_name,
            "location": location_name,
            "lat": lat,
            "lon": lon,
            "current": weather_data["current"],
            "daily": weather_data["daily"]
        }
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Weather condition descriptions
weather_conditions = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Foggy", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy Drizzle", "🌦️"),
    61: ("Light Rain", "🌧️"),
    63: ("Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Light Snow", "❄️"),
    73: ("Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    80: ("Rain Showers", "🌦️"),
    81: ("Heavy Showers", "🌦️"),
    82: ("Violent Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with Hail", "⛈️"),
    99: ("Heavy Thunderstorm", "⛈️")
}

# Main app logic
if get_weather or city:
    with st.spinner(f"🌍 Getting weather for {city}..."):
        weather_data = get_weather_data(city)
        
        if weather_data:
            current = weather_data["current"]
            daily = weather_data["daily"]
            
            # Convert temperature based on unit
            current_temp = current["temperature_2m"]
            if "Fahrenheit" in unit:
                current_temp = (current_temp * 9/5) + 32
                temp_unit = "°F"
            else:
                temp_unit = "°C"
            
            # Get weather condition
            weather_code = current["weather_code"]
            condition, emoji = weather_conditions.get(weather_code, ("Unknown", "❓"))
            
            # Display current weather
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown(f'<div class="weather-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="city-name">{emoji} {weather_data["city"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="temp-big">{current_temp:.1f}{temp_unit}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align: center; font-size: 1.3rem;">{condition}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Current weather details
            st.markdown("### 📊 Current Conditions")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💨 Wind Speed", f"{current['wind_speed_10m']} km/h")
            with col2:
                st.metric("💧 Humidity", f"{current['relative_humidity_2m']}%")
            with col3:
                st.metric("📍 Latitude", f"{weather_data['lat']:.2f}")
            with col4:
                st.metric("📍 Longitude", f"{weather_data['lon']:.2f}")
            
            # 5-Day Forecast
            st.markdown("### 📅 5-Day Forecast")
            
            forecast_cols = st.columns(5)
            for i in range(5):
                with forecast_cols[i]:
                    # Date
                    date_str = daily["time"][i]
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    day_name = date_obj.strftime("%A")[:3]
                    
                    # Temperatures
                    max_temp = daily["temperature_2m_max"][i]
                    min_temp = daily["temperature_2m_min"][i]
                    
                    if "Fahrenheit" in unit:
                        max_temp = (max_temp * 9/5) + 32
                        min_temp = (min_temp * 9/5) + 32
                    
                    # Weather condition
                    daily_code = daily["weather_code"][i]
                    daily_condition, daily_emoji = weather_conditions.get(daily_code, ("", "❓"))
                    
                    # Display forecast card
                    st.markdown(f'<div class="forecast-card">', unsafe_allow_html=True)
                    st.markdown(f"*{day_name}*")
                    st.markdown(f"*{daily_emoji}*")
                    st.markdown(f"*H:* {max_temp:.0f}{temp_unit}")
                    st.markdown(f"*L:* {min_temp:.0f}{temp_unit}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Location Map
            st.markdown("### 🗺️ Location on Map")
            map_data = pd.DataFrame({
                'lat': [weather_data["lat"]],
                'lon': [weather_data["lon"]]
            })
            st.map(map_data, zoom=10)
            
            # Location Details
            with st.expander("📍 View Location Details"):
                st.write(f"*Full Location:* {weather_data['location']}")
                st.write(f"*Coordinates:* {weather_data['lat']:.4f}, {weather_data['lon']:.4f}")
                
        else:
            st.error("❌ Could not fetch weather data. Please check the city name and try again.")
            
            # Show popular cities
            st.markdown("### 🌆 Try These Popular Cities:")
            popular_cols = st.columns(5)
            popular_cities = ["London", "New York", "Tokyo", "Paris", "Sydney"]
            
            for i, pop_city in enumerate(popular_cities):
                with popular_cols[i]:
                    if st.button(pop_city, key=f"pop_{i}"):
                        # This will trigger a rerun with the new city
                        st.experimental_set_query_params(city=pop_city)
                        st.experimental_rerun()

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h2>🌤️ Welcome to Weather Dashboard!</h2>
        <p style="font-size: 1.2rem; color: #666; margin-top: 20px;">
            Get real-time weather information for any city in the world.<br>
            Enter a city name in the sidebar and click "Get Weather" to start!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show sample cities in main area too
    st.markdown("### 🏙️ Quick Start - Click a City:")
    sample_cols = st.columns(5)
    sample_cities = ["London", "New York", "Tokyo", "Paris", "Delhi"]
    
    for i, sample_city in enumerate(sample_cities):
        with sample_cols[i]:
            if st.button(f"📍 {sample_city}", key=f"sample_{i}", use_container_width=True):
                # Store city in session state and rerun
                if 'city' not in st.session_state:
                    st.session_state.city = sample_city
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>🌍 Weather data provided by <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a></p>
        <p>📍 Location data by <a href="https://nominatim.openstreetmap.org/" target="_blank">OpenStreetMap</a></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'city' not in st.session_state:
    st.session_state.city = ""