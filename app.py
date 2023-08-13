from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask import Flask, render_template, request, redirect, session



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
    try:
        if session["role"]==0 or session["role"]=='0':
            return redirect("/donate")
        elif session["role"]==1 or session["role"]=='1':
            return redirect("/user")
        
    except:
        pass
    return render_template("index.html")


@app.route("/about")
def about():
    try:
        if session["role"]==0 or session["role"]=='0':
            return redirect("/donate")
        elif session["role"]==1 or session["role"]=='1':
            return redirect("/user")
    except:
        pass
    return render_template("about.html")


@app.route("/contact")
def contact():
    try:
        if session["role"]==0 or session["role"]=='0':
            return redirect("/donate")
        elif session["role"]==1 or session["role"]=='1':
            return redirect("/user")
    except:
        pass
    return render_template("contact.html")


@app.route("/profile")
def profile():
    try:
        if session["role"] == 0 or session["role"]=="0":
            rows = db.execute("SELECT food_item.food_name, food_item.quantity, login.points FROM food_item INNER JOIN login ON food_item.donor_id = login.user_id;")
            return render_template("profile.html",values=rows)
        elif session["role"]==1 or session["role"]=='1':
            return redirect("/user")
        
    except:
        pass
    return render_template("login.html")
    

@app.route("/user")
def takefood():
    try:
        rows = db.execute("SELECT * from food_item;")
        return render_template("foodtake.html",values=rows)
    except:
        pass
    return render_template("login.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    try:
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
            rows = db.execute("SELECT * FROM login WHERE email = ?", request.form.get("email"))

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
                return apology("Invalid username or password", 403)

            # Remember which user has logged in
            session["user_id"] = rows[0]["user_id"]
            session["role"] = rows[0]["role"]
            session["fname"] = rows[0]["f_name"]
            session["lname"] = rows[0]["l_name"]
            session["phone"] = rows[0]["phone"]
            session["email"] = rows[0]["email"]

            # Redirect user to home page
            if session["role"]==1 or session["role"]=="1":
                return redirect("/user")
            elif session["role"]==0 or session["role"]=="0":
                return redirect("/donate")
    except:
        pass
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    try:
        # Forget any user_id
        session.clear()
    except:
    # Redirect user to login form
        pass
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def register():
    """Register user"""
    try:
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
                db.execute("INSERT INTO login (f_name,l_name,email,phone,password) VALUES (?, ?,?,?,?)", fname,lname,email,phone, hash)
                return redirect("/")
            except:
                pass

        else:
            return render_template("signup.html")
    except:
        pass
    return render_template("login.html")
    

@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    try:
        point=0
        if session["role"] == 0:
            if request.method == "POST":
                name = request.form.get("name")
                quantity = int(request.form.get("quantity"))
                food_type = request.form.get("type")
                address = request.form.get("address")
                # Insert data into the database
                db.execute("INSERT INTO food_item (food_name,donor_id,quantity,type,address) VALUES (?, ?,?,?,?)", name,session["user_id"],quantity,food_type, address)

                point+=quantity*50
                db.execute("UPDATE login SET points = ? WHERE user_id = ?", point,session["user_id"])

            return render_template("donate.html")
    except:
        pass

    return render_template('index.html')
