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

    r = requests.get(url.format(city, API_KEY)).json()

    weather = {
        'city': city,
        'temperature': round(r['main']['temp']),
        'description': r['weather'][0]['description'].title(),
        'icon': r['weather'][0]['icon']
    }

    print(weather)

    return render_template('weather.html', weather=weather)