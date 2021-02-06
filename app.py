import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
import sys


##################################################################
#
# SQLalchemy Challenge      due 8-Feb-2021
#       Kate Spitzer
#
# This script uses Flask to create a simple web application
# that has a few simple routes which access the hawaii.sqlite
# database.
#
#       /api/v1.0/precipitation
#           - returns a JSON dictionary of all precipitation data
#               from the measurement table using date as the key
#               and prcp as the value.
#       /api/v1.0/stations
#           - returns a JSON list of all stations found in the
#               stations table.
#       /api/v1.0/tobs
#           - returns a JSON list of all temperature observation
#               data found in the measurement table.
#       /api/v1.0/start_date
#           - returns a JSON list containing the minimum temperature,
#               the average temperature, and the maximum temperature
#               from the measurement table for all dates beginning
#               at the start date entered and later.
#       /api/v1.0/start_date/end_date
#           - returns a JSON list containing the minimum temperature,
#               the average temperature, and the maximum temperature
#               from the measurement table for all dates between the
#               start date and end date entered, inclusive.
#
##################################################################

# build path to sqlite database
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
# root page
#################################################
@app.route("/")
def welcome():
    """  List all available api routes.  """
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

######################
# precipitation route
######################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """  CreateReturn a dictionary of precipitation data  """
    # Query all precipitation data
    results = session.query(Measurement.date,\
            Measurement.prcp).all()

    session.close()

    # create a dictionary from the query results
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

######################
# station route
######################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """  Return a list of station names  """
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Create a list of stations
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


################################
# temperature observation route
################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """  Return a list of observed temperatures for the most active station for the most current year  """    
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

    # retrieve all rows for the station for the most current year
    results = session.query(Measurement.tobs).\
            filter(Measurement.station == busy_station).\
            filter(Measurement.date > min_date).all()

    session.close()

    # create a list of temperatures
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


##################################
# aggregate temps with start date
##################################
@app.route("/api/v1.0/<start>")
def start_date(start):

    """  Calculate the low temp, average temp, and high temp starting at the date entered  """

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query data to calculate stats for date greater than or equal to date entered
    stats_with_start = session.query(func.min(Measurement.tobs),\
                        func.avg(Measurement.tobs),\
                        func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).all()
    session.close()

    # create a list with results
    stat_list = [stats_with_start[0][0], round(stats_with_start[0][1], 2), stats_with_start[0][2]]


    return jsonify(stat_list)




@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query data to calculate stats for date within range entered
    stats_with_range = session.query(func.min(Measurement.tobs),\
                        func.avg(Measurement.tobs),\
                        func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()
    session.close()

    # create a list with results
    stat_list = [stats_with_range[0][0], round(stats_with_range[0][1], 2), stats_with_range[0][2]]

    return jsonify(stat_list)



# execute main
if __name__ == '__main__':
    app.run(debug=False)
