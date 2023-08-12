import matplotlib.pyplot as plt
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///aahar.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact")
def about():
    return render_template("contact.html")


# @app.route("/buy", methods=["GET", "POST"])
# @login_required
# def buy():
#     """Buy shares of stock"""
#     if request.method == "POST":
#         user_id = session["user_id"]
#         symbol = request.form.get("symbol")
#         share = request.form.get("shares")

#         # Check if both are empty
#         if symbol == "":
#             return apology("Missing Symbol")
#         elif not share.isdigit():
#             return apology("Missing shares")
#         elif share == "":
#             return apology("Missing share"), 400
#         elif share is None:
#             return apology("Missing share")
#         try:
#             converted_share = int(share)
#         except:
#             return apology("Something went wrong"), 400
#         if item is None:
#             return apology("Invalid Symbol")
#         # Retrive of available cash from users table
#         cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

#         stock_name = item["name"]
#         stock_price = int(item["price"])
#         total_price = stock_price * converted_share
#         # Condition checking
#         if int(cash) < int(total_price):
#             return apology("Not eneough cash available for buying"), 400
#         else:
#             db.execute("UPDATE users SET cash = ? WHERE id = ? ", (cash - total_price), user_id)
#             db.execute("INSERT INTO transactions(user_id, name, symbol, type, shares, price) VALUES(?, ?, ?, ?, ?, ?)",
#                        user_id, stock_name, symbol, "BUY", converted_share, stock_price)
#         return redirect("/")

#     else:
#         return render_template("buy.html"), 400


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""
#     buy = db.execute("SELECT * FROM transactions WHERE user_id = ? AND type='BUY'", session["user_id"])
#     sell = db.execute("SELECT * FROM transactions WHERE user_id = ? AND type='SELL'", session["user_id"])

#     buy_graph={"time":[],"price":[]}
#     sell_graph={"time":[],"price":[]}
#     for i in buy:
#         buy_graph["price"].append(i["price"])
#         buy_graph["time"].append(i["timimg"])
#     for i in sell:
#         sell_graph["price"].append(i["price"])
#         sell_graph["time"].append(i["timimg"])
#     profit=[]
#     time=[]
#     for i in range(len(buy_graph["price"])):
#         profit.append(sell_graph["price"][i]-buy_graph["price"][i])
#         time.append(sell_graph["time"][i][11:16])
#     for i in profit:
#             fig, ax = plt.subplots()
#             ax.barh(time, profit, align='center')
#             plt.xlabel("Profit")
#             plt.ylabel("Time")
#             plt.savefig('./static/img/profit.jpg')
#     return render_template("history.html", buy=buy, sell=sell, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("Must provide a email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide a password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""
#     if request.method == "POST":
#         stock = request.form.get("symbol")
#         # Invalid input checking
#         if stock == "":
#             return apology("Invalid Symbol")
#         item = lookup(stock)
#         if item == None:
#             return apology("Invalid Symbol")
#         return render_template("quote.html", item=item, usd_function=usd)
#     else:
#         return render_template("quote.html"), 400


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")

        # User input validation
        if fname == "" and phone == "" and email == "" and password == "":
            return apology("Please fill all the details to process further")

        elif not fname:
            return apology("FIrst Name is required")
        elif not phone:
            return apology("Phone is required")
        elif not email:
            return apology("Email is required")

        elif not password:
            return apology('Password is required')
        
        # Password generating process
        hash = generate_password_hash(password)
        checks = db.execute("SELECT * FROM login")
        for check in checks:
            if email in check["email"]:
                return apology(f'The email is already in use')
        try:
            db.execute("INSERT INTO login (f_name,l_name,email,phone,password) VALUES (?, ?)", fname,lname,email,phone, hash)
            return redirect("/")
        except:
            pass

    else:
        return render_template("register.html")


@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    
    if request.method == "POST":
        name = request.form.get("name")
        quantity = int(request.form.get("quantity"))
        if 'image' not in request.files:
            return "No image part"
    
        image = request.files['image']

        if image.filename == '':
            return "No selected image"
    
        db.execute('INSERT INTO food_item (food_name, donor_id, image, quantity) VALUES (?, ?,?,?)', (name, session["user_id"],image.read(),quantity))
    return render_template("fooddonate.html")


    
