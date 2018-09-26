# Define query based models to use in api

# Local import 
from app import db

# Create Table for aggregation:
from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base


# Custom aggregation query classes:
class VW_INT_Agg_MonthlyDonorsPerLocation(db.Model):
    __tablename__ = 'VW_INT_Agg_MonthlyDonorsPerLocation'
    __table_args__ = {'useexisting': True} 
    
    id = Column(Integer, primary_key=True, autoincrement=True)
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
        return "VW_INT_Agg_MonthlyDonorsPerLocation(region_id={self.region_id}, " \
        "location_name='{self.location_name}', " \
        "donation_type='{self.donation_type}', " \
        "yearmonth_num='{self.yearmonth_num}', " \
        "yearmonth_name='{self.yearmonth_name}', " \
        "num_donors={self.num_donors})".format(self=self)
