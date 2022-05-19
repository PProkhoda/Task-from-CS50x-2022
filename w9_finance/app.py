import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    hist_info = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares FROM history WHERE hist_id = ? GROUP BY symbol", session["user_id"])

    # list of names
    nam = []
    for e in hist_info:
        e = e['name']
        nam.append(e)

    # list of symbols
    sym = []
    for q in hist_info:
        q = q['symbol']
        sym.append(q)

    # list of sum(shares)
    shar = []
    for w in hist_info:
        w = w['shares']
        shar.append(w)

    user_info = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    last_cash = user_info[0]["cash"]

    # list of prices
    prices = []
    for x in hist_info:
        list = lookup(x["symbol"])
        x = list["price"]
        prices.append(x)
    # for x in sym:
    #     list = lookup(sym[x])
    #     x = list["price"]
    #     prices.append(x)

    # list of total
    total = []
    for i in range(0, len(prices)):
        total.append(prices[i]*shar[i])

    for a in range(len(hist_info)):
        hist_info[a]["price"] = prices[a]
        hist_info[a]["total"] = total[a]

    # for s in range(len(hist_info)):
    #     hist_info[s]["total"] = total[s]

    #cash in wallet
    user_info = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    last_cash = user_info[0]["cash"]

    # total foot
    total_foot = sum(total) + last_cash

    print("HIST_INFO: ", hist_info)

    return render_template("index.html", hist_info=hist_info, last_cash=last_cash, total_foot=total_foot)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares", 403)

        # Query API database for symbol
        symbol = request.form.get("symbol")
        dict = lookup(symbol)
        if not dict:
            return apology("invalid symbol", 400)

        # Ensure Shares is INTEGER
        shares = request.form.get("shares")
        if not shares.isdigit():
            return apology("invalid shares1", 400)

        # Ensure Shares > 0
        if int(shares) < 0:
            return apology("invalid Shares2", 400)

        cash = dict["price"] * int(shares)

        user_info = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        last_cash = user_info[0]["cash"]

        # last_cash_sum = sum(last_cash)
        if cash > last_cash:
            return apology("need cash", 400)

        # datetime
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H.%M.%S")

        # Add row to history for this purchase
        db.execute("INSERT INTO history (hist_id, symbol, shares, price, name, transacted) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], dict["symbol"], shares, dict["price"], dict["name"], date_now)

        # reload cash in users
        new_cash = last_cash - cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        # return flash
        flash("Bought!")

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/hist")
@login_required
def history():
    """Show history of transactions"""

    hist_info = db.execute("SELECT * FROM history WHERE hist_id = ?", session["user_id"])
    return render_template("hist.html", hist_info=hist_info)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Query API database for symbol
        symbol = request.form.get("symbol")
        dict = lookup(symbol)
        if not dict:
            return apology("invalid symbol", 400)

        # return quoted.html + symbol data
        return render_template("quoted.html", dict=dict)

    # User reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("password don't match", 400)

        # Ensure confirmation = password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password don't match", 400)

        # Query database for username
        nam = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # check name in DB
        if len(nam) != 0:
            return apology("username is already taken", 400)

        # add user to db "users"
        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # return flash
        flash("Registered")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # make sure there is enough shares
        hist_info = db.execute("SELECT SUM(shares) AS shares FROM history WHERE hist_id = ? AND symbol = ? GROUP BY symbol",
                               session["user_id"], request.form.get("symbol"))
        last_share = hist_info[0]["shares"]
        if last_share < int(request.form.get("shares")):
            return apology("not enough quantity", 400)

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares", 400)

        # Ensure Shares is INTEGER
        shares = int(request.form.get("shares")) * (-1)
        # if not shares.isdigit():
        #     return apology("invalid shares1", 400)

        # Ensure Shares > 0
        if shares > 0:
            return apology("invalid Shares2", 400)

        # Query API database for symbol
        symbol = request.form.get("symbol")
        dict = lookup(symbol)

        cash = dict["price"] * shares * (-1)

        user_info = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        last_cash = user_info[0]["cash"]

        # datetime
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H.%M.%S")

        # Add row to history for this purchase
        db.execute("INSERT INTO history (hist_id, symbol, shares, price, name, transacted) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], dict["symbol"], shares, dict["price"], dict["name"], date_now)

        # reload cash in users
        new_cash = last_cash + cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        # return flash
        flash("Sell!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        hist_info = db.execute(
            "SELECT symbol, name, SUM(shares) AS shares FROM history WHERE hist_id = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", hist_info=hist_info)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add cash"""
    if request.method == "POST":

        # Ensure add was submitted
        if not request.form.get("cashadd"):
            return apology("must provide Add", 400)

        # Ensure Shares is INTEGER
        cashadd = request.form.get("cashadd")
        if not cashadd.isdigit():
            return apology("invalid add", 400)

        # Ensure Shares > 0
        if int(cashadd) < 0:
            return apology("invalid add2", 400)

        user_info = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        last_cash = user_info[0]["cash"]

        # datetime
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H.%M.%S")

        # Add row to history for this purchase
        db.execute("INSERT INTO cashadd (cash_id, cashadd, transacted) VALUES(?, ?, ?)",
                   session["user_id"], cashadd, date_now)

        # reload cash in users
        new_cash = last_cash + int(cashadd)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        # return flash
        flash("Cash has been deposited!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("add.html")
