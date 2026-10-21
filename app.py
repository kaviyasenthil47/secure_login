
from flask import Flask, request, session, redirect, url_for
from database import Database
from auth import verify_password
import os
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import render_template_string

app = Flask(__name__)

# Set SECRET_KEY in your environment before running.
app.secret_key = os.environ["SECRET_KEY"]

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # Local HTTP development only
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_REFRESH_EACH_REQUEST=False,
)

csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return """
        <h2>Secure Login System</h2>
        <a href="/login">Login</a>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string("""
            <h2>Login</h2>
            <form method="post">
                <input type="hidden" name="csrf_token"
                   value="{{ csrf_token() }}">

                <input name="user_name"
                   placeholder="Username" required>

                <input name="password" type="password"
                   placeholder="Password" required>

                <button type="submit">Login</button>
            </form>
    """)

    user_name = request.form.get("user_name", "").strip()
    password = request.form.get("password", "")

    db = Database()
    try:
        user = db.get_user_by_username(user_name)

        if user and verify_password(password, user["password_hash"]):
            session.clear()
            session["user_id"] = user["user_id"]
            session.permanent = True
            app.permanent_session_lifetime = __import__(
                "datetime"
            ).timedelta(minutes=30)

            return redirect(url_for("dashboard"))
    finally:
        db.close()

    return "Invalid username or password.", 401


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return "Unauthorized. Please log in.", 401

    return render_template_string("""
        <h2>Welcome to your dashboard!</h2>
        <form method="post" action="/logout">
            <input type="hidden" name="csrf_token"
               value="{{ csrf_token() }}">
            <button type="submit">Logout</button>
        </form>
        """)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False  # Local HTTP testing only
    )
    app.run(debug=True)
