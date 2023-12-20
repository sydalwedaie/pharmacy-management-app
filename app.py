# Description: This file contains the main application logic for the website. It is responsible for handling all the routes and rendering the appropriate templates. It also contains the logic for the helper functions. 

import time

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, staff_login_required

################################################################################
# Configurations
################################################################################
# Configure Application
app = Flask(__name__)

# Configure database
database = SQL("sqlite:///database.db")

# Configure Session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Give templates access to functions on every page
@app.context_processor
def utilities():
    def username(user_id):
        user_entry = database.execute(
            "SELECT username FROM Users WHERE user_id=?",
            session.get("user_id")
        )
        if user_entry:
            return user_entry[0]["username"]
        else:
            return None

    return dict({
        "username": username,
        "format_time": time.ctime
    })

@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    

################################################################################
# Routes
################################################################################

# Each route is a function that returns a response. The response can be a string, a template, or a redirect.
# The function is executed when the user visits the URL associated with the route. For example, the index() function is executed when the user visits the URL http://localhost:5000/. Similarly, the login() function is executed when the user visits the URL http://localhost:5000/login.

@app.route("/")
@login_required
def index():
    return render_template("index.html")


# The login_required() decorator ensures that the user is logged in before they can access the route. If the user is not logged in, they are redirected to the login page.
@app.route("/products")
@login_required
def products():
    # get cart items
    products = database.execute("""
        SELECT product_id, name, description, price, quantity_in_stock 
        FROM Products
    """)
    return render_template("products.html", products=products)


@app.route("/search_products")
def search_products():
    query = request.args.get('query')
    products = database.execute(
        "SELECT * FROM Products WHERE name LIKE ?",
        '%' + query + '%'
    )
    return jsonify(products)


# User Management Routes #######################################################
# There are two ways to access a route: GET and POST. The GET method is used to access a route via a URL. The POST method is used to access a route via a form submission. In this route, if the user visits the logic route directly, the GET branch is executed and the user is presented with a login form. If the user submits the login form, the form data is sent to the same route via the POST method. The route then checks the username and password and logs the user in if they are valid.
@app.route("/login", methods=["GET", "POST"])
def login():
    # User reached route via login URL
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via login form
    username = request.form.get("username")
    password = request.form.get("password")

    # Check username and passwrod are supplied
    if not username:
        return apology("must provide username" )
    elif not password:
        return apology("must provide password" )

    # Query database for username
    user_entry = database.execute("SELECT * FROM Users WHERE username=?", username)

    # Ensure username exists and password is correct
    if len(user_entry) != 1 or not check_password_hash(user_entry[0]["password_hash"], password):
        return apology("Invalid username and/or password.")

    # Remember which user has logged in
    session["user_id"] = user_entry[0]["user_id"]
    session["user_type"] = user_entry[0]["user_type"]

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# staff login required
# This route is executed when the user tries to access a staff-only route without being logged in as a staff member. The user is redirected to the staff login page.
@app.route("/staff_restricted")
@login_required
def staff_restricted():
    return render_template("staff_restricted.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # Access via POST
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    user_type = request.form.get("user_type")

    # Validate username
    if not username:
        return apology("Must supply a username." )
    elif database.execute("SELECT username FROM Users WHERE username=?", username):
        return apology("Username already exists. Choose another username." )

    # Validate password
    if not password:
        return apology("Must supply a password." )

    # Validate confirmation
    if not confirmation:
        return apology("Must supply a confirmation." )
    elif password != confirmation:
        return apology("Password and Confirmation do not match." )

    # Add user to database
    database.execute(
        "INSERT INTO Users (username, password_hash, user_type) VALUES (?, ?, ?)",
        username, generate_password_hash(password), user_type
    )

    # Update CustomerData and StaffData tables depending on user_type
    if user_type == "customer":
        database.execute(
            "INSERT INTO CustomerData (user_id, name) VALUES (?, ?)",
            database.execute("SELECT user_id FROM Users WHERE username=?", username)[0]["user_id"], username
        )
    elif user_type == "staff":
        database.execute(
            "INSERT INTO StaffData (user_id, name) VALUES (?, ?)",
            database.execute("SELECT user_id FROM Users WHERE username=?", username)[0]["user_id"], username
        )
    
    # Log the user in
    user_entry = database.execute("SELECT * FROM Users WHERE username=?", username)
    session["user_id"] = user_entry[0]["user_id"]
    session["user_type"] = user_entry[0]["user_type"]

    return redirect("/")


# Edit Profile 
@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    user_id = session.get("user_id")
    # Access via GET
    if request.method == "GET":
        # get user data
        user_data = database.execute("SELECT * FROM Users WHERE user_id=?", user_id)[0]

        # get staff data
        if session.get("user_type") == "staff":
            staff_data = database.execute("SELECT * FROM StaffData WHERE user_id=?", user_id)[0]
            return render_template("edit_profile.html", user_data=user_data, staff_data=staff_data)

        # get customer data
        elif session.get("user_type") == "customer":
            customer_data = database.execute("SELECT * FROM CustomerData WHERE user_id=?", user_id)[0]
            return render_template("edit_profile.html", user_data=user_data, customer_data=customer_data)

    # Access via POST
    name = request.form.get("name")
    email = request.form.get("email")
    contact_number = request.form.get("contact_number")

    # Update Users table
    database.execute(
        "UPDATE Users SET email = ?, contact_number = ? WHERE user_id = ?",
        email, contact_number, user_id
    )

    # Update CustomerData table
    if session.get("user_type") == "customer":
        address = request.form.get("address")
        database.execute(
            "UPDATE CustomerData SET name = ?, address = ? WHERE user_id = ?",
            name, address, user_id
        )

    # Update StaffData table
    elif session.get("user_type") == "staff":
        position = request.form.get("position")
        date_of_join = request.form.get("date_of_join")
        # date of join should not be in the future
        if date_of_join > time.strftime("%Y-%m-%d"):
            return apology("Date of join cannot be in the future" )

        database.execute(
            "UPDATE StaffData SET name = ?, position = ?, date_of_join = ? WHERE user_id = ?",
            name, position, date_of_join, user_id
        )

    # Redirect to Edit Profile page
    return redirect("/edit_profile")


# Inventory Control Routes #####################################################
@app.route("/add_product", methods=["GET", "POST"])
@staff_login_required
def add_product():
    # Access via GET
    if request.method == "GET":
        return render_template("add_product.html")

    # Access via POST
    name = request.form.get("product_name")
    description = request.form.get("product_description")
    supplier = request.form.get("product_supplier")
    expiry_date = request.form.get("product_expiry_date")
    price = request.form.get("product_price")
    quantity = request.form.get("product_quantity")

    # Validate inputs
    if not name:
        return apology("Must provide a name" )
    elif not description:
        return apology("Must provide a description" )
    elif not price:
        return apology("Must provide a price" )
    elif float(price) <= 0:
        return apology("Price must be a positive number" )
    elif not quantity:
        return apology("Must provide a quantity" )
    elif int(quantity) < 0:
        return apology("Quantity must be a positive number" )


    # Add product to database
    database.execute(
        "INSERT INTO products (name, description, supplier, expiry_date, price,\
        quantity_in_stock) VALUES (?, ?, ?, ?, ?, ?)",
        name, description, supplier, expiry_date, price, quantity
    )

    # Redirect to Add Product page
    return redirect("/add_product")


@app.route("/update_product", methods=["GET", "POST"])
@staff_login_required
def update_product():
    products = database.execute(
        "SELECT product_id, name, description, supplier, expiry_date, price, quantity_in_stock FROM Products"
    )
    
    # Access via GET
    if request.method == "GET":
        return render_template("update_product.html", products=products)

    # Access via POST
    name = request.form.get("product_name")
    description = request.form.get("product_description")
    supplier = request.form.get("product_supplier")
    expiry_date = request.form.get("product_expiry_date")
    price = request.form.get("product_price")
    quantity = request.form.get("product_quantity")

    # Validate inputs
    if not name:
        return apology("Must provide a name" )
    elif not description:
        return apology("Must provide a description" )
    elif not price:
        return apology("Must provide a price" )
    elif float(price) <= 0:
        return apology("Price must be a positive number" )
    elif not quantity:
        return apology("Must provide a quantity" )
    elif int(quantity) < 0:
        return apology("Quantity must be a positive number" )


    # update product in database
    database.execute(
        "UPDATE Products SET description = ?, price = ?, quantity_in_stock = ? WHERE name = ?",
        description, price, quantity, name
    )

    # Redirect to Update Product page
    return redirect("/update_product")


# Report Routes ################################################################
@app.route("/staff_report", methods=["GET", "POST"])
@staff_login_required
def staff_report():
    staff = database.execute(
        "SELECT name, position, date_of_join FROM StaffData",
    )
    return render_template("staff_report.html", staff=staff)


@app.route("/product_report", methods=["GET", "POST"])
@staff_login_required
def product_report():
    products = database.execute(
        "SELECT name, description, supplier, expiry_date, price, quantity_in_stock FROM Products"
    )
    return render_template("product_report.html", products=products)


@app.route("/order_report", methods=["GET", "POST"])
@staff_login_required
def order_report():
    orders = database.execute(
        "SELECT order_id, user_id, order_date, total_amount FROM Orders",
    )
    return render_template("order_report.html", orders=orders)

    

# Order Placement Routes #######################################################
@app.route("/add_to_cart", methods=["POST"])
@login_required
def add_to_cart():
    # Access via POST
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    user_id = session.get("user_id")

    # cannot add an expired product to cart
    if database.execute("SELECT expiry_date FROM Products WHERE product_id=?", product_id)[0]['expiry_date'] < time.strftime("%Y-%m-%d"):
        return apology("Sorry! This product is currently unavailable for purchase." ) 
        
    # Add product to cart
    database.execute(
        "INSERT INTO Cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
        user_id, product_id, quantity
    )

    # Redirect to products page
    return redirect("/products")


@app.route("/cart")
@login_required
def cart():
    user_id = session.get("user_id")
    # Access via GET
    if request.method == "GET":
        cart = database.execute("""
            SELECT Cart.product_id, Products.name as product_name, Cart.quantity
            FROM Cart
            INNER JOIN Products ON Cart.product_id = Products.product_id
            WHERE Cart.user_id = ?
        """, user_id)
        return render_template("cart.html", cart=cart)


@app.route("/place_order", methods=["POST"])
@login_required
def place_order():
    user_id = session.get("user_id")
    cart_items = database.execute("""
        SELECT Cart.product_id, Cart.quantity, Products.price
        FROM Cart
        INNER JOIN Products ON Cart.product_id = Products.product_id
        WHERE Cart.user_id = ?
    """, user_id)

    # Create a new order
    database.execute(
        "INSERT INTO Orders (user_id, order_date, total_amount) VALUES (?, CURRENT_DATE, ?)",
        user_id, sum(item['price'] * item['quantity'] for item in cart_items)
    )

    # Get the ID of the newly created order
    order_id = database.execute(
        "SELECT order_id FROM Orders WHERE user_id = ? ORDER BY order_id DESC LIMIT 1",
        user_id
    )[0]['order_id']

    # Insert items into OrderDetails
    for item in cart_items:
        database.execute(
            "INSERT INTO OrderDetails (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            order_id, item['product_id'], item['quantity'], item['price']
        )

    # Update the Products table to reflect the new stock levels
    for item in cart_items:
        database.execute(
            "UPDATE Products SET quantity_in_stock = quantity_in_stock - ? WHERE product_id = ?",
            item['quantity'], item['product_id']
        )

    # Clear the user's cart
    database.execute("DELETE FROM Cart WHERE user_id = ?", user_id)

    # Redirect to a confirmation page or the home page
    return redirect("/reciept")


@app.route("/cancel_order", methods=["POST"])
@login_required
def cancel_order():
    user_id = session.get("user_id")
    database.execute("DELETE FROM Cart WHERE user_id = ?", user_id)
    return redirect("/cart")


@app.route("/reciept", methods=["GET", "POST"])
@login_required
def reciept():
    user_id = session.get("user_id")
    order = database.execute(
        "SELECT * FROM Orders WHERE user_id = ? ORDER BY order_id DESC LIMIT 1",
        user_id
    )[0]

    order_details = database.execute("""
        SELECT OrderDetails.quantity, OrderDetails.price, Products.name as product_name
        FROM OrderDetails
        INNER JOIN Products ON OrderDetails.product_id = Products.product_id
        WHERE OrderDetails.order_id = ?
    """, order['order_id'])

    return render_template(
        "reciept.html", 
        order_details=order_details, 
        total_amount=order['total_amount']
    )


@app.route("/order_history")
@login_required
def order_history():
    user_id = session.get("user_id")
    orders = database.execute(
        "SELECT * FROM Orders WHERE user_id = ? ORDER BY order_date DESC",
        user_id
    )

    for order in orders:
        order['order_details'] = database.execute("""
            SELECT OrderDetails.quantity, OrderDetails.price, Products.name as product_name
            FROM OrderDetails
            INNER JOIN Products ON OrderDetails.product_id = Products.product_id
            WHERE OrderDetails.order_id = ?
        """, order['order_id'])

    return render_template("order_history.html", orders=orders)