import os
from flask_script import Manager # handles commands
from flask_migrate import Migrate, MigrateCommand
from app import query_models

