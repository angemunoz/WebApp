Information regarding running the system:

    1. Initialize virtual environment:
	On CMD, go to the folder containing this file (it should be named "WebApp"), requirements.txt, wsgi.py and the folder named trfocd.
	Input the following:
		To create a virtual environment (only needs to be done once):
		> py -m venv myvirtual
		To enter the virtual environment (needs redoing every time CMD is closed):
		> myvirtual\Scripts\activate
		To install all required packages (only needs to be done once):
		> pip install -r requirements.txt
	Do not close this window.
    
    2. Download MySQL 8.0.34 (https://dev.mysql.com/downloads/installer/)
	Follow installation steps.
	Leave everything as default.
	There is a possibility to add an user at this stage, but we will do it on the next step.

    3. Create a new user on MySQL:
	Select local instance.
	Under "Server" select "Users and Privileges".
	Select "Add Account":
		Provide a log-in name (the connection string uses "ocdesintr").
		Provide a password (the connection string uses "patrae&aFrad1s").
		Confirm password.
		On Administrative roles:
			Select checkbox "DBA" (grants all permissions).
		Select "Apply".
	
    4. Create a database  on MySQL:
	Select "Create a new schema in the connected server" (displayed as a circular tower widget with a small "+" sign, should be below "Query").
		Name the database (the connection string uses "dtrfocdb").
		Select "Apply".
			Select "Apply" to confirm the SQL code.

    5. Confirm database link in __init__.py.
	The code found in __init__ is: 
		app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://ocdesintr:patrae&aFrad1s@192.168.1.6/dtrfocdb"
			ocdesintr -> Username, change if another username given on the creation of the database.
			patrae&aFrad1s -> Password, change if another password given on the creation of the database.
			192.168.1.6 -> Static IP address, if using the default port change to 3306.
			dtrfocdb -> Name of database, change if another username given on the creation of the database.
        Save file if changes required.

    6. Create tables
	The tables can be created from the flask shell.
	Return to CMD, if the window was closed please return to the folder previously specified and re-enter the virtual environment (note other folders will return an error).
	Input the following:
		Open the flask shell within the virtual environment:
		> flask shell
		Import the database from the module:
		> from trfocd import db
		Create all tables on the database:
		> db.create_all()
		Leave the flask shell:
		> exit()
	CMD should still have the virtual environment active and be in the right folder.
	All tables should now appear on your MySQL Workbench.

    7. Start the website:
	On CMD input the following:
		To set the app:
		> set FLASK_APP=wsgi
		To run the app:
		> flask run
		A message should appear confirming that the app is now running.
		The default address is 127.0.0.1:5000.

    The app should now be available locally at: 127.0.0.1:5000