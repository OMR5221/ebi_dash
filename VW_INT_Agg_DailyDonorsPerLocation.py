"""
This is the module and supports all the REST actions for the data
"""

from flask import (
    make_response,
    abort,
)
from config import db
from models import (
    VW_INT_Agg_DailyDonorsPerLocation,
    VW_INT_Agg_DailyDonorsPerLocationSchema,
)


def read_all_daily():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    dailyDonors = VW_INT_Agg_DailyDonorsPerLocation.query.order_by(VW_INT_Agg_DailyDonorsPerLocation.yearmonthdayNum).all()

    # Serialize the data for the response
    dailyDonors_schema = VW_INT_Agg_DailyDonorsPerLocationSchema(many=True)
    data = dailyDonors_schema.dump(dailyDonors).data
    return data