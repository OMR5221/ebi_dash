import os
from config import db
from models import *


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
								

def populate_splite_tables():

	# Get data to intialize and populate Tables:
	dailyDonorDetails = (session.query((INT_DIMLocation.RegionID).label('regionID'),
	(INT_DIMLocation.FinanceLocationName).label('locationName'),
	(Int_DimDonationType.DonationDescription).label('donationType'),
	cast((DimDate.DateKey),Integer).label('yearmonthdayNum'),
	(DimDate.FullDateUSA).label('yearmonthdayName'),
	func.count(INT_MKTCollectionDetails.personid).label('numDonors'))
	.filter(INT_MKTCollectionDetails.LocationSK == INT_DIMLocation.LocationSK)
	.filter(INT_MKTCollectionDetails.DonationTypeSK == Int_DimDonationType.DonationTypeSk)
	.filter(INT_MKTCollectionDetails.CollectionDateSK == DimDate.DateKey)
	.group_by(INT_DIMLocation.RegionID, INT_DIMLocation.FinanceLocationName, Int_DimDonationType.DonationDescription, DimDate.DateKey,DimDate.FullDateUSA).all())

	"""
	# Get data to intialize and populate Tables:
	monthlyDonDetails = (session.query((INT_DIMLocation.RegionID).label('regionID'),
	(INT_DIMLocation.FinanceLocationName).label('locationName'),
	(Int_DimDonationType.DonationDescription).label('donationType'),
	cast((DimDate.Year+DimDate.Month),Integer).label('yearmonthNum'),
	(DimDate.MonthYear).label('yearmonthName'),
	func.count(INT_MKTCollectionDetails.personid).label('numDonors'))
	.filter(INT_MKTCollectionDetails.LocationSK == INT_DIMLocation.LocationSK)
	.filter(INT_MKTCollectionDetails.DonationTypeSK == Int_DimDonationType.DonationTypeSk)
	.filter(INT_MKTCollectionDetails.CollectionDateSK == DimDate.DateKey)
	.group_by(INT_DIMLocation.RegionID, INT_DIMLocation.FinanceLocationName, Int_DimDonationType.DonationDescription, cast((DimDate.Year+DimDate.Month),Integer),DimDate.MonthYear).all())
	"""


	# Delete database file if it exists currently
	if os.path.exists('ebidash.db'):
		os.remove('ebidash.db')

	# Create the database and tables?
	db.create_all()

	# iterate over the PEOPLE structure and populate the database
	dd_list = []

	print("TABLE LOAD START")
	# list of tuples
	for dd in dailyDonDetails:
		nr = VW_INT_Agg_MonthlyDonorsPerLocation(dd[0], dd[1], dd[2], dd[3], dd[4], dd[5])
		dd_list.append(nr)

	db.session.bulk_save_objects(dd_list)
	db.session.commit()


in_engine = sa.create_engine('mssql+pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0')
# create an unbound base our objects will inherit from
Base = declarative_base()
metadata = MetaData(bind=engine)
Base.metadata = metadata
g = globals()
metadata.reflect()
Session = sessionmaker(bind=engine)
session = Session()
  	

reflect_all_tables_to_declarative(['INT_MKTCollectionDetails', 'INT_DIMLocation', 'Int_DimDonationType', 'DimDate'])