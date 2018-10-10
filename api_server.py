#server_flask_restless
import flask
from flask import Flask, send_from_directory, request, jsonify
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey, Numeric, cast, func, create_engine)
from sqlalchemy.ext.automap import automap_base
# import flask.ext.sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# import flask.ext.restless
import flask_restless
import re
import inflect
from flask_cors import CORS
import pickle
import json

import scipy
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Amazon S3 service:
import boto3

# Get our custom models for queries:
# from adhoc import query_models

from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
# 3rd party moudles
from flask import render_template

# local modules
import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api('ebiSwagger.yml')

# create a URL route in our application for "/"
@connex_app.route('/')
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


if __name__ == '__main__':
    connex_app.run(debug=True)