import streamlit as st
import streamlit as st

st.set_page_config(page_title="Weather App", page_icon="🌤️")

st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1687938929591-5fed723326e6?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="weather-box">
<h1>🌤️ Weather App</h1>
<p>Check the weather of your city</p>
</div>
""", unsafe_allow_html=True)
import requests
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(page_title="Weather App", page_icon="🌤️")

st.title("🌤️ Weather App")

# City select
cities = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"]
city = st.selectbox("🏙️ Select City", cities)

# City weather
if st.button("🌤️ Get City Weather"):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    geo = requests.get(geo_url).json()

    if "results" in geo:
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )

        weather = requests.get(weather_url).json()["current"]

        st.success(f"📍 Weather of {city}")
        st.metric("🌡️ Temperature", f"{weather['temperature_2m']} °C")
        st.metric("💧 Humidity", f"{weather['relative_humidity_2m']} %")
        st.metric("💨 Wind", f"{weather['wind_speed_10m']} km/h")


st.divider()

# Use My Location
st.subheader("📍 Use your Location")

location = streamlit_geolocation()

if location and location.get("latitude"):

    lat = location["latitude"]
    lon = location["longitude"]

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    weather = requests.get(weather_url).json()["current"]

    st.success("📍 Your location detected!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🌡️ Temperature", f"{weather['temperature_2m']} °C")

    with col2:
        st.metric("💧 Humidity", f"{weather['relative_humidity_2m']} %")

    with col3:
        st.metric("💨 Wind", f"{weather['wind_speed_10m']} km/h")

else:
    st.info("👆 Click the location button above to allow your location.")
    