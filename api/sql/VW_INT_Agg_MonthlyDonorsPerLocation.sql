if object_id('Integration.dbo.VW_INT_Agg_DailyDonorsPerLocation') is not null drop table Integration.dbo.VW_INT_Agg_DailyDonorsPerLocation;
SELECT DISTINCT
	dl.RegionID,
	dl.locationdepartmentname,
    dl.FinanceLocationName,
    dt.DonationDescription,
	mkt.collectiondatesk yearmonthday_num,
	dd.FullDateUSA yearmonthday_name,
	count(mkt.personid) numDonors
INTO Integration.dbo.VW_INT_Agg_DailyDonorsPerLocation
FROM Integration.dbo.INT_MKTCollectionDetails mkt
JOIN Integration.dbo.INT_DIMLocation dl
	ON dl.locationSK = mkt.locationsk
JOIN Integration.dbo.Int_DimDonationType dt
	ON mkt.DonationTypeSk = dt.DonationTypeSk
JOIN Integration.dbo.DimDate dd
	ON MKT.CollectionDateSK = dd.DateKey
group by
	dl.RegionID,
	dl.locationdepartmentname,
    dl.FinanceLocationName,
    dt.DonationDescription,
	mkt.collectiondatesk,
	dd.FullDateUSA
	;


/*
select distinct yearmonthday_name, sum(numdonors)
from Integration.dbo.VW_INT_Agg_DailyDonorsPerLocation
group by yearmonthday_name
order by yearmonthday_name
*/

ALTER TABLE Integration.dbo.VW_INT_Agg_DailyDonorsPerLocation
ADD ID INT IDENTITY(1,1) PRIMARY KEY
;


if object_id('Integration.dbo.VW_INT_Agg_MonthlyDonorsPerLocation') is not null drop table Integration.dbo.VW_INT_Agg_MonthlyDonorsPerLocation;
SELECT DISTINCT
	dl.RegionID,
	dl.locationdepartmentname,
    dl.FinanceLocationName,
    dt.DonationDescription,
	CAST(SUBSTRING(STR(mkt.collectiondatesk),1,8) as INTEGER) yearmonth_num,
    --CAST((dd.Year + replace(str(dd.Month,2), ' ', '0') ) as Integer) yearmonth_num,
    dd.MonthYear yearmonth_name,
	count(mkt.personid) numDonors
INTO Integration.dbo.VW_INT_Agg_MonthlyDonorsPerLocation
FROM Integration.dbo.INT_MKTCollectionDetails mkt
JOIN Integration.dbo.INT_DIMLocation dl
	ON dl.locationSK = mkt.locationsk
JOIN Integration.dbo.Int_DimDonationType dt
	ON mkt.DonationTypeSk = dt.DonationTypeSk
JOIN Integration.dbo.DimDate dd
	ON MKT.CollectionDateSK = dd.DateKey
group by
	dl.RegionID,
    dl.FinanceLocationName,
    dt.DonationDescription,
	dl.locationdepartmentname,
    CAST(SUBSTRING(STR(mkt.collectiondatesk),1,8) as INTEGER),
    dd.MonthYear
	;


ALTER TABLE Integration.dbo.VW_INT_Agg_MonthlyDonorsPerLocation
ADD ID INT IDENTITY(1,1) PRIMARY KEY
;