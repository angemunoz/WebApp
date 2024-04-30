# Import the app from the trfocd folder app settings on __init__.py, from Flask (https://flask-ptbr.readthedocs.io/en/latest/quickstart.html#)
from trfocd import app

# Code to only run the app if called directly and set the debug.
if __name__ == '__main__':
    app.run(debug=True)
