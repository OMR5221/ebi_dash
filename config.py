import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite ULR for SqlAlchemy
ebidash_in_url = 'mssql+pyodbc://ORLEBIDEVDB/INTEGRATION?driver=SQL+Server+Native+Client+11.0'
ebidash_out_url = 'sqlite:///' + os.path.join(basedir, 'ebidash.db')

# Configure the SqlAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = ebidash_out_url
SQLALCHEMY_BINDS = {
    'input': 'pyodbc://ORLEBIDEVDB/Integration?driver=SQL+Server+Native+Client+11.0',
    'output': 'sqlite:///' + os.path.join(basedir, 'ebidash.db')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)