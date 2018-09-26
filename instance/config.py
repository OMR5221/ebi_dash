import os

class Config(object):
	"""Parent config class"""
	# Default settings:
	DEBUG = False
	CSRF_ENABLED = True
	# SECRET_KEY = os.getenv('SECRET')
	#ADMINS = frozenset(['oswald.ramirez@oneblood.org, '])
	SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0'
	CORS_ALLOW_HEADERS = "Content-Type"
	CORS_RESOURCES = {r"/api/*" : {"origins" : "*"}}
	
# Inherits from Default Config:
class DevelopmentConfig(Config):
	"""Configs for DEV"""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0'

class TestingConfig(Config):
	TESTING = True
	DEBUG = True

class QualityAssuranceConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://ORLEBIQADB/Integration?driver=SQL+Server+Native+Client+11.0'
	
class ProductionConfig(Config):
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://ORLEBIPRODDB/Integration?driver=SQL+Server+Native+Client+11.0'

app_config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'qa': QualityAssuranceConfig,
	'production': ProductionConfig
}