import streamlit as st
import requests
import pickle
import numpy as np
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Crop Recommendation System", page_icon="🌱", layout="wide")

# --- Enhanced Custom CSS Styling with Pastel Colors ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%);
        color: #ffffff;
    }
    
    /* Header Styling - Pastel theme */
    .main-header {
        background: linear-gradient(135deg, #ffd3e1 0%, #fd9bb4 50%, #f06292 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(253, 155, 180, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #ffffff, #f8f8f8);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(253, 155, 180, 0.4);
    }
    
    .subtitle {
        background: linear-gradient(135deg, #e1bee7 0%, #ce93d8 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 10px 25px rgba(206, 147, 216, 0.4);
        margin-bottom: 2rem;
        border: 1px solid rgba(206, 147, 216, 0.3);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffb3d1;
        margin: 2rem 0 1rem 0;
        padding: 1rem 0;
        border-bottom: 2px solid #ffb3d1;
        text-shadow: 0 0 10px rgba(255, 179, 209, 0.5);
    }
    
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.08) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 179, 209, 0.25);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffb3d1;
        text-shadow: 0 0 15px rgba(255, 179, 209, 0.6);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #e8c5d8;
        margin-top: 0.5rem;
    }
    
    /* Button Styling - Pastel theme */
    .stButton > button {
        background: linear-gradient(135deg, #ffb3d1 0%, #f8bbd9 100%);
        color: #2d1b2e;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(255, 179, 209, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 179, 209, 0.6);
        background: linear-gradient(135deg, #ffc1e3 0%, #ffcce5 100%);
    }
    
    /* Input Styling - Pastel theme */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 179, 209, 0.4);
        border-radius: 10px;
        color: #ffffff;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffb3d1;
        box-shadow: 0 0 0 3px rgba(255, 179, 209, 0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 179, 209, 0.4);
        border-radius: 10px;
    }
    
    /* Alerts and Messages - Pastel theme */
    .stAlert {
        border-radius: 12px;
        border: none;
        backdrop-filter: blur(10px);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(174, 213, 129, 0.25) 0%, rgba(139, 195, 74, 0.25) 100%);
        border: 1px solid rgba(174, 213, 129, 0.5);
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(179, 209, 255, 0.25) 0%, rgba(144, 202, 249, 0.25) 100%);
        border: 1px solid rgba(179, 209, 255, 0.5);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 213, 79, 0.25) 0%, rgba(255, 193, 7, 0.25) 100%);
        border: 1px solid rgba(255, 213, 79, 0.5);
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-card {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Map Styling */
    .stMap {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }
    
    /* Footer - Pastel theme */
    .footer-note {
        background: linear-gradient(135deg, rgba(206, 147, 216, 0.12) 0%, rgba(179, 209, 255, 0.12) 100%);
        border: 1px solid rgba(206, 147, 216, 0.3);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
        color: #d0d0d0;
    }
    </style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class="main-header animated-card">
    <div class="main-title">🌱 Smart Crop Recommendation</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle animated-card">
    <h4 style='color:#ffffff; margin: 0;'>🚀 Empowering farmers with AI-driven, weather-aware crop advice</h4>
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
# Prices in Rs/quintal, costs in Rs/acre, yield in quintal/acre
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
st.markdown('<p class="section-header">📍 Location & Soil Information</p>', unsafe_allow_html=True)

# Clean Input Section without unnecessary containers
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    city = st.text_input("🌍 City/Town/Village", value="Hyderabad", help="Enter your location")
    soil_ph = st.text_input("🧪 Soil pH (optional)", value="", help="Enter soil pH value (6.0-8.0)")

with col2:
    soil_type = st.selectbox("🌱 Soil Type (optional)", 
                           ["", "Sandy", "Clay", "Loam", "Silty", "Peaty", "Chalky"],
                           help="Select your soil type")
    fetch_weather = st.button("🌤️ Fetch Weather Data", use_container_width=True, 
                             help="Get current weather conditions")

with col3:
    if city and soil_type:
        st.markdown("""
        <div class="metric-card animated-card">
            <div class="metric-value">📊</div>
            <div class="metric-label">Data Ready</div>
        </div>
        """, unsafe_allow_html=True)

API_KEY = st.secrets["openweather"]["api_key"]
weather = None
if fetch_weather and city:
    with st.spinner("🌐 Fetching weather data..."):
        # For demo, use static forecast data
        forecast_days = [
            {"date": "2025-09-24", "temp": 24, "humidity": 90, "rainfall": 0},
            {"date": "2025-09-25", "temp": 24, "humidity": 90, "rainfall": 2},
            {"date": "2025-09-26", "temp": 25, "humidity": 92, "rainfall": 8},
            {"date": "2025-09-27", "temp": 24, "humidity": 88, "rainfall": 5},
            {"date": "2025-09-28", "temp": 23, "humidity": 85, "rainfall": 0},
        ]
        weather = forecast_days[0]
        st.session_state["weather"] = weather
        st.session_state["forecast_days"] = forecast_days
        st.success(f"✅ Weather data for {city} successfully retrieved!")
        lat, lon = get_lat_lon(city)
        st.session_state["lat"] = lat
        st.session_state["lon"] = lon
else:
    st.info("👆 Enter your location and click 'Fetch Weather Data' to continue.")

# --- Show Weather Data & Trends ---
if "weather" in st.session_state:
    weather = st.session_state["weather"]
    
    st.markdown('<p class="section-header">🌤️ Current Weather Conditions</p>', unsafe_allow_html=True)
    
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
    
    # Enhanced weather chart with pastel colors
    fig = go.Figure(data=[
        go.Bar(name='Current Weather',
               x=['Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)'],
               y=[weather['temp'], weather['humidity'], weather['rainfall']],
               marker=dict(
                   color=['#ffb3d1', '#aed581', '#ffe082'],  # Pastel pink, light green, soft yellow
                   line=dict(color='rgba(255,255,255,0.3)', width=2)
               ),
               text=[f"{weather['temp']}°C", f"{weather['humidity']}%", f"{weather['rainfall']}mm"],
               textposition='auto'
               )
    ])
    fig.update_layout(
        height=350, 
        margin=dict(l=10, r=10, t=40, b=10), 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#ffffff', family='Inter'),
        title=dict(text="Weather Overview", font=dict(size=18, color='#ffb3d1')),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Weather trends with pastel colors
    forecast_days = st.session_state.get("forecast_days", [])
    if forecast_days:
        st.markdown('<p class="section-header">📈 5-Day Weather Forecast</p>', unsafe_allow_html=True)
        
        dates = [d["date"] for d in forecast_days]
        temps = [d["temp"] for d in forecast_days]
        hums = [d["humidity"] for d in forecast_days]
        rains = [d["rainfall"] for d in forecast_days]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=dates, y=temps, 
            mode='lines+markers+text', 
            name='Temperature (°C)', 
            line=dict(color='#ffb3d1', width=3),  # Pastel pink
            marker=dict(size=8, color='#ffb3d1'),
            text=[f"{t}°C" for t in temps],
            textposition="top center"
        ))
        fig2.add_trace(go.Scatter(
            x=dates, y=hums, 
            mode='lines+markers+text', 
            name='Humidity (%)', 
            line=dict(color='#aed581', width=3),  # Light green
            marker=dict(size=8, color='#aed581'),
            text=[f"{h}%" for h in hums],
            textposition="top center"
        ))
        fig2.add_trace(go.Scatter(
            x=dates, y=rains, 
            mode='lines+markers+text', 
            name='Rainfall (mm)', 
            line=dict(color='#ffe082', width=3),  # Soft yellow
            marker=dict(size=8, color='#ffe082'),
            text=[f"{r}mm" for r in rains],
            textposition="top center"
        ))
        
        fig2.update_layout(
            height=400, 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#ffffff', family='Inter'),
            title=dict(text="Weather Trends", font=dict(size=18, color='#aed581')),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title="Date"),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title="Value"),
            legend=dict(
                bgcolor='rgba(255,255,255,0.1)',
                bordercolor='rgba(255,255,255,0.3)',
                borderwidth=1
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Location map
    lat = st.session_state.get("lat", None)
    lon = st.session_state.get("lon", None)
    if lat and lon:
        st.markdown('<p class="section-header">🗺️ Your Location</p>', unsafe_allow_html=True)
        map_df = pd.DataFrame({"lat": [lat], "lon": [lon], "location": [city]})
        st.map(map_df, zoom=10)

# --- Crop Recommendation ---
st.markdown('<p class="section-header">🤖 AI-Powered Crop Recommendations</p>', unsafe_allow_html=True)

recommend_crop = st.button("🌾 Get Crop Recommendations", use_container_width=True, 
                          help="Generate top 3 crop recommendations based on your data")

if recommend_crop:
    if not city:
        st.warning("⚠️ Please enter your location and fetch weather data first.")
    elif "weather" not in st.session_state:
        st.warning("⚠️ Please fetch weather data before getting recommendations.")
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
        
        st.markdown(f"### 🏆 Top 3 Recommended Crops for {city}")
        
        for i, idx in enumerate(top3_idx):
            crop = crops[idx]
            score = proba[idx]
            sow = crop_calendar.get(crop, {}).get('sow', 'N/A')
            harvest = crop_calendar.get(crop, {}).get('harvest', 'N/A')
            
            # Market price and financials (keeping original calculation)
            price = market_data.get(crop, {}).get('price', 'N/A')
            cost = market_data.get(crop, {}).get('cost', 'N/A')
            yield_ = market_data.get(crop, {}).get('yield', 'N/A')
            
            if all(isinstance(x, (int, float)) for x in [price, cost, yield_]):
                revenue = price * yield_
                profit = revenue - cost
            else:
                revenue = profit = 'N/A'
            
            # Enhanced crop recommendation card with pastel colors
            rank_colors = ['#ffb3d1', '#aed581', '#b3d9ff']  # Pastel Pink, Light Green, Light Blue
            rank_emoji = ['🥇', '🥈', '🥉']
            
            # Create a clean card layout
            with st.container():
                # Create columns for better layout
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"#### {rank_emoji[i]} {crop}")
                    
                    # Use Streamlit columns for crop details
                    detail_col1, detail_col2 = st.columns(2)
                    
                    with detail_col1:
                        st.markdown(f"""
                        **🌱 Sowing Period:** {sow}
                        
                        **🌾 Harvest Period:** {harvest}
                        """)
                    
                    with detail_col2:
                        st.markdown(f"""
                        **💰 Market Price:** ₹{price}/quintal
                        
                        **📊 Expected Yield:** {yield_} qtl/acre
                        """)
                    
                    # Financial analysis in a separate info box
                    st.info(f"""
                    **💼 Financial Analysis:**
                    - Input Cost: ₹{cost}/acre
                    - Estimated Revenue: ₹{revenue}
                    - Estimated Profit: ₹{profit}
                    """)
                
                with col2:
                    # Suitability score as a metric
                    st.metric(
                        label="Suitability Score",
                        value=f"{score*100:.1f}%",
                        delta=None
                    )
                    
                    # Progress bar for visual representation with pastel colors
                    progress_color = rank_colors[i]
                    st.markdown(f"""
                    <div style="margin: 1rem 0;">
                        <div style="background: rgba(255,255,255,0.1); height: 12px; border-radius: 6px; overflow: hidden;">
                            <div style="background: {progress_color}; height: 100%; width: {score*100:.1f}%; border-radius: 6px; 
                                       box-shadow: 0 0 10px {progress_color}50;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
        
        # Demo disclaimer
        st.markdown("""
        <div class="footer-note animated-card">
            <strong>📝 Demo Note:</strong> This is a prototype demonstration. For production use, 
            train the model on local agricultural data and expand crop calendar with market information.
            <br><br>
            <strong>🚀 Future Enhancements:</strong> Add downloadable reports, user dashboards, 
            and real-time market price integration!
        </div>
        """, unsafe_allow_html=True)
