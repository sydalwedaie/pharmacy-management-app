# Description: Helper functions for the application. These functions are used inside app.py.

import csv
import datetime
import pytz
import subprocess
import urllib
import uuid


from flask import redirect, render_template, session
from functools import wraps


def apology(message):
    # Render message as an apology to user.
    return render_template("apology.html", message=message)


def login_required(f):
    # Decorate routes to require login.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def staff_login_required(f):
    # Decorate routes to require staff login.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        elif session.get("user_type") != "staff":
            return redirect("/staff_restricted")
        return f(*args, **kwargs)
    return decorated_function