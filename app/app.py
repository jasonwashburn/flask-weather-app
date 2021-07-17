import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

API_KEY = os.getenv('API_KEY')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_city = request.form.get("city")
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"

    weather_data = []
    for city in cities:
        response = requests.get(url.format(city.name, API_KEY)).json()

        weather = {
            'city': city.name,
            'temperature': round(response['main']['temp']),
            'description': response['weather'][0]['description'].title(),
            'icon': response['weather'][0]['icon']
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0')