import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

API_KEY = os.getenv('API_KEY')
app = Flask(__name__)


@app.route("/")
def index():
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"
    city = 'Omaha'
    response = requests.get(url.format(city, API_KEY)).json()

    weather = {
        'city': city,
        'temperature': round(response['main']['temp']),
        'description': response['weather'][0]['description'].title(),
        'icon': response['weather'][0]['icon']
    }

    print(weather)

    return render_template('weather.html', weather=weather)


if __name__ == "__main__":
    app.run(host='0.0.0.0')