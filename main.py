from flask import Flask, render_template
from blueprints.admin.__init__ import admin_bp
from blueprints.super_admin.__init__ import super_admin_bp
from blueprints.coordinator.__init__ import coordinator_bp
from blueprints.warehouse.__init__ import warehouse_bp
from flask_login import LoginManager
from database import db_session
from models import User, Coordinator
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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ""
login_manager.login_message = "Sign in"
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"


@app.route("/")
def welcome_page():
    return render_template("index.html")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    return Coordinator.query.filter(Coordinator.id == user_id).first() or User.query.filter(User.id == user_id).first()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
