from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_sevierk'
app.config['MYSQL_PASSWORD'] = '5662' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_sevierk'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes

# HOME PAGE

@app.route('/')
def root():
    return render_template("home.j2")

@app.route('/home', methods=["POST", "GET"])
def home():
    return render_template("home.j2")

# GUEST TABLES

# GUESTS CREATE AND READ ALL 
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

# GUESTS DELETE
@app.route("/delete_guest/<int:guest_id>")
def delete_guest(guest_id):
    query = "DELETE FROM guests WHERE guest_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (guest_id,))
    mysql.connection.commit()
    return redirect('/guests')

# GUESTS UPDATE
@app.route("/edit_guest/<int:guest_id>", methods=["POST", "GET"])
def edit_guest(guest_id):
    if request.method == "GET":
        # First, we target the guest that we want to edit
        query = "SELECT * FROM guests WHERE guest_id = '%s'" % (guest_id)
        cur = mysql.connection.cursor()
        cur.execute(query) #(guest_id,))
        data = cur.fetchall()
        return render_template("edit_guest.j2", data=data)

    if request.method == "POST":
        # taking in edit guest form inputs
        guest_id = request.form["guest_id"]
        guest_name = request.form["guest_name"]
        email = request.form["email"]
        phone_num = request.form["phone_num"]

        # when phone num is NULL
        if phone_num == "":
            phone_num = None
            query = "UPDATE guests SET guest_name = %s, guests.email = %s, guests.phone_num = %s WHERE guest_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (guest_name, email, phone_num, guest_id))
            mysql.connection.commit()
            return redirect('/guests')

        # all inputs are entered (may need to error check for no inputs)
        else:
            query = "UPDATE guests SET guest_name = %s, email = %s, phone_num = %s WHERE guest_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (guest_name, email, phone_num, guest_id))
            mysql.connection.commit()
            return redirect('/guests')

# ATTRACTIONS CREATE AND READ ALL 
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

# ATTRACTION DELTE
@app.route("/delete_attraction/<int:ride_id>")
def delete_attraction(ride_id):
    query = "DELETE FROM attractions WHERE ride_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (ride_id,))
    mysql.connection.commit()
    return redirect('/attractions')

# ATTRACTION UPDATE
@app.route("/edit_attraction/<int:ride_id>", methods=["POST", "GET"])
def edit_attraction(ride_id):
    # all fields are required. guest_id is NULL-able
    if request.method == "GET":
        # First, we target the guest that we want to edit
        query = "SELECT * FROM attractions WHERE ride_id = '%s'" % (ride_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_attraction.j2", data=data)

    if request.method == "POST":
        # taking in edit attraction form inputs
        ride_id = request.form["ride_id"]
        ride_name = request.form["ride_name"]
        date_created = request.form["date_created"]
        num_riders = request.form["num_riders"]

        # all inputs are entered (may need to error check for no inputs)
        query = "UPDATE attractions SET date_created=(SELECT date FROM dates WHERE date=%s), ride_name = %s, num_riders = %s WHERE ride_id=%s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date_created, ride_name, num_riders, ride_id))
        mysql.connection.commit()
        return redirect('/attractions')

# ORDER TABLE CREATE AND READ ALL
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

# ORDER UPDATE
@app.route("/edit_order/<int:order_id>", methods=["POST", "GET"])
def edit_order(order_id):
    # all fields are required. guest_id is NULL-able
    if request.method == "GET":
        # First, we target the guest that we want to edit
        query = "SELECT * FROM orders WHERE order_id = '%s'" % (order_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_order.j2", data=data)

    if request.method == "POST":
        # taking in edit guest form inputs
        guest_id = request.form["guest_id"]
        date = request.form["date"]
        ticket = request.form["ticket"]
        season_pass_holder = request.form["season_pass_holder"]

        # all inputs are entered (may need to error check for no inputs)
        query = "UPDATE orders SET date=(SELECT date FROM dates WHERE date=%s), ticket=%s, season_pass_holder=%s, guest_id = (SELECT guest_id FROM guests WHERE guest_id=%s) WHERE order_id=%s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, ticket, season_pass_holder, guest_id, order_id))
        mysql.connection.commit()
        return redirect('/orders')


# ORDER DELETE
@app.route("/delete_order/<int:order_id>")
def delete_order(order_id):
    query = "DELETE FROM orders WHERE order_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (order_id,))
    mysql.connection.commit()
    return redirect('/orders')


# DATE TABLE CREATE AND READ ALL
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

# # DATE UPDATE
@app.route("/edit_date/<string:date>", methods=["POST", "GET"])
def edit_date(date):
    # all fields are required. guest_id is NULL-able
    if request.method == "GET":
        # First, we target the guest that we want to edit
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

        # all inputs are entered (may need to error check for no inputs)
        query = "UPDATE dates SET date=%s, day_of_week = %s, holiday = %s, weather = %s WHERE date = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, day_of_week, holiday, weather, date))
        mysql.connection.commit()
        return redirect('/dates')

# DATE DELETE
@app.route("/delete_date/<string:date>")
def delete_date(date):
    query = "DELETE FROM dates WHERE date = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query,(date,))
    mysql.connection.commit()
    return redirect('/dates')






# RIDES RIDDEN BY GUESTS CREATE AND READ
@app.route('/guests_has_attractions', methods=["POST", "GET"])
def guests_has_attractions():
    if request.method == "POST":
        ride_id = request.form["ride_id"]
        date_created = request.form["date_created"]
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

# # RIDES RIDDEN BY GUESTS DELETE
# @app.route("/delete_guest_has_attractions/<string:date>")
# def delete_date(date):
#     query = "DELETE FROM dates WHERE date = %s;"
#     cur = mysql.connection.cursor()
#     cur.execute(query,(date,))
#     mysql.connection.commit()
#     return redirect('/dates')

# master table CREATE AND READ ALL 
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

# # master table UPDATE
@app.route("/edit_table/<int:table_id>", methods=["POST", "GET"])
def edit_master_table(table_id):
    # all fields are required. guest_id is NULL-able
    if request.method == "GET":
        # First, we target the guest that we want to edit
        query = "SELECT * FROM master_table WHERE table_id = '%s'" % (table_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_table.j2", data=data)

    if request.method == "POST":
        table_id = request.form["table_id"]
        date = request.form["date"]
        total_guests = request.form["total_guests"]
        total_riders = request.form["total_riders"]

        # all inputs are entered (may need to error check for no inputs)
        query = "UPDATE master_table SET date=(SELECT date FROM dates WHERE date=%s), total_guests = %s, total_riders = %s WHERE table_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, total_guests, total_riders, table_id))
        mysql.connection.commit()
        return redirect('/master_table')

# master table DELETE
@app.route("/delete_table/<int:table_id>")
def delete_master_table(table_id):
    query = "DELETE FROM master_table WHERE table_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query,(table_id,))
    mysql.connection.commit()
    return redirect('/master_table')

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4785)) 
    app.run(port=port, debug=True)