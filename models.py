from datetime import datetime
from config import db, ma
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey, Numeric, cast, func, create_engine)


class VW_INT_Agg_MonthlyDonorsPerLocation(db.Model):
	__tablename__ = 'VW_INT_Agg_MonthlyDonorsPerLocation'
	__table_args__ = {'useexisting': True}
	__bind_key__ = 'output'

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
	__bind_key__ = 'output'

	id = Column(Integer, primary_key=True, autoincrement=True)
	regionID = Column(Integer())
	locationName = Column(String(100))
	donationType = Column(String(50))
	yearmonthdayNum = Column(Integer())
	yearmonthdayName = Column(String(20))
	numDonors = Column(Integer())

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
		return NumDonorsLoc.query.all()
		
	def delete(self):
		session.delete(self)
		session.commit()
		
	def __repr__(self):
		return "NumDonorsLoc(region_id={self.regionID}, " \
		"location_name='{self.locationName}', " \
		"donation_type='{self.donationType}', " \
		"yearmonthdayNum='{self.yearmonthdayNum}', " \
		"yearmonthdayName='{self.yearmonthdayName}', " \
		"num_donors={self.numDonors})".format(self=self)


class VW_INT_Agg_DailyDonorsPerLocationSchema(ma.ModelSchema):
    class Meta:
        model = VW_INT_Agg_DailyDonorsPerLocation
        sqla_session = db.session