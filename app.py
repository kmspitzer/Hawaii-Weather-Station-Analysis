import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
import sys

print(os.path.dirname(__file__))

root_project_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, root_project_path)

hawaii_path = os.path.join(root_project_path, "Resources/hawaii.sqlite")


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///"+hawaii_path)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date,\
            Measurement.prcp).all()

    session.close()

    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
     # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))


    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""    
    # Find the most recent date in the data set
    max_date = session.query(func.max(Measurement.date)).scalar()

    # calculate the date 1 year earlier
    date_split = max_date.split("-")
    min_date = dt.date(int(date_split[0]), int(date_split[1]), int(date_split[2])) - dt.timedelta(days=365)

    # pull only the most active station 
    stn_query = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()

    busy_station = stn_query.station
#
 
    results = session.query(Measurement.tobs).\
            filter(Measurement.station == busy_station).\
            filter(Measurement.date > min_date).all()

    session.close()

    all_tobs = list(np.ravel(results))

    # Create a dictionary from the row data and append to a list of all_passengers
#    all_passengers = []
#    for name, age, sex in results:
#        passenger_dict = {}
#        passenger_dict["name"] = name
#        passenger_dict["age"] = age
#        passenger_dict["sex"] = sex
#        all_passengers.append(passenger_dict)

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=False)