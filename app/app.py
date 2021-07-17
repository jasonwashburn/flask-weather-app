import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

API_KEY = os.getenv('API_KEY')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "thisisasecret"

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_city_weather_data(city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid={ API_KEY }"
    response = requests.get(url).json()
    return response


@app.route("/")
def index_get():
    cities = City.query.all()

    weather_data = []
    for city in cities:
        response = get_city_weather_data(city.name)

        weather = {
            'city': city.name.title(),
            'temperature': round(response['main']['temp']),
            'description': response['weather'][0]['description'].title(),
            'icon': response['weather'][0]['icon']
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


@app.route("/", methods=["POST"])
def index_post():
    err_msg = ""
    if request.method == "POST":
        new_city = request.form.get("city").lower()
        if new_city:
            existing_city = City.query.filter_by(name=new_city).first()
            if not existing_city:
                new_city_data = get_city_weather_data(new_city)
                if new_city_data['cod'] == 200:
                    new_city_obj = City(name=new_city)
                    db.session.add(new_city_obj)
                    db.session.commit()
                else:
                    err_msg = "City does not exist!"
            else:
                err_msg = "City already exists in the database!"

    if err_msg:
        flash(err_msg, "error")
    else:
        flash("City added successfully")

    return redirect(url_for("index_get"))


@app.route("/delete/<name>")
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f"{ name } successfully deleted", "success")
    return redirect(url_for("index_get"))


if __name__ == "__main__":
    app.run(host='0.0.0.0')