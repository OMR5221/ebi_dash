#server_flask_restless
import flask
from flask import Flask, send_from_directory, request, jsonify
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey, Numeric, cast, func, create_engine)
from sqlalchemy.ext.automap import automap_base
# import flask.ext.sqlalchemy
from flask_sqlalchemy import SQLAlchemy
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

import io
import csv
from psycopg2 import sql

#from adhoc import query_models

engine = sa.create_engine('mssql+pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0')
# create an unbound base our objects will inherit from
Base = declarative_base()
metadata = MetaData(bind=engine)
Base.metadata = metadata
g = globals()
metadata.reflect()
Session = sessionmaker(bind=engine)
session = Session()

def intersect(lst1, lst2):
    return list(set(lst1) & set(lst2))

def reflect_all_tables_to_declarative(wanted_tables):
    """Reflects all tables to declaratives

    Given a valid engine URI and declarative_base base class
    reflects all tables and imports them to the global namespace.

    Returns a session object bound to the engine created.
    """

    # create an unbound base our objects will inherit from
    #Base = declarative_base()

    #engine = sa.create_engine(uri)
    #metadata = MetaData(bind=engine)
    #Base.metadata = metadata

    #g = globals()

    #metadata.reflect()
    
    for tablename, tableobj in metadata.tables.items():
        try:
            if tablename in wanted_tables:
                g[tablename] = type(str(tablename), (Base,), {'__table__' : tableobj, '__tablename__' : str(tablename)})
                print("Reflecting {0}".format(tablename))
        except sa.exc.ArgumentError:
            print("Missing Primary Key: {0}".format(tablename))
            for col in tableobj.c:
                #if re.match(".*sk", str(col), re.I):
                print(col)
                # print(re.match('*SK', col))
            g[tablename] = type(str(tablename), (Base,), 
                                {'__table__' : tableobj,
                                 '__tablename__' : tablename,
                                 '__mapper_args__' : {
                                        'primary_key': [col for col in tableobj.c if re.match(".*sk", str(col), re.I)]
                                        #PrimaryKeyConstraint(re.match(r'*SK', tablename, re.I))
                                     }
                                })
            #for col in (metadata.tables[tablename]).columns:
            #    print(col)
    
    #return session
        

def camelize_classname(base, tablename, table):
    "Produce a 'camelized' class name, e.g. "
    "'words_and_underscores' -> 'WordsAndUnderscores'"

    return str(tablename[0].upper() + \
            re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))

_pluralizer = inflect.engine()
def pluralize_collection(base, local_cls, referred_cls, constraint):
    "Produce an 'uncamelized', 'pluralized' class name, e.g. "
    "'SomeTerm' -> 'some_terms'"

    referred_name = referred_cls.__name__
    uncamelized = re.sub(r'[A-Z]',
                         lambda m: "_%s" % m.group(0).lower(),
                         referred_name)[1:]
    pluralized = _pluralizer.plural(uncamelized)
    return pluralized


def make_aggs():

    # Custom aggregation query classes:
    class VW_INT_Agg_MonthlyDonorsPerLocation(Base):
        __tablename__ = 'VW_INT_Agg_MonthlyDonorsPerLocation'
        __table_args__ = {'useexisting': True} 
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        regionID = Column(Integer())
        locationName = Column(String(100), index=True)
        donationType = Column(String(50))
        yearmonthNum = Column(Integer())
        yearmonthName = Column(String(20))
        numDonors = Column(Integer())
        
        def __init__(self, reg_id, loc_name, don_desc, ym_num, ym_name, num_dons):
            self.regionID = reg_id
            self.locationName = loc_name
            self.donationType = don_desc
            self.yearmonthNum = ym_num
            self.yearmonthName = ym_name
            self.numDonors = num_dons
            
        def save(self):
            session.add(self)
            session.commit()
            
        @staticmethod
        def get_all():
            return NumDonorsLoc.query.all()
            
        def delete(self):
            session.delete(self)
            session.commit()
            
        def __repr__(self):
            return "NumDonorsLoc(region_id={self.regionID}, " \
            "location_name='{self.locationName}', " \
            "donation_type='{self.donationType}', " \
            "yearmonth_num='{self.yearmonthNum}', " \
            "yearmonth_name='{self.yearmonthName}', " \
            "num_donors={self.numDonors})".format(self=self)
        
<<<<<<< HEAD
    # Create the Agg Tables:
    VW_INT_Agg_MonthlyDonorsPerLocation.__table__.create(engine, checkfirst=True)
    VW_INT_Agg_DailyDonorsPerLocation.__table__.create(engine, checkfirst=True)
=======
    VW_INT_Agg_MonthlyDonorsPerLocation.__table__.create(engine, checkfirst=True)
>>>>>>> parent of 93596f5... 10032018: Added Daily Donor Table
    
    print("Query run START")
    donDetails = (session.query((INT_DIMLocation.RegionID).label('regionID'),
    (INT_DIMLocation.FinanceLocationName).label('locationName'),
    (Int_DimDonationType.DonationDescription).label('donationType'),
    cast((DimDate.Year+DimDate.Month),Integer).label('yearmonthNum'),
    (DimDate.MonthYear).label('yearmonthName'),
    func.count(INT_MKTCollectionDetails.personid).label('numDonors'))
    .filter(INT_MKTCollectionDetails.LocationSK == INT_DIMLocation.LocationSK)
    .filter(INT_MKTCollectionDetails.DonationTypeSK == Int_DimDonationType.DonationTypeSk)
    .filter(INT_MKTCollectionDetails.CollectionDateSK == DimDate.DateKey)
    .group_by(INT_DIMLocation.RegionID, INT_DIMLocation.FinanceLocationName, Int_DimDonationType.DonationDescription, cast((DimDate.Year+DimDate.Month),Integer),DimDate.MonthYear).all())
    
    print("Query run END")
    
    dd_list = []

    print("TABLE LOAD START")
<<<<<<< HEAD
    
    print("CREATING MONTHLY OBJECTS")
    for md in monthlyDonDetails:
        nr = VW_INT_Agg_MonthlyDonorsPerLocation(md[0], md[1], md[2], md[3], md[4], md[5])
        md_tp.append(nr)
    print("CREATING DAILY OBJECTS")    
    for dd in dailyDonDetails:
        nr = VW_INT_Agg_DailyDonorsPerLocation(dd[0], dd[1], dd[2], dd[3], dd[4], dd[5])
        dd_tp.append(nr)

    print("SESSION SAVE 1")
    session.bulk_save_objects(md_tp)
    print("SESSION SAVE 2")
    session.bulk_save_objects(dd_tp)
    print("SESSION COMMIT")
=======
    # list of tuples
    for dd in donDetails:
        nr = VW_INT_Agg_MonthlyDonorsPerLocation(dd[0], dd[1], dd[2], dd[3], dd[4], dd[5])
        dd_list.append(nr)

    session.bulk_save_objects(dd_list)
>>>>>>> parent of 93596f5... 10032018: Added Daily Donor Table
    session.commit()
    print("TABLE LOAD END")

    print(dd_list[0])
    
# Create the Flask application and the Flask-sqlalchemy object:
app = flask.Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://ORLEBIDEVDB/INTEGRATION?driver=SQL+Server+Native+Client+11.0'
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"

# Expose the url route /api/ to requests from any origin:
app.config['CORS_RESOURCES'] = {r"/api/*" : {"origins" : "*"}}

reflect_all_tables_to_declarative(['INT_MKTCollectionDetails', 'INT_DIMLocation', 'Int_DimDonationType', 'DimDate'])

make_aggs()

reflect_all_tables_to_declarative(['VW_INT_Agg_MonthlyDonorsPerLocation'])

# ddList = session.query(VW_INT_Agg_MonthlyDonorsPerLocation).all()

db = SQLAlchemy(app)

cors = CORS(app)

# print(type(db))

# Create the Flask-Restless API Manager:
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at
# localhost:####/api/<tablename> by default
# Allowed HTTP methods can be specified as well:
manager.create_api(VW_INT_Agg_MonthlyDonorsPerLocation, methods=['GET'],max_results_per_page=1000) # Limit max results to 1000
 
app.run()
