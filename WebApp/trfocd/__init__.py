from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# All needed installs present in requirements.txt

# Create the app and link the folder which holds the static file.
app = Flask(__name__, static_folder="static")

# Set the secret key.
app.config['SECRET_KEY'] = '7646db2cacd7138c92f94647f3cdf249ea52b7624db5ff42'

# Link the app to the database created on MySQL and initialize it.
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://ocdesintr:patrae&aFrad1s@192.168.1.6/dtrfocdb"
db = SQLAlchemy(app)

# Apply CSRF protection to the forms.
csrf = CSRFProtect(app)

# Protect users' session cookie.
LoginManager.session_protection = "strong"


# Ensure users can log in and out and restrict access to only their own data.
login_manager = LoginManager()
login_manager.init_app(app)

# Link the routes.py, models.py and graphs.py files to the app.
# Must happen after the app is set.
from trfocd import routes, models, graphs