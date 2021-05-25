import numpy as np
from datetime import datetime as dt, timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(bind = engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f'Available Routes: <br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start>/<end>'

    )
#hard coding date from analysis notebook
@app.route("/api/v1.0/precipitation")
def temps_to_dict():
    date_converted = dt.strptime('2017-08-23',"%Y-%m-%d")
    year_previous = date_converted - timedelta(days = 365)
    year_previous
    scores = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date <= date_converted, measurement.date > year_previous).\
            order_by(measurement.date).all()
    #converting to dictionary
    dates_list = []
    prcp_list = []

    for score in scores:
        dates_list.append(score[0])
        prcp_list.append(score[1])

    temps_dict = {
        'Date' : dates_list,
        'Precipitation' : prcp_list
    }
    return temps_dict

@app.route("/api/v1.0/stations")
def stations_list():
    stations = session.query(measurement.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def dates_temperature():
    temps = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').all()
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def startend(start):
    start_date = dt.datetime.strptime(start , '%Y-%m-%d')
    tmax = session.query(func.max(measurement.tobs)).\
        filter (measurement.date == start_date).all()
    tmin = session.query(func.min(measurement.tobs)) .\
    filter (measurement.date == start_date).all()
    tavg = session.query(func.avg(measurement.tobs)) .\
        filter (measurement.date == start_date).all()

    temp_dict = ({
        'TMAX' : tmax,
        'TMIN' : tmin,
        'TAVG' : tavg
    })
    
    

if __name__ == '__main__':
    app.run(debug=True)
