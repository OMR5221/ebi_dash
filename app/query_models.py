# Define query based models to use in api

# Local import 
from app import db

# Create Table for aggregation:
from sqlalachemy.ext.declarative import declarative_base
Base = declarative_base()

class NumDonorsLoc(Base):

	__tablename__ = 'numdons_loc'
	
	id = db.Column(Integer, primary_key=True, autoincrement=True)
	region_id = db.Column(Integer())
	location_name = db.Column(String(100), index=True)
	donation_type = db.Column(String(50))
	yearmonth_num = db.Column(Integer())
	yearmonth_name = db.Column(String(20))
	num_donors = db.Column(Integer())
	
	def __init__(self, reg_id, loc_name, don_desc, ym_num, ym_name, num_dons):
		self.region_id = reg_id
		self.location_name = loc_name
		self.donation_type = don_desc
		self.yearmonth_num = ym_num
		self.yearmonth_name = ym_name
		self.num_donors = num_dons
		
	def save(self):
		db.session.add(self)
		db.session.commit()
		
	@staticmethod
	def get_all():
		return NumDonorsLoc.query.all()
		
	def delete(self):
		db.session.delete(self)
		db.session.commit()
		
	def __repr__(self):
		return "NumDonorsLoc(region_id={self.region_id}, " \
		"location_name='{self.location_name}', " \
		"donation_type='{self.donation_type}', " \
		"yearmonth_num='{self.yearmonth_num}', " \
		"yearmonth_name='{self.yearmonth_name}', " \
		"num_donors={self.num_donors})".format(self=self)