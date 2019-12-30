import datetime

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
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
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(str(lastdate[0]), '%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores
    yearago = lastdate - dt.timedelta(days=365)

    prcp_results = session.query(Measurement.date, Measurement.prcp) \
        .filter(Measurement.date >= yearago). \
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
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(str(lastdate[0]), '%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores
    yearago = lastdate - dt.timedelta(days=365)

    tobs_results = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.date >= yearago). \
        order_by(Measurement.date.asc()).all()

    return jsonify({k: v for k, v in tobs_results})


# You can have 2 routes to one function
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def names(start=None, end=None):
    #start_date = dt.strptime(start, "%Y-%m-%d").date()
    if end is not None:
        results = dict(session.query(func.min(Measurement.tobs),
                                     func.max(Measurement.tobs),
                                     func.avg(Measurement.tobs)). \
                       filter(Measurement.date >= start).filter(Measurement.date <= end). \
                       all())
    else:
        results = dict(session.query(func.min(Measurement.tobs),
                                     func.max(Measurement.tobs),
                                     func.avg(Measurement.tobs)). \
                       filter(Measurement.date >= start). \
                       all())

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
