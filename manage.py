# Perform DB migrations when a chnage is necessary:
# Keeps track of all commands issued and handles how they are called from cli
# MigrateCommand: has a set of migration commands
import os
from flask_script import Manager # handles commands
from flask_migrate import Migrate, MigrateCommand
from app import models
from app import db, create_app


app = create_app(config_name='development') #os.getenv('APP_SETTINGS')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
	manager.run()