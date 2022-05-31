from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sql_return
import os

app = Flask(__name__)
SQL = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

filters = dict(location='all', sockets='all', wifi='all', toilet='all', calls='all', seats='all', coffee_price='all')
img_selected = False
cafe_url = ''
cafe_name_loc = []


class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean(), nullable=False)
    has_toilet = db.Column(db.Boolean(), nullable=False)
    has_wifi = db.Column(db.Boolean(), nullable=False)
    can_take_calls = db.Column(db.Boolean(), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


def cafe_output():
    global filters

    final_query = []

    for key in filters:
        if filters[key] == 'all':
            filters[key] = None
        elif filters[key] == 'yes':
            filters[key] = 0
        elif filters[key] == 'no':
            filters[key] = 1


    query = Cafe.query.filter(Cafe.has_sockets != filters['sockets'],
                              Cafe.has_wifi != filters['wifi'],
                              Cafe.has_toilet != filters['toilet'],
                              Cafe.can_take_calls != filters['calls']).all()

    for cafe in query:
        if filters['location'] is not None:
            if filters['location'] == cafe.location:
                final_query.append(cafe)
        if filters['seats'] is not None:
            if filters['seats'] == cafe.seats:
                final_query.append(cafe)
        if filters['coffee_price'] is not None:
            if filters['coffee_price'] == cafe.coffee_price:
                final_query.append(cafe)
        elif filters['location'] is None and filters['seats'] is None and filters['coffee_price'] is None:
            final_query.append(cafe)

    return final_query


@app.route('/dropdown_filter/<string:field>/<string:value>', methods=['POST'])
def dropdown_filter(field, value):
    global filters
    global img_selected
    img_selected = False
    filters[field] = request.form.get(value)
    return redirect(url_for('home'))


@app.route('/clear_filters')
def clear_filters():
    global filters
    global img_selected
    img_selected = False
    for key in filters:
        filters[key] = 'all'
    return redirect(url_for('home'))


@app.route('/filter/<string:key>/<string:val>')
def db_filter(key, val):
    global img_selected
    global filters
    img_selected = True
    filters[key] = val
    return redirect(url_for('home'))


@app.route('/img_selector/<string:cafe_name>')
def img_selector(cafe_name):
    global img_selected
    global cafe_url
    global cafe_name_loc
    img_selected = True
    cafe_url = sql_return.SQLReturn().single_cafe(cafe_name)
    cafe_name_loc = [cafe_url.name, cafe_url.location]
    cafe_url = cafe_url.img_url
    return redirect(url_for('home'))



@app.route('/')
def home():
    global filters
    global img_selected
    global cafe_url
    global cafe_name_loc
    locations = sql_return.SQLReturn().all_locations()
    seats = sql_return.SQLReturn().all_seats()
    prices = sql_return.SQLReturn().all_prices()
    cafe_info = cafe_output()
    if not img_selected:
        cafe_url = cafe_info[0].img_url
        cafe_name_loc = [cafe_info[0].name, cafe_info[0].location]

    return render_template("index.html", locations=locations, seats=seats, prices=prices, cafe_info=cafe_info,
                           cafe_url=cafe_url, cafe_name_loc=cafe_name_loc)


if __name__ == '__main__':
    app.run(debug=True)
