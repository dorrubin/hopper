# File: app.py
# Author: Dor Rubin
from flask import Flask
from flask import request, render_template
from IPython import embed
import json
from flaskext.mysql import MySQL


# MYSQL CONFIG
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toor'
app.config['MYSQL_DATABASE_DB'] = 'hopper'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

mysql.init_app(app)
conn = mysql.connect()


def updateJSON(rows, start_date):
    """ Re-write the json file
    Update the events.json file with the flights that matched the query
    """
    objects_list = []
    for row in rows:
        d = {}
        d['title'] = str(row[1])
        d['start'] = row[0].strftime('%Y-%m-%d')
        price = float(row[1])
        if price < 300:
            color = "green"
        elif price < 400:
            color = "#EEB90F"
        else:
            color = "red"
        d['color'] = color
        objects_list.append(d)
    if start_date:
        d = {}
        d['title'] = 'SELECTED DATE'
        d['start'] = start_date
        d['color'] = "blue"
        objects_list.append(d)
    with open('events.json', 'w') as fp:
        json.dump(objects_list, fp)


def getDeparting(start_date, end_date):
    """ Get the data for all flight departing within range
    For each departure time within range, select the minimum for each day
    """
    cursor = conn.cursor()
    query = """SELECT departure_odate, MIN(total_usd)
                FROM flights
                WHERE date(departure_odate) BETWEEN date('{0}') and date('{1}')
                GROUP BY departure_odate
                ORDER BY departure_odate;
             """.format(start_date, end_date)
    cursor.execute(query)
    data = cursor.fetchall()
    updateJSON(data, '')


def getReturning(start_date):
    """ Get the data for all flight returning given departure date
    For each flight with a departure time equal to the one selected,
    Return the minimum cost for each day
    """
    cursor = conn.cursor()
    query = """SELECT return_odate, MIN(total_usd)
                FROM flights
                WHERE date(departure_odate) = date('{0}')
                GROUP BY return_odate
                ORDER BY return_odate;
             """.format(start_date)
    cursor.execute(query)
    data = cursor.fetchall()
    updateJSON(data, start_date)


@app.route('/')
def calendar():
    """ Render index.html
    """
    return render_template("index.html")


@app.route('/data')
def return_data():
    """ GET Route for populating the calendar
    """
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    selected_date = request.args.get('selection', '')
    if selected_date:
        getReturning(selected_date)
    else:
        getDeparting(start_date, end_date)
    # pass the new events.json file to the frontend
    with open("events.json", "r") as input_data:
        return input_data.read()


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
