import streamlit as st
import requests
import pickle
import numpy as np
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Crop Recommendation System", page_icon="🌱", layout="wide")

# --- Enhanced Custom CSS Styling with Nude Color Theme ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .main {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #1a1611 0%, #2d2520 50%, #1a1611 100%);
        color: #f5f2ed;
    }
    
    /* Header Styling - Nude theme */
    .main-header {
        background: linear-gradient(135deg, #d4c5b0 0%, #c7b299 50%, #b8a082 100%);
        padding: 2.5rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 25px 50px rgba(180, 160, 130, 0.3);
        border: 2px solid rgba(212, 197, 176, 0.3);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #4a3f35;
        text-shadow: 2px 2px 8px rgba(74, 63, 53, 0.3);
    }
    
    .subtitle {
        background: linear-gradient(135deg, #b8a082 0%, #a69074 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        color: #f5f2ed;
        font-size: 1.3rem;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 15px 30px rgba(166, 144, 116, 0.4);
        margin-bottom: 2rem;
        border: 1px solid rgba(166, 144, 116, 0.3);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.9rem;
        font-weight: 600;
        color: #d4c5b0;
        margin: 2.5rem 0 1.5rem 0;
        padding: 1rem 0;
        border-bottom: 3px solid #c7b299;
        text-shadow: 0 0 15px rgba(212, 197, 176, 0.4);
    }
    
    /* Card Styling - Nude theme */
    .weather-card {
        background: linear-gradient(135deg, rgba(212, 197, 176, 0.15) 0%, rgba(199, 178, 153, 0.15) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(212, 197, 176, 0.3);
        padding: 1.8rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(212, 197, 176, 0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(245, 242, 237, 0.1) 0%, rgba(245, 242, 237, 0.05) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(212, 197, 176, 0.4);
        padding: 1.8rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #d4c5b0;
        text-shadow: 0 0 20px rgba(212, 197, 176, 0.6);
    }
    
    .metric-label {
        font-size: 1rem;
        color: #c7b299;
        margin-top: 0.8rem;
        font-weight: 500;
    }
    
    /* Button Styling - Nude theme */
    .stButton > button {
        background: linear-gradient(135deg, #d4c5b0 0%, #c7b299 100%);
        color: #4a3f35;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        box-shadow: 0 10px 25px rgba(212, 197, 176, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(212, 197, 176, 0.6);
        background: linear-gradient(135deg, #e0d3c0 0%, #d4c5b0 100%);
    }
    
    /* Input Styling - Nude theme */
    .stTextInput > div > div > input {
        background: rgba(245, 242, 237, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(212, 197, 176, 0.4);
        border-radius: 12px;
        color: #f5f2ed;
        padding: 1rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #d4c5b0;
        box-shadow: 0 0 0 3px rgba(212, 197, 176, 0.3);
        background: rgba(245, 242, 237, 0.15);
    }
    
    .stSelectbox > div > div {
        background: rgba(245, 242, 237, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(212, 197, 176, 0.4);
        border-radius: 12px;
    }
    
    /* Alerts and Messages - Nude theme */
    .stAlert {
        border-radius: 15px;
        border: none;
        backdrop-filter: blur(15px);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(139, 125, 107, 0.25) 0%, rgba(122, 108, 91, 0.25) 100%);
        border: 2px solid rgba(139, 125, 107, 0.5);
        color: #f5f2ed;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(166, 144, 116, 0.25) 0%, rgba(148, 128, 105, 0.25) 100%);
        border: 2px solid rgba(166, 144, 116, 0.5);
        color: #f5f2ed;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(205, 180, 140, 0.25) 0%, rgba(190, 165, 125, 0.25) 100%);
        border: 2px solid rgba(205, 180, 140, 0.5);
        color: #f5f2ed;
    }
    
    /* Crop Recommendation Cards - Nude theme */
    .crop-card {
        background: linear-gradient(135deg, #8b7d6b 0%, #7a6c5b 100%);
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(139, 125, 107, 0.4);
        border: 2px solid rgba(139, 125, 107, 0.3);
        transition: all 0.4s ease;
    }
    
    .crop-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(139, 125, 107, 0.5);
    }
    
    .crop-name {
        color: #f5f2ed;
        font-size: 1.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .suitability-badge {
        background: linear-gradient(135deg, #cd b48c 0%, #be9d7d 100%);
        color: #4a3f35;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        display: inline-block;
        margin-left: 1rem;
        box-shadow: 0 5px 15px rgba(205, 180, 140, 0.4);
    }
    
    .crop-details {
        color: #f5f2ed;
        margin-top: 1rem;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-card {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Map Styling */
    .stMap {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(212, 197, 176, 0.3);
    }
    
    /* Footer - Nude theme */
    .footer-note {
        background: linear-gradient(135deg, rgba(166, 144, 116, 0.15) 0%, rgba(148, 128, 105, 0.15) 100%);
        border: 2px solid rgba(166, 144, 116, 0.4);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        color: #c7b299;
    }
    
    /* Custom subheader styling */
    .custom-subheader {
        font-size: 1.5rem;
        font-weight: 600;
        color: #d4c5b0;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 10px rgba(212, 197, 176, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class="main-header animated-card">
    <div class="main-title">🌱 Smart Crop Recommendation Dashboard</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle animated-card">
    <h4 style='color:#f5f2ed; margin: 0;'>🚀 Empowering farmers with AI-driven, weather-aware crop advice</h4>
</div>
""", unsafe_allow_html=True)

# --- Load Model ---
@st.cache_resource
def load_model():
    with open('crop_rf_model.pkl', 'rb') as f:
        return pickle.load(f)
model = load_model()

# --- Helper: Geocoding for Map ---
def get_lat_lon(city):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
    try:
        r = requests.get(url)
        data = r.json()
        if len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None, None
    except Exception:
        return None, None

# --- Helper: Real Weather and Forecast ---
def get_weather_and_forecast(city, api_key):
    url_now = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        now = requests.get(url_now).json()
        forecast = requests.get(url_forecast).json()
        if 'main' not in now or 'list' not in forecast:
            return None, None
        weather = {
            'temp': now['main']['temp'],
            'humidity': now['main']['humidity'],
            'rainfall': now.get('rain', {}).get('1h', 0)
        }
        forecast_days = []
        used_dates = set()
        for entry in forecast['list']:
            date = entry['dt_txt'][:10]
            hour = int(entry['dt_txt'][11:13])
            if hour == 12 and date not in used_dates:
                forecast_days.append({
                    'date': date,
                    'temp': entry['main']['temp'],
                    'humidity': entry['main']['humidity'],
                    'rainfall': entry.get('rain', {}).get('3h', 0)
                })
                used_dates.add(date)
            if len(forecast_days) == 5:
                break
        return weather, forecast_days
    except Exception:
        return None, None

# --- Static: Crop Calendar (Demo) ---
crop_calendar = {
    'Rice':    {'sow': 'June-July', 'harvest': 'October-November'},
    'Wheat':   {'sow': 'November-December', 'harvest': 'March-April'},
    'Maize':   {'sow': 'June-July', 'harvest': 'September-October'},
    'Barley':  {'sow': 'October-November', 'harvest': 'March-April'},
    'Millet':  {'sow': 'June-July', 'harvest': 'September-October'},
    'Soybean': {'sow': 'June-July', 'harvest': 'September-October'},
    'Sugarcane': {'sow': 'February-March', 'harvest': 'December-January'},
}

# --- Static: Market Prices and Financials (Demo) ---
market_data = {
    'Rice':     {'price': 2200, 'cost': 25000, 'yield': 22},
    'Wheat':    {'price': 2100, 'cost': 18000, 'yield': 18},
    'Maize':    {'price': 1700, 'cost': 15000, 'yield': 16},
    'Barley':   {'price': 1600, 'cost': 14000, 'yield': 14},
    'Millet':   {'price': 2000, 'cost': 12000, 'yield': 10},
    'Soybean':  {'price': 3500, 'cost': 20000, 'yield': 12},
    'Sugarcane':{'price': 340,  'cost': 40000, 'yield': 400},
}

# --- Main Page Input Details ---
st.markdown('<p class="custom-subheader">1. Enter Your Details</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    city = st.text_input("🌍 City/Town/Village", value="Hyderabad")
    soil_ph = st.text_input("🧪 Soil pH (optional)", value="")
    soil_type = st.selectbox("🌱 Soil Type (optional)", ["", "Sandy", "Clay", "Loam", "Silty", "Peaty", "Chalky"])

with col2:
    # Add spacing to align button properly
    st.markdown("<br><br>", unsafe_allow_html=True)
    fetch_weather = st.button("🌤️ Fetch Weather Data", use_container_width=True)

API_KEY = st.secrets["openweather"]["api_key"]
weather = None
if fetch_weather and city:
    with st.spinner("🌐 Fetching weather data..."):
        weather, forecast_days = get_weather_and_forecast(city, API_KEY)
        if weather and forecast_days:
            st.session_state["weather"] = weather
            st.session_state["forecast_days"] = forecast_days
            st.success(f"✅ Weather data for {city} successfully retrieved!")
            lat, lon = get_lat_lon(city)
            st.session_state["lat"] = lat
            st.session_state["lon"] = lon
        else:
            st.error("❌ Could not fetch weather data. Please check city name or API key.")
else:
    st.info("👆 Enter your city/town/village and click 'Fetch Weather Data' to continue.")

# --- Show Weather Data & Trends ---
if "weather" in st.session_state:
    weather = st.session_state["weather"]
    
    # Weather summary
    st.markdown(f"""
    <div class="weather-card animated-card">
        <h3 style="color: #d4c5b0; margin-bottom: 1rem;">🌤️ Current Weather Conditions</h3>
        <p style="font-size: 1.1rem; color: #f5f2ed;">
            <strong>Temperature:</strong> {weather['temp']}°C &nbsp;&nbsp;|&nbsp;&nbsp;
            <strong>Humidity:</strong> {weather['humidity']}% &nbsp;&nbsp;|&nbsp;&nbsp;
            <strong>Rainfall:</strong> {weather['rainfall']} mm
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Weather metrics in cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card animated-card">
            <div class="metric-value">{weather['temp']}°C</div>
            <div class="metric-label">🌡️ Temperature</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card animated-card">
            <div class="metric-value">{weather['humidity']}%</div>
            <div class="metric-label">💧 Humidity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card animated-card">
            <div class="metric-value">{weather['rainfall']}mm</div>
            <div class="metric-label">🌧️ Rainfall</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced weather chart with nude colors
    fig = go.Figure(data=[
        go.Bar(name='Current Weather',
               x=['Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)'],
               y=[weather['temp'], weather['humidity'], weather['rainfall']],
               marker=dict(
                   color=['#d4c5b0', '#c7b299', '#cdb48c'],  # Nude color palette
                   line=dict(color='rgba(245, 242, 237, 0.4)', width=2)
               ),
               text=[f"{weather['temp']}°C", f"{weather['humidity']}%", f"{weather['rainfall']}mm"],
               textposition='auto',
               textfont=dict(color='#4a3f35', size=12, family='Poppins')
               )
    ])
    fig.update_layout(
        height=350, 
        margin=dict(l=10, r=10, t=40, b=10), 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#f5f2ed', family='Poppins'),
        title=dict(text="Weather Overview", font=dict(size=18, color='#d4c5b0')),
        xaxis=dict(gridcolor='rgba(245, 242, 237, 0.1)'),
        yaxis=dict(gridcolor='rgba(245, 242, 237, 0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Weather trends
    forecast_days = st.session_state.get("forecast_days", [])
    if forecast_days:
        st.markdown('<p class="custom-subheader">📈 Weather Trends (Next 5 Days)</p>', unsafe_allow_html=True)
        
        dates = [d["date"] for d in forecast_days]
        temps = [d["temp"] for d in forecast_days]
        hums = [d["humidity"] for d in forecast_days]
        rains = [d["rainfall"] for d in forecast_days]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=dates, y=temps, 
            mode='lines+markers+text', 
            name='Temperature (°C)', 
            line=dict(color='#d4c5b0', width=4),
            marker=dict(size=10, color='#d4c5b0'),
            text=[f"{t}°C" for t in temps],
            textposition="top center",
            textfont=dict(color='#d4c5b0')
        ))
        fig2.add_trace(go.Scatter(
            x=dates, y=hums, 
            mode='lines+markers+text', 
            name='Humidity (%)', 
            line=dict(color='#c7b299', width=4),
            marker=dict(size=10, color='#c7b299'),
            text=[f"{h}%" for h in hums],
            textposition="top center",
            textfont=dict(color='#c7b299')
        ))
        fig2.add_trace(go.Scatter(
            x=dates, y=rains, 
            mode='lines+markers+text', 
            name='Rainfall (mm)', 
            line=dict(color='#cdb48c', width=4),
            marker=dict(size=10, color='#cdb48c'),
            text=[f"{r}mm" for r in rains],
            textposition="top center",
            textfont=dict(color='#cdb48c')
        ))
        
        fig2.update_layout(
            height=400, 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#f5f2ed', family='Poppins'),
            title=dict(text="5-Day Weather Forecast", font=dict(size=18, color='#c7b299')),
            xaxis=dict(gridcolor='rgba(245, 242, 237, 0.1)', title="Date"),
            yaxis=dict(gridcolor='rgba(245, 242, 237, 0.1)', title="Value"),
            legend=dict(
                bgcolor='rgba(245, 242, 237, 0.1)',
                bordercolor='rgba(245, 242, 237, 0.3)',
                borderwidth=2,
                font=dict(color='#f5f2ed')
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Location map
    lat = st.session_state.get("lat", None)
    lon = st.session_state.get("lon", None)
    if lat and lon:
        st.markdown('<p class="custom-subheader">🗺️ Your Location on Map</p>', unsafe_allow_html=True)
        map_df = pd.DataFrame({"lat": [lat], "lon": [lon], "Crop": ["?"]})
        st.map(map_df)

# --- Crop Recommendation ---
st.markdown('<p class="custom-subheader">2. AI Crop Recommendations (Top 3)</p>', unsafe_allow_html=True)

recommend_crop = st.button("🌾 Recommend Crops", use_container_width=True)

if recommend_crop:
    if not city:
        st.warning("⚠️ Please enter your location and fetch weather data.")
    elif "weather" not in st.session_state:
        st.warning("⚠️ Please fetch weather data first.")
    else:
        weather = st.session_state["weather"]
        
        # Prepare soil features (keeping original calculation logic)
        soil_features = []
        if soil_ph:
            try:
                soil_features.append(float(soil_ph))
            except Exception:
                soil_features.append(7.0)
        else:
            soil_features.append(7.0)
        
        soil_type_map = {"Sandy": 1, "Clay": 2, "Loam": 3, "Silty": 4, "Peaty": 5, "Chalky": 6, "": 0}
        soil_features.append(soil_type_map.get(soil_type, 0))
        
        X = np.array([[weather['temp'], weather['humidity'], weather['rainfall']] + soil_features])
        X = X[:, :3]  # Keep original model input format
        
        proba = model.predict_proba(X)[0]
        crops = model.classes_
        top3_idx = np.argsort(proba)[::-1][:3]
        
        st.success(f"🌾 **Top 3 recommended crops for {city}:**")
        
        for idx in top3_idx:
            crop = crops[idx]
            score = proba[idx]
            sow = crop_calendar.get(crop, {}).get('sow', 'N/A')
            harvest = crop_calendar.get(crop, {}).get('harvest', 'N/A')
            price = market_data.get(crop, {}).get('price', 'N/A')
            cost = market_data.get(crop, {}).get('cost', 'N/A')
            yield_ = market_data.get(crop, {}).get('yield', 'N/A')
            
            if all(isinstance(x, (int, float)) for x in [price, cost, yield_]):
                revenue = price * yield_
                profit = revenue - cost
            else:
                revenue = profit = 'N/A'
            
            st.markdown(f"""
            <div class='crop-card animated-card'>
                <b class='crop-name'>{crop}</b>
                <span class='suitability-badge'>Suitability: {score*100:.1f}%</span><br><br>
                <div class='crop-details'>
                    <strong>🌱 Sow:</strong> <b>{sow}</b> &nbsp;&nbsp;|&nbsp;&nbsp; <strong>🌾 Harvest:</strong> <b>{harvest}</b><br>
                    <strong>💰 Market Price:</strong> <b>₹{price}/quintal</b> &nbsp;&nbsp;|&nbsp;&nbsp; <strong>💵 Input Cost:</strong> <b>₹{cost}/acre</b> &nbsp;&nbsp;|&nbsp;&nbsp; <strong>📊 Yield:</strong> <b>{yield_} qtl/acre</b><br>
                    <strong>💼 Estimated Revenue:</strong> <b>₹{revenue}</b> &nbsp;&nbsp;|&nbsp;&nbsp; <strong>💸 Estimated Profit:</strong> <b>₹{profit}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("📝 This is a demonstration. For production use, train the model on local agricultural data and expand the crop calendar with real market information!")

st.markdown("""
<div class="footer-note animated-card">
    <strong>🌟 Want more features?</strong><br>
    Try adding downloadable reports, user dashboards, or real-time market integration next!
</div>
""", unsafe_allow_html=True)
