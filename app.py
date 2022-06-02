'''
CS340 Portfolio Project
Citation for the following function: Holistic citation for CRUD operations in Flask (followed guide)
Date: 6/1/2022
Copied from /OR/ Adapted from /OR/ Based on: The OSU CS340 Flask Guide
Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
'''

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_XXXX'
app.config['MYSQL_PASSWORD'] = 'XXX' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_XXXX'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes

# -------------- HOME PAGE ---------------------

@app.route('/')
def root():
    return render_template("home.j2")

@app.route('/home', methods=["POST", "GET"])
def home():
    return render_template("home.j2")


# -------------- GUEST TABLE ---------------------

# CREATE / READ
@app.route('/guests',  methods=["POST", "GET"])
def guests():
    if request.method == "POST":
        guest_name = request.form["guest_name"]
        email = request.form["email"]
        phone_num = request.form["phone_num"]

        # phone number is NULL-able
        if phone_num == "":
            query = "INSERT INTO guests (guest_name, email) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (guest_name, email))
            mysql.connection.commit()
            return redirect('/guests')

        else:
            query = "INSERT INTO guests (guest_name, email, phone_num) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (guest_name, email, phone_num))
            mysql.connection.commit()
            return redirect('/guests')

    elif request.method == "GET":
        query = "SELECT * FROM guests"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("guests.j2", guests=results)

# DELETE
@app.route("/delete_guest/<int:guest_id>")
def delete_guest(guest_id):
    query = "DELETE FROM guests WHERE guest_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (guest_id,))
    mysql.connection.commit()
    return redirect('/guests')

# UPDATE
@app.route("/edit_guest/<int:guest_id>", methods=["POST", "GET"])
def edit_guest(guest_id):
    if request.method == "GET":
        query = "SELECT * FROM guests WHERE guest_id = '%s'" % (guest_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_guest.j2", data=data)

    if request.method == "POST":
        guest_id = request.form["guest_id"]
        guest_name = request.form["guest_name"]
        email = request.form["email"]
        phone_num = request.form["phone_num"]

        # phone number is NULL-able
        if phone_num == "":
            phone_num = None
            query = "UPDATE guests SET guest_name = %s, guests.email = %s, guests.phone_num = %s WHERE guest_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (guest_name, email, phone_num, guest_id))
            mysql.connection.commit()
            return redirect('/guests')

        else:
            query = "UPDATE guests SET guest_name = %s, email = %s, phone_num = %s WHERE guest_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (guest_name, email, phone_num, guest_id))
            mysql.connection.commit()
            return redirect('/guests')


# -------------- ATTRACTIONS TABLE ---------------------

# CREATE / READ 
@app.route('/attractions',  methods=["POST", "GET"])
def attractions():
    if request.method == "POST":
        ride_name = request.form["ride_name"]
        date_created = request.form["date_created"]
        num_riders = 0

        query = "INSERT INTO attractions (ride_name, date_created, num_riders) VALUES (%s, (SELECT date FROM dates WHERE date=%s), %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (ride_name, date_created, num_riders))
        mysql.connection.commit()
        return redirect('/attractions')

    elif request.method == "GET":
        query = "SELECT * FROM attractions;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("attractions.j2", attractions=results)

# DELETE
@app.route("/delete_attraction/<int:ride_id>")
def delete_attraction(ride_id):
    query = "DELETE FROM attractions WHERE ride_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (ride_id,))
    mysql.connection.commit()
    return redirect('/attractions')

# UPDATE
@app.route("/edit_attraction/<int:ride_id>", methods=["POST", "GET"])
def edit_attraction(ride_id):
    if request.method == "GET":
        query = "SELECT * FROM attractions WHERE ride_id = '%s'" % (ride_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_attraction.j2", data=data)

    if request.method == "POST":
        ride_id = request.form["ride_id"]
        ride_name = request.form["ride_name"]
        date_created = request.form["date_created"]
        num_riders = request.form["num_riders"]

        query = "UPDATE attractions SET date_created=(SELECT date FROM dates WHERE date=%s), ride_name = %s, num_riders = %s WHERE ride_id=%s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date_created, ride_name, num_riders, ride_id))
        mysql.connection.commit()
        return redirect('/attractions')


# -------------- ORDERS TABLE ---------------------

# CREATE / READ
@app.route('/orders', methods=["POST", "GET"])
def orders():
    if request.method == "POST":
        guest_id = request.form["Guest_ID"]
        date = request.form["date_created"]
        ticket = request.form["ticket"]
        season_pass = request.form["season_pass"]

        query = "INSERT INTO orders (guest_id, date, ticket, season_pass_holder) VALUES ((SELECT guest_id FROM guests WHERE guest_id=%s), (SELECT date FROM dates WHERE date=%s), ticket=%s, season_pass_holder=%s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (guest_id, date, ticket, season_pass))
        mysql.connection.commit()
        return redirect('/orders')

    elif request.method == "GET":
        query = "SELECT * FROM orders;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("orders.j2", orders=results)

# UPDATE
@app.route("/edit_order/<int:order_id>", methods=["POST", "GET"])
def edit_order(order_id):
    if request.method == "GET":
        query = "SELECT * FROM orders WHERE order_id = '%s'" % (order_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_order.j2", data=data)

    if request.method == "POST":
        guest_id = request.form["guest_id"]
        date = request.form["date"]
        ticket = request.form["ticket"]
        season_pass_holder = request.form["season_pass_holder"]

        query = "UPDATE orders SET date=(SELECT date FROM dates WHERE date=%s), ticket=%s, season_pass_holder=%s, guest_id = (SELECT guest_id FROM guests WHERE guest_id=%s) WHERE order_id=%s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, ticket, season_pass_holder, guest_id, order_id))
        mysql.connection.commit()
        return redirect('/orders')

# DELETE
@app.route("/delete_order/<int:order_id>")
def delete_order(order_id):
    query = "DELETE FROM orders WHERE order_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (order_id,))
    mysql.connection.commit()
    return redirect('/orders')


# -------------- DATES TABLE ---------------------

# CREATE / READ
@app.route('/dates', methods=["POST", "GET"])
def dates():
    if request.method == "POST":
        date = request.form["date"]
        day_of_week = request.form["day_of_week"]
        holiday = request.form["holiday"]
        weather = request.form["weather"]

        query = "INSERT INTO dates (date, day_of_week, holiday, weather) VALUES (%s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, day_of_week, holiday, weather))
        mysql.connection.commit()
        return redirect('/dates')

    elif request.method == "GET":
        query = "SELECT * FROM dates;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("dates.j2", dates=results)

# UPDATE
@app.route("/edit_date/<string:date>", methods=["POST", "GET"])
def edit_date(date):
    if request.method == "GET":
        query = "SELECT * FROM dates WHERE date = '%s'" % (date)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_date.j2", data=data)
    
    if request.method == "POST":
        date = request.form["date"]
        day_of_week = request.form["day_of_week"]
        holiday = request.form["holiday"]
        weather = request.form["weather"]

        query = "UPDATE dates SET date=%s, day_of_week = %s, holiday = %s, weather = %s WHERE date = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, day_of_week, holiday, weather, date))
        mysql.connection.commit()
        return redirect('/dates')

# DELETE
@app.route("/delete_date/<string:date>")
def delete_date(date):
    query = "DELETE FROM dates WHERE date = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query,(date,))
    mysql.connection.commit()
    return redirect('/dates')


# -------------- GUESTS_HAS_ATTRACTIONS TABLE ---------------------

# CREATE / READ
@app.route('/guests_has_attractions', methods=["POST", "GET"])
def guests_has_attractions():
    if request.method == "POST":
        ride_id = request.form["ride_id"]
        date_created = request.form["date"]
        guest_id = request.form["guest_id"]
        
        query = "INSERT INTO guests_has_attractions (guest_id, ride_id, date) VALUES ((SELECT guest_id FROM guests WHERE guest_id=%s), (SELECT ride_id FROM attractions WHERE ride_id=%s), (SELECT date FROM dates WHERE date=%s))"
        cur = mysql.connection.cursor()
        cur.execute(query, (guest_id, ride_id, date_created))
        mysql.connection.commit()
        return redirect('/guests_has_attractions')

    query = "SELECT * FROM guests_has_attractions;"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return render_template("guests_has_attractions.j2", guests_has_attractions=results)

# DELETE
@app.route("/delete_guests_has_attractions/<int:guest_attraction_id>")
def delete_guests_has_attractions(guest_attraction_id):
    query = "DELETE FROM guests_has_attractions WHERE guest_attraction_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query,(guest_attraction_id,))
    mysql.connection.commit()
    return redirect('/guests_has_attractions')


# -------------- MASTER_TABLE TABLE ---------------------

# CREATE / READ
@app.route('/master_table',  methods=["POST", "GET"])
def master_table():
    if request.method == "POST":
        date = request.form["date"]
        total_guests = request.form["total_guests"]
        total_riders = request.form["total_riders"]

        if total_riders == '':
            query = "INSERT INTO master_table (date, total_guests) VALUES ((SELECT date FROM dates WHERE date=%s), %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (date, total_guests))
            mysql.connection.commit()
            return redirect('/master_table')

        else:
            query = "INSERT INTO master_table (date, total_guests, total_riders) VALUES ((SELECT date FROM dates WHERE date=%s), %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (date, total_guests, total_riders))
            mysql.connection.commit()
            return redirect('/master_table')

    elif request.method == "GET":
        query = "SELECT * FROM master_table;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("master_table.j2", master_table=results)

# UPDATE
@app.route("/edit_master_table/<int:table_id>", methods=["POST", "GET"])
def edit_master_table(table_id):
    if request.method == "GET":
        query = "SELECT * FROM master_table WHERE table_id = '%s'" % (table_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_master_table.j2", data=data)

    if request.method == "POST":
        table_id = request.form["table_id"]
        date = request.form["date"]
        total_guests = request.form["total_guests"]
        total_riders = request.form["total_riders"]

        query = "UPDATE master_table SET date=(SELECT date FROM dates WHERE date=%s), total_guests = %s, total_riders = %s WHERE table_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, total_guests, total_riders, table_id))
        mysql.connection.commit()
        return redirect('/master_table')

# DELETE
@app.route("/delete_table/<int:table_id>")
def delete_master_table(table_id):
    query = "DELETE FROM master_table WHERE table_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query,(table_id,))
    mysql.connection.commit()
    return redirect('/master_table')

# LISTENER
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4785)) 
    app.run(port=port, debug=True)