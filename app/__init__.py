# app/__init__.py
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# Localm imports
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

# Create app based on input config file:
def create_app(config_name):

	from api.models import VW_INT_Agg_MonthlyDonorsPerLocation


	app = FlaskAPI(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	# Deprectaed settiung that throws warning when not explicitly disabled:
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	
	
	@app.route('/monthyeardonors', methods=['POST', 'GET'])
	def YearMonthDonors():
		if request.method == "GET":
			donors_ym_loc = VW_INT_Agg_MonthlyDonorsPerLocation.get_all()
			results = []
			
			for dlym in donors_ym_loc:
				obj = {
					'region_id' = dlym.region_id, 
					'location_name' = dlym.location_name,
					'donation_type' = dlym.donation_type,
					'yearmonth_num' = dlym.yearmonth_num,
					'yearmonth_name' = dlym.yearmonth_name,
					'num_donors' = dlym.num_donors
				}
				results.append(obj)
				
			response = jsonify(results)
			response.status_code = 200
			return response
	
	
	return app