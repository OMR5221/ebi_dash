# Define query based models to use in api
from sqlalachemy.ext.declarative import declarative_base
Base = declarative_base()

class NumDonorsLoc(Base):

	__tablename__ = 'numdons_loc'
	
	region_id = Column(Integer())
	location_name = Column(String(100), index=True)
	donation_type = Column(String(50))
	yearmonth_num = Column(Integer())
	yearmonth_name = Column(String(20))
	num_donors = Column(Integer())
	
	def __init__(self, reg_id, loc_name, don_desc, ym_num, ym_name, num_dons):
		self.region_id = reg_id
		self.location_name = loc_name
		self.donation_type = don_desc
		self.yearmonth_num = ym_num
		self.yearmonth_name = ym_name
		self.num_donors = num_dons
		
	
	def __repr__(self):
		return 
		"NumDonorsLoc(region_id={self.region_id}, " \
		"location_name='{self.location_name}', " \
		"donation_type='{self.donation_type}', " \
		"yearmonth_num='{self.yearmonth_num}', " \
		"yearmonth_name='{self.yearmonth_name}', " \
		"num_donors={self.num_donors})".format(self=self)
		
	@staticmethod
	def get_all():
		return NumDonorsLoc.query.all()