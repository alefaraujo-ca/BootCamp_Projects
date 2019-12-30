from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (f"Welcome to Surf's Up!<br/>"
            f"------------------------------------------<br/><br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/stations<br/>"
            f">>>>>>>>>>>>: List of all weather observation stations<br/><br/>"
            f"/api/v1.0/precipitation<br/>"
            f">>>>>>>>>>>>: The latest year of precipitation data<br/><br/>"
            f"/api/v1.0/tobs<br/>"
            f">>>>>>>>>>>>: The latest year of temperature observation data<br/><br/>"
            f"/api/v1.0/date_search/yyyy-mm-dd <br/>"
            f">>>>>>>>>>>>: Low, high, and average temperature after a given date<br/><br/>"
            f"/api/v1.0/date_search/yyyy-mm-dd/yyyy-mm-dd <br/>"
            f">>>>>>>>>>>>: Low, high, and average temperature for a given period<br/>"
    )


# unpack a tuple using list comprehensions
# { date:temp for k,v in tuple }
# or -- same code with for loop
# dict = {}
# for x in tuple
#     date, temp = x
#     dict[date] = temp


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(str(last_date[0]), '%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores
    year_ago = last_date - dt.timedelta(days=365)

    prcp_results = session.query(Measurement.date, Measurement.prcp) \
        .filter(Measurement.date >= year_ago). \
        order_by(Measurement.date.asc()).all()

    return jsonify({k: v for k, v in prcp_results})


@app.route("/api/v1.0/stations")
def stations():
    ''' do code '''
    station_results = session.query(Station.station, Station.name).all()

    return jsonify({k: v for k, v in station_results})


@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(str(last_date[0]), '%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores
    year_ago = last_date - dt.timedelta(days=365)

    tobs_results = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.date >= year_ago). \
        order_by(Measurement.date.asc()).all()

    return jsonify({k: v for k, v in tobs_results})


@app.route('/api/v1.0/date_search/<start_date>')
def start(start_date):
    sel = [func.strftime("%Y-%m", Measurement.date),
           func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = (session.query(*sel)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)
               .group_by(func.strftime("%Y-%m", Measurement.date))
               .all())

    dates = []
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low"] = result[1]
        date_dict["Avg"] = result[2]
        date_dict["High"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)


@app.route('/api/v1.0/date_search/<start_date>/<end_date>')
def period(start_date, end_date):
    sel = [func.strftime("%Y-%m", Measurement.date),
           func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = (session.query(*sel)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date)
               .group_by(func.strftime("%Y-%m", Measurement.date))
               .all())

    dates = []
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low"] = result[1]
        date_dict["Avg"] = result[2]
        date_dict["High"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)


if __name__ == '__main__':
    app.run(debug=True)
