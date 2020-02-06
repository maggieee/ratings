"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)
#session(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/login")
def show_login():
    """Show the login form"""

    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login_user():
    """Log the user in if they have valid credentials."""

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, password=password).all()

        if len(user) != 0:
            session[user[0].email] = user[0].password
            flash('You were successfully logged in')
            print(session)

    return render_template("user_details.html", user=user)


@app.route("/logout", methods=['POST'])
def logout_user():
    """Log the user out and remove them from the session."""

    print(session)

    session.clear()
    print(session)

    return redirect("/")


@app.route("user_details")
def show_user_details():
    """Show user details."""

    return render_template("user_details.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET"])
def register_form():
    """Show the register page"""

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """Register a new user with email and password."""

    email = request.form.get('email').strip()
    password = request.form.get('password').strip()

    new_user = User(email=email, password=password)

    if len(User.query.filter_by(email=email).all()) == 0:

        db.session.add(new_user)
        db.session.commit()

        return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
