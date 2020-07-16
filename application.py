import os

from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
import requests, json
import ast


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def apology(message):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        """
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", bottom=escape(message))

def loggedin_apology(message):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        """
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("loggedin_apology.html", bottom=escape(message))

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted

        username=request.form.get("username")
        password=request.form.get("password")

        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("Must confirm password")

        # Ensure password confirmation matches password
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("Password confirmation must match password")

        # Check username does not already exist and if not add username to database
        try:
            result = db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password":password})
        except:
            return apology("That username has already been taken")


        # Automatically login user once registered
        session["user_id"] = db.execute("SELECT id FROM users", {'id': id}).fetchone()

        # Redirect user to home page
        return redirect("/search")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

    return apology("Please register")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", {'username': username}).fetchall()


        # Ensure username exists and password is correct
        if len(rows) != 1 or not password: 
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/search")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    
    session.clear()

    return render_template("goodbye.html")


@app.route("/search", methods=["GET"])
@login_required
def search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
@login_required
def search_for():
     
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get data from search form
        search = request.form.get("search")
        search = "%" + search + "%"


        # If nothing entered in form
        if not search:
            return loggedin_apology("Please enter a search term")

        else:
            # Query database
            results = db.execute("SELECT title, author, isbn FROM books WHERE \
                                    isbn ILIKE :ss OR title ILIKE :ss OR author ILIKE :ss \
                                        ORDER BY title ASC", {'ss': search}).fetchall()

            if not results:
                return loggedin_apology("Sorry, no results match your search")
            else:
                return render_template("results.html", results=results)


@app.route("/book/<isbn>", methods=['GET', 'POST'])
@login_required
def book(isbn):

    if request.method == "GET":

        book_info = db.execute("SELECT title, author, year, isbn, book_id FROM books WHERE isbn = :isbn", {'isbn': isbn}).fetchone()
        book_id = book_info[4]
        isbn = book_info[3]
        reviews = db.execute("SELECT review FROM reviews WHERE book_id = :book_id", {'book_id': book_id}).fetchall()
        reviews=[i[0] for i in reviews]

        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "a6IjM6Xf4F3H1WRCrWcEQ", "isbns":isbn })
        data = res.json()

        ar = data['books'][0]['average_rating']
        nr = data['books'][0]['work_ratings_count']

        return render_template("book.html", book_info=book_info, reviews=reviews, ar=ar, nr=nr)

    if request.method == "POST":

        # Get form information.
        book_id = request.form.get("book_id")
        rating = request.form.get("rating")
        review = request.form.get("book_review")

        # Get user_id
        user_id=session["user_id"]

        # Make sure user has not left previous review for book.
        if db.execute("SELECT book_id, user_id FROM reviews WHERE book_id = :book_id AND user_id = :user_id", {"book_id": book_id, "user_id": user_id}).rowcount == 0:
            db.execute("INSERT INTO reviews (user_id, book_id, review, rating) VALUES (:user_id, :book_id, :review, :rating)",
                {"user_id": user_id, "book_id": book_id,  "review": review, "rating": rating})
            db.commit()
            return loggedin_apology("Thank you for your review!")
        else:
            return loggedin_apology("You have already submitted a review for this book")

@app.route("/api/<isbn>", methods=['GET'])
def api_call(isbn):

    try:

        books = db.execute("SELECT (title, author, year, isbn, COUNT(reviews.id), AVG(rating)) FROM books INNER JOIN reviews ON reviews.book_id = books.book_id WHERE  isbn = :isbn GROUP BY title, author, year, isbn", {"isbn": isbn}).fetchone()
        books = books[0]
        books = books.strip('()')
        books = books.split(",")
        books = [i.replace('"', '') for i in books]
        books = [i.replace('"', '') for i in books]

        
        # if not books:
        #     return jsonify({"Error": "Sorry, we don't have that book"}), 404
        

        fields = ("title", "author", "year", "isbn", "review_count", "average_score")
        result = zip(fields, books)
        result = dict(result)
        result['year'] = int(result['year'])
        result['isbn'] = int(result['isbn'])
        result['review_count'] = int(result['review_count'])
        result['average_score'] = float(result['average_score'])
    
    except:
        return jsonify({"Error": "Sorry, we don't have that book"}), 404



    return result

