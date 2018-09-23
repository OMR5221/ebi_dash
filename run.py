import os

# Local import from /app/__init__::create_app()
from app import create_app

config_name = "development" # os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
	app.run()