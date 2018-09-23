#server_flask_restless
import flask
from flask import Flask, send_from_directory, request, jsonify
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey, Numeric, cast, func)
from sqlalchemy.ext.automap import automap_base
# import flask.ext.sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# import flask.ext.restless
import flask_restless
import re
import inflect
from flask_cors import CORS
import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re
import pickle
import json

import scipy
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Amazon S3 service:
import boto3

# Get our custom models for queries:
from app import query_models

def intersect(lst1, lst2):
    return list(set(lst1) & set(lst2))

def reflect_all_tables_to_declarative(uri):
    """Reflects all tables to declaratives

    Given a valid engine URI and declarative_base base class
    reflects all tables and imports them to the global namespace.

    Returns a session object bound to the engine created.
    """

    # create an unbound base our objects will inherit from
    Base = declarative_base()

    engine = sa.create_engine(uri)
    metadata = MetaData(bind=engine)
    Base.metadata = metadata

    g = globals()

    metadata.reflect()
    
    wanted_tables = ['INT_MKTCollectionDetails', 'INT_DIMLocation', 'Int_DimDonationType', 'DimDate']

    for tablename, tableobj in metadata.tables.items():
        try:
            if tablename in wanted_tables:
                g[tablename] = type(str(tablename), (Base,), {'__table__' : tableobj, '__tablename__' : tablename })
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

    Session = sessionmaker(bind=engine)
    return Session()
		

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

	
# Create the Flask application and the Flask-sqlalchemy object:
app = flask.Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://ORLEBIDEVDB/INTEGRATION?driver=SQL+Server+Native+Client+11.0'
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"

# Expose the url route /api/ to requests from any origin:
app.config['CORS_RESOURCES'] = {r"/api/*" : {"origins" : "*"}}

# engine = sa.create_engine('mssql+pyodbc://ORLEBIDEVDB/INTEGRATION?driver=SQL+Server+Native+Client+11.0')

#metadata = MetaData()
#metadata.reflect(bind=engine)

# we can reflect it ourselves from a database, using options
# such as 'only' to limit what tables we look at...
#metadata.reflect(engine, only=['INT_MKTCollectionDetails'])

session = reflect_all_tables_to_declarative('mssql+pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0')


# mktCollects = Table('mktCollects', metadata, autoload=True, autoload_with=engine)
#print(type(mktCollects))

# we can then produce a set of mappings from this MetaData.
#Base = automap_base(metadata=metadata)

#Base.prepare()

# calling prepare() just sets up mapped classes and relationships.
#Base.prepare(engine, reflect=True)
			#classname_for_table=camelize_classname,
            #name_for_collection_relationship=pluralize_collection)

# mapped classes are now created with names by default
# matching that of the table name.
#mktCollects = Base.classes.INT_MKTCollectionDetails

# session = Session(engine)

donDetails = (session.query(INT_DIMLocation.RegionID,
INT_DIMLocation.FinanceLocationName,
Int_DimDonationType.DonationDescription,
cast((DimDate.Year+DimDate.Month),Integer).label('yyyymm'),
DimDate.MonthYear,
func.count(INT_MKTCollectionDetails.personid).label('numDonors'))
.filter(INT_MKTCollectionDetails.LocationSK == INT_DIMLocation.LocationSK)
.filter(INT_MKTCollectionDetails.DonationTypeSK == Int_DimDonationType.DonationTypeSk)
.filter(INT_MKTCollectionDetails.CollectionDateSK == DimDate.DateKey)
.group_by(INT_DIMLocation.RegionID, INT_DIMLocation.FinanceLocationName, Int_DimDonationType.DonationDescription, cast((DimDate.Year+DimDate.Month),Integer),DimDate.MonthYear).all())

db = SQLAlchemy(app)

cors = CORS(app)

# print(type(db))

# Create the Flask-Restless API Manager:
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at
# localhost:####/api/<tablename> by default
# Allowed HTTP methods can be specified as well:
manager.create_api(donDetails, methods=['GET'],max_results_per_page=1000) # Limit max results to 1000
 
app.run()