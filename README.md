# NTF Pharmacy Management Application

This application is a web-based system for managing a pharmacy's operations. It includes features for managing users, products, orders, and staff data. The application is built using Flask, a Python web framework, and SQLite for the database.

## Application Structure

The application is structured as follows:

- `app.py`: This is the main application file. It contains the application's routes and the logic for rendering templates. It also configures the application and the database.
- `helpers.py`: This file contains helper functions used throughout the application. These include functions for rendering error messages and checking user login status.
- `init_db.py`: This script is used to initialize the database.
- `schema.sql`: This file contains the SQL statements for creating the database tables.
- `static/`: This directory contains static files such as CSS stylesheets.
- `templates/`: This directory contains the HTML templates that are rendered by the application.

## Running the Application

To run the application, follow these steps:

- Make sure you have Python3 installed. If not, download from python.org.
- Clone the repository to your local machine.
- Navigate to the directory containing the application.
- Run `pip install -r requirements.txt` to install the required packages.
- Run `python3 init_db.py` to initialize the database.
- Run `flask run` to start the application.
- Ignore the WARNING and note the address where it says "Running on http://...".
- Open a web browser and navigate the address displayed in the previous step.

## Libraries

The following Python libraries used in this application are:

- `Flask`: A web framework for Python, used for handling requests and responses on the server, and rendering templates.
- `Flask-Session`: A Flask extension for handling server-side sessions.
- `SQLite3`: A library for interacting with SQLite databases, used to execute SQL commands and manage the database.
- `Werkzeug`: A utility library for WSGI web applications, used for password hashing.
- `CS50`: A library developed by Harvard University, used for database operations.
- `Time`: A built-in Python library for time-related functions.
- `CSV`, `Datetime`, `Pytz`, `Subprocess`, `Urllib`, `UUID`: Built-in Python libraries used for various utility functions.
