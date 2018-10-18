from datetime import datetime
from config import db, ma
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey, Numeric, cast, func, create_engine)


class VW_INT_Agg_MonthlyDonorsPerLocation(db.Model):
	__tablename__ = 'VW_INT_Agg_MonthlyDonorsPerLocation'
	__table_args__ = {'useexisting': True}
	#__bind_key__ = 'output'

	id = db.Column(Integer, primary_key=True, autoincrement=True)
	regionID = db.Column(Integer())
	locationName = db.Column(String(100), index=True)
	donationType = db.Column(String(50))
	yearmonthNum = db.Column(Integer())
	yearmonthName = db.Column(String(20))
	numDonors = db.Column(Integer())

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
		return VW_INT_Agg_MonthlyDonorsPerLocation.query.all()
		
	def delete(self):
		session.delete(self)
		session.commit()
		
	def __repr__(self):
		return "VW_INT_Agg_MonthlyDonorsPerLocation(region_id={self.regionID}, " \
		"location_name='{self.locationName}', " \
		"donation_type='{self.donationType}', " \
		"yearmonth_num='{self.yearmonthNum}', " \
		"yearmonth_name='{self.yearmonthName}', " \
		"num_donors={self.numDonors})".format(self=self)


class VW_INT_Agg_MonthlyDonorsPerLocationSchema(ma.ModelSchema):
    class Meta:
        model = VW_INT_Agg_MonthlyDonorsPerLocation
        sqla_session = db.session
		
		
class VW_INT_Agg_DailyDonorsPerLocation(db.Model):
	__tablename__ = 'VW_INT_Agg_DailyDonorsPerLocation'
	__table_args__ = {'useexisting': True}
	#__bind_key__ = 'output'

	id = db.Column(Integer, primary_key=True, autoincrement=True)
	regionID = db.Column(Integer())
	locationName = db.Column(String(100))
	donationType = db.Column(String(50))
	yearmonthdayNum = db.Column(Integer())
	yearmonthdayName = db.Column(String(20))
	numDonors = db.Column(Integer())

	def __init__(self, reg_id, loc_name, don_desc, ym_num, ym_name, num_dons):
		self.regionID = reg_id
		self.locationName = loc_name
		self.donationType = don_desc
		self.yearmonthdayNum = ym_num
		self.yearmonthdayName = ym_name
		self.numDonors = num_dons
		
	def save(self):
		session.add(self)
		session.commit()
		
	@staticmethod
	def get_all():
		return VW_INT_Agg_DailyDonorsPerLocation.query.all()
		
	def delete(self):
		session.delete(self)
		session.commit()
		
	def __repr__(self):
		return "VW_INT_Agg_DailyDonorsPerLocation(region_id={self.regionID}, " \
		"location_name='{self.locationName}', " \
		"donation_type='{self.donationType}', " \
		"yearmonthdayNum='{self.yearmonthdayNum}', " \
		"yearmonthdayName='{self.yearmonthdayName}', " \
		"num_donors={self.numDonors})".format(self=self)


class VW_INT_Agg_DailyDonorsPerLocationSchema(ma.ModelSchema):
    class Meta:
        model = VW_INT_Agg_DailyDonorsPerLocation
        sqla_session = db.session
		
		

class VW_INT_Agg_LastDonationPerDonor(db.Model):
	__tablename__ = 'VW_INT_Agg_LastDonationPerDonor'
	__table_args__ = {'useexisting': True}
	#__bind_key__ = 'output'

	id = db.Column(Integer, primary_key=True, autoincrement=True)
	donorID = db.Column(Integer())
	locationName = db.Column(String(100))
	donationType = db.Column(String(50))
	lastDonationNum = db.Column(Integer())
	lastDonationName = db.Column(String(20))
	numDaysLastDon = db.Column(Integer())

	def __init__(self, don_id, loc_name, don_desc, date_num, date_name, num_days):
		self.donorID = don_id
		self.locationName = loc_name
		self.donationType = don_desc
		self.lastDonationNum = date_num
		self.lastDonationName = date_name
		self.numDaysLastDon = num_days
		
	def save(self):
		session.add(self)
		session.commit()
		
	@staticmethod
	def get_all():
		return VW_INT_Agg_LastDonationPerDonor.query.all()
		
	def delete(self):
		session.delete(self)
		session.commit()
		
	def __repr__(self):
		return "VW_INT_Agg_LastDonationPerDonor(donor_id={self.donorID}, " \
		"location_name='{self.locationName}', " \
		"donation_type='{self.donationType}', " \
		"lastDonationNum='{self.lastDonationNum}', " \
		"lastDonationName='{self.lastDonationName}', " \
		"numDaysLastDon={self.numDaysLastDon})".format(self=self)

class VW_INT_Agg_LastDonationPerDonorSchema(ma.ModelSchema):
    class Meta:
        model = VW_INT_Agg_LastDonationPerDonor
        sqla_session = db.session
		
		
		
class VW_INT_Agg_YearlyDonorsbyCounty(db.Model):
	__tablename__ = 'VW_INT_Agg_YearlyDonorsbyCounty'
	__table_args__ = {'useexisting': True}
	# __bind_key__ = 'output'

	id = db.Column(Integer, primary_key=True, autoincrement=True)
	year = db.Column(Integer())
	minLong = db.Column(Integer())
	maxLong = db.Column(Integer())
	minLat = db.Column(Integer())
	maxLat = db.Column(Integer())
	fips = db.Column(Integer())
	countyName = db.Column(String(200))
	numDonors = db.Column(Integer())

	def __init__(self, year, min_long, max_long, min_lat, max_lat, fips, county_name, num_dons):
		self.year  = don_id
		self.minLong = min_long
		self.maxLong = max_long
		self.minLat = min_lat
		self.maxLat = max_lat
		self.fips = fips
		self.countyName = county_name
		self.numDonors = num_dons
		
	def save(self):
		session.add(self)
		session.commit()
		
	@staticmethod
	def get_all():
		return VW_INT_Agg_YearlyDonorsbyCounty.query.all()
		
	def delete(self):
		session.delete(self)
		session.commit()
		
	def __repr__(self):
		return "VW_INT_Agg_YearlyDonorsbyCounty(year={self.year}, " \
		"countyName='{self.countyName}', " \
		"fips='{self.fips}', " \
		"numDonors={self.numDonors})".format(self=self)

class VW_INT_Agg_YearlyDonorsbyCountySchema(ma.ModelSchema):
    class Meta:
        model = VW_INT_Agg_YearlyDonorsbyCounty
        sqla_session = db.session