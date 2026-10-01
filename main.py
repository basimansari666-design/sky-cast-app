from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/weather")
def weather():
    city = request.args.get("city", "Karachi")

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city,
            "count": 1,
            "format": "json"
        }

        geo = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        ).json()

        if "results" not in geo:
            return jsonify({
                "error": "City not found"
            }), 404

        place = geo["results"][0]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,"
                "apparent_temperature,"
                "relative_humidity_2m,"
                "wind_speed_10m,"
                "weather_code"
            ),
            "timezone": "auto"
        }

        data = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        ).json()

        return jsonify({
            "city": place["name"],
            "country": place.get("country", ""),
            "temperature": data["current"]["temperature_2m"],
            "feels_like": data["current"]["apparent_temperature"],
            "humidity": data["current"]["relative_humidity_2m"],
            "wind": data["current"]["wind_speed_10m"],
            "weather_code": data["current"]["weather_code"]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run()
