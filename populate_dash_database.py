import os
from config import db
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
import os
import scipy
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Amazon S3 service:
import boto3

# Get our custom models for queries:
# from adhoc import query_models

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from models import *


def reflect_all_tables_to_declarative(wanted_tables):
    """Reflects all tables to declaratives
    Given a valid engine URI and declarative_base base class
    reflects all tables and imports them to the global namespace.
    Returns a session object bound to the engine created.
    """
    
    for uri, tables in wanted_tables.items():
    
        # create an unbound base our objects will inherit from
        Base = declarative_base()
        engine = sa.create_engine(uri)
        metadata = MetaData(bind=engine)
        Base.metadata = metadata

        #g = globals()

        metadata.reflect()
        
        for tablename, tableobj in metadata.tables.items():
            try:
                if tablename in tables:
                    g[tablename] = type(str(tablename.replace(" ", "")), (Base,), {'__table__' : tableobj, '__tablename__' : str(tablename.replace(" ", ""))})
                    print("Reflecting {0}".format(tablename))
            except sa.exc.ArgumentError:
                print("Missing Primary Key: {0}".format(tablename))
                for col in tableobj.c:
                    #if re.match(".*sk", str(col), re.I):
                    print(col)
                    # print(re.match('*SK', col))
                print("Reflecting {0}".format(tablename))    
                g[str(tablename.replace(" ", ""))] = type(str(tablename.replace(" ", "")), (Base,), 
                                    {'__table__' : tableobj,
                                     '__tablename__' : str(tablename.replace(" ", "")),
                                     '__mapper_args__' : {
                                            'primary_key': [col for col in tableobj.c if re.match(".*sk|.*key", str(col), re.I)]
                                            #PrimaryKeyConstraint(re.match(r'*SK', tablename, re.I))
                                         }
                                    })
                                
    Session = sessionmaker()
    return Session()

def pop_monthlyDonors():
        
    VW_INT_Agg_MonthlyDonorsPerLocation.__table__.create(output_engine, checkfirst=True)
    
    print("Query run START")
    donMonthlyDetails = (inputsession.query((INT_DIMLocation.RegionID).label('regionID'),
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
    
    md_list = []

    print("TABLE LOAD START")
    # list of tuples
    for md in donMonthlyDetails:
        nr = VW_INT_Agg_MonthlyDonorsPerLocation(md[0], md[1], md[2], md[3], md[4], md[5])
        md_list.append(nr)

    outputsession.bulk_save_objects(md_list)
    outputsession.commit()
    print("TABLE LOAD END")

    print(md_list[0])
    

def pop_dailyDonors():
        
    VW_INT_Agg_DailyDonorsPerLocation.__table__.create(output_engine, checkfirst=True)
    
    print("Query run START")
    donDailyDetails = (inputsession.query((INT_DIMLocation.RegionID).label('regionID'),
    (INT_DIMLocation.FinanceLocationName).label('locationName'),
    (Int_DimDonationType.DonationDescription).label('donationType'),
    (DimDate.DateKey).label('yearmonthdayNum'),
    (DimDate.FullDateUSA).label('yearmonthdayName'),
    func.count(INT_MKTCollectionDetails.personid).label('numDonors'))
    .filter(INT_MKTCollectionDetails.LocationSK == INT_DIMLocation.LocationSK)
    .filter(INT_MKTCollectionDetails.DonationTypeSK == Int_DimDonationType.DonationTypeSk)
    .filter(INT_MKTCollectionDetails.CollectionDateSK == DimDate.DateKey)
    .group_by(INT_DIMLocation.RegionID, INT_DIMLocation.FinanceLocationName, Int_DimDonationType.DonationDescription, DimDate.DateKey,DimDate.FullDateUSA).all())
    
    print("Query run END")
    
    dd_list = []

    print("TABLE LOAD START")
    # list of tuples
    for dd in donDailyDetails:
        nr = VW_INT_Agg_DailyDonorsPerLocation(dd[0], dd[1], dd[2], dd[3], dd[4], dd[5])
        dd_list.append(nr)

    outputsession.bulk_save_objects(dd_list)
    outputsession.commit()
    print("TABLE LOAD END")

    print(dd_list[0])
    
    
def pop_yearlyDonorsbyCounty():
        
    VW_INT_Agg_YearlyDonorsbyCounty.__table__.create(output_engine, checkfirst=True)
    
    print("Query run START")
    donCountyYearly = (inputsession.query((DimDate.Year).label('year'),
    func.min(STG_HEMAZipCodeMaster.Longitude).label('minLong'),
    func.max(STG_HEMAZipCodeMaster.Longitude).label('maxLong'),
    func.min(STG_HEMAZipCodeMaster.Latitude).label('minLat'),
    func.max(STG_HEMAZipCodeMaster.Latitude).label('maxLat'),
    (STG_HEMAZipCodeMaster.CountyCode).label('FIPS'),
    (STG_HEMAZipCodeMaster.CountyName).label('CountyName'),
    func.count(INT_MKTCollectionDetails.personid).label('numDonors'))
	.filter(STG_HEMAZipCodeMaster.ZipCode == INT_MKTCollectionDetails.PersonZipCode)
    .filter(INT_MKTCollectionDetails.LocationSK == INT_DIMLocation.LocationSK)
    .filter(INT_MKTCollectionDetails.DonationTypeSK == Int_DimDonationType.DonationTypeSk)
    .filter(INT_MKTCollectionDetails.CollectionDateSK == DimDate.DateKey)
    .group_by(DimDate.Year,STG_HEMAZipCodeMaster.CountyCode,STG_HEMAZipCodeMaster.CountyName).all())
    
    print("Query run END")
    
    cy_list = []

    print("TABLE LOAD START")
    # list of tuples
    for cy in donCountyYearly:
        nr = VW_INT_Agg_YearlyDonorsbyCounty(cy[0], cy[1], cy[2], cy[3],cy[4], cy[5], cy[6], cy[7])
        cy_list.append(nr)

    outputsession.bulk_save_objects(cy_list)
    outputsession.commit()
    print("TABLE LOAD END")

    print(dd_list[0])

    
# Begin main processing:
basedir = os.path.abspath(os.path.dirname(__file__))
 
SQLALCHEMY_BINDS = {
    'input_int': 'mssql+pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0',
    'input_stg': 'mssql+pyodbc://ORLEBIDEVDB/STAGE?driver=SQL+Server+Native+Client+11.0',
    'output': 'sqlite:///' + os.path.join(basedir, 'ebidash.db')
}
input_int_engine = sa.create_engine('mssql+pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0')
input_stg_engine = sa.create_engine('mssql+pyodbc://ORLEBIDEVDB/STAGE?driver=SQL+Server+Native+Client+11.0')
output_engine = sa.create_engine('sqlite:///' + os.path.join(basedir, 'ebidash.db'))
# create an unbound base our objects will inherit from
Base = declarative_base()
metadata = MetaData()
# metadata.reflect(bind=input_int_engine)
# metadata.reflect(bind=input_stg_engine)
# metadata = MetaData(bind=input_int_engine)
# metadata = MetaData(bind=input_stg_engine)
#Base.metadata = metadata
g = globals()
#metadata.reflect()
# InputIntSession = sessionmaker(bind=input_int_engine)
# InputSession = sessionmaker(bind=input_stg_engine)
# inputsession = InputIntSession()

wanted_tables_dict = {
    SQLALCHEMY_BINDS['input_int']: ['INT_MKTCollectionDetails', 'INT_DIMLocation', 'Int_DimDonationType', 'DimDate'], 
    SQLALCHEMY_BINDS['input_stg']: ['STG_HEMAZipCodeMaster']
}

inputsession = reflect_all_tables_to_declarative(wanted_tables_dict)

# do something with the session and the orm objects
results = inputsession.query(STG_HEMAZipCodeMaster).all()
print("STG_HEMAZipCodeMaster:")
for result in results:
	print(result)
	
# do something with the session and the orm objects
results = inputsession.query(DimDate).all()
print("DIMDATE:")
for result in results:
	print(result)

OutputSession = sessionmaker(bind=output_engine)
outputsession = OutputSession()

print("Build Monthly")
pop_monthlyDonors()
print("Build Daily")
pop_dailyDonors()
print("Build County Donor Count")
pop_yearlyDonorsbyCounty()

reflect_all_tables_to_declarative(['VW_INT_Agg_MonthlyDonorsPerLocation', 'VW_INT_Agg_DailyDonorsPerLocation', 'VW_INT_Agg_YearlyDonorsbyCounty'])
