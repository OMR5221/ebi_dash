class VW_INT_Agg_MonthlyDonorsPerLocation(Base, session):
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
            return NumDonorsLoc.query.all()
            
        def delete(self):
            session.delete(self)
            session.commit()
			
		def load(self):
			"""
			(INT_DIMLocation.RegionID,
			INT_DIMLocation.FinanceLocationName,
			Int_DimDonationType.DonationDescription,
			cast((DimDate.Year+DimDate.Month),Integer).label('yyyymm'),
			DimDate.MonthYear,
			func.count(INT_MKTCollectionDetails.personid).label('numDonors'))
			.filter(INT_MKTCollectionDetails.LocationSK == INT_DIMLocation.LocationSK)
			.filter(INT_MKTCollectionDetails.DonationTypeSK == Int_DimDonationType.DonationTypeSk)
			.filter(INT_MKTCollectionDetails.CollectionDateSK == DimDate.DateKey)
			.group_by(INT_DIMLocation.RegionID, INT_DIMLocation.FinanceLocationName, Int_DimDonationType.DonationDescription, cast((DimDate.Year+DimDate.Month),Integer),DimDate.MonthYear))
			"""
					
        def __repr__(self):
            return "NumDonorsLoc(region_id={self.region_id}, " \
            "location_name='{self.location_name}', " \
            "donation_type='{self.donation_type}', " \
            "yearmonth_num='{self.yearmonth_num}', " \
            "yearmonth_name='{self.yearmonth_name}', " \
            "num_donors={self.num_donors})".format(self=self)

# Create the Table schema
VW_INT_Agg_MonthlyDonorsPerLocation.__table__.create(engine, checkfirst=True)
# Loa the table with data from other DW Tables:
VW_INT_Agg_MonthlyDonorsPerLocation.load()