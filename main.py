from flask import Flask, render_template, redirect, url_for
from blueprints.admin.__init__ import admin_bp
from blueprints.super_admin.__init__ import super_admin_bp
from blueprints.coordinator.__init__ import coordinator_bp
from blueprints.warehouse.__init__ import warehouse_bp
from database import db_session
import os

app = Flask(__name__)

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(super_admin_bp, url_prefix="/super-admin")
app.register_blueprint(coordinator_bp, url_prefix="/coordinator")
app.register_blueprint(warehouse_bp, url_prefix="/warehouse")


app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(16)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["REMEMBER_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = 'Lax'

UsersStatus = []

app.jinja_env.autoescape = True | False


@app.route("/")
def welcome_page():
    return redirect(url_for("coordinator_bp.sign_in_view"))


@app.errorhandler(404)
def error_404(error):
    return render_template("404.html")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
