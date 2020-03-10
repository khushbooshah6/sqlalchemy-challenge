import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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

# Create session (link)  to the DB
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
        f"<h2><font color='purple'>Welcome to Flask App On Hawaiian Data Analysis</font><h2><br/>"
        f"<h5>Available Routes:<h5><br/>"
        f"<font size='10'>/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end></font>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    getData =  session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    precipitation_dictionary = {}

    def ToDictionary(Tup,Dicty):
        for first,second in Tup:
            Dicty.setdefault(first,[]).append(second)
        return Dicty

    return jsonify(precipitation_dictionary)

def calculatedtemps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """

    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(
            Measurement.date <= end_date).all()

@app.route("/api/v1.0/stations")
def stations():
    getData =  session.query(Station.station).all()
    getData = list(np.ravel(getData))
    return jsonify(getData)

@app.route("/api/v1.0/tobs")
def tobs():
    getData =  session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    getData = list(np.ravel(getData))
    return jsonify(getData)

@app.route("/api/v1.0/<start>")
def startdate(start):
    EndDate = session.query(func.max(Measurement.date)).all()[0][0]
    Temperatures = calc_temps(start, EndDate)
    TemperatureList = list(np.ravel(Temperatures))
    return jsonify(TemperatureList)

@app.route("/api/v1.0/<start>/<end>")
def enddate(start, end):
    Temperatures = calc_temps(start, end)
    TemperatureList = list(np.ravel(Temperatures))
    return jsonify(TemperatureList)


if __name__ == '__main__':
    app.run(debug=True)
