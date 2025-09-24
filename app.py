import streamlit as st
import requests
import pandas as pd

# Dummy crop recommendation model (replace with real trained model)
def load_model():
    # For demonstration: crops are ["Rice", "Wheat", "Maize"]
    class DummyModel:
        def predict(self, X):
            # Simple rule: if rainfall high, rice; temp > 25 maize; else wheat
            results = []
            for _, row in X.iterrows():
                if row['rainfall'] > 100:
                    results.append("Rice")
                elif row['temperature'] > 25:
                    results.append("Maize")
                else:
                    results.append("Wheat")
            return results
    return DummyModel()

def fetch_weather(location, api_key):
    # Get basic weather data (replace location logic as needed)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    r = requests.get(url)
    data = r.json()
    if r.status_code != 200 or "main" not in data:
        return None
    return {
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'rainfall': data.get('rain', {}).get('1h', 0)  # fallback if no rain data
    }

st.title("AI-Based Crop Recommendation for Farmers 🌾")

st.sidebar.header("Enter your location")
location = st.sidebar.text_input("City/Town/Village", value="Delhi")
api_key = st.secrets["openweather_api"] if "openweather_api" in st.secrets else st.text_input("OpenWeatherMap API Key")

if st.button("Get Recommendation"):
    weather = fetch_weather(location, api_key)
    if weather:
        st.write(f"Weather in {location}:", weather)
        X = pd.DataFrame([weather])
        model = load_model()
        crop = model.predict(X)[0]
        st.success(f"Recommended crop: **{crop}** ✅")
    else:
        st.error("Could not fetch weather. Check your API key and location.")

st.info("This is a demo. Replace the rule-based model and add more features as needed!")
