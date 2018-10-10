"""
This is the module and supports all the REST actions for the data
"""

from flask import (
    make_response,
    abort,
)
from config import db
from models import (
    VW_INT_Agg_MonthlyDonorsPerLocation,
    VW_INT_Agg_MonthlyDonorsPerLocationSchema,
)

    
def read_all_monthly():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    monthlyDonors = VW_INT_Agg_MonthlyDonorsPerLocation.query.order_by(VW_INT_Agg_MonthlyDonorsPerLocation.yearmonthNum).all()

    # Serialize the data for the response
    monthlyDonors_schema = VW_INT_Agg_MonthlyDonorsPerLocationSchema(many=True)
    data = monthlyDonors_schema.dump(monthlyDonors).data
    return data