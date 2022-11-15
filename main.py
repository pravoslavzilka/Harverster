from flask import Flask, render_template
from blueprints.admin.__init__ import admin_bp
from blueprints.super_admin.__init__ import super_admin_bp
from blueprints.coordinator.__init__ import coordinator_bp
from blueprints.warehouse.__init__ import warehouse_bp

app = Flask(__name__)

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(super_admin_bp, url_prefix="/super-admin")
app.register_blueprint(coordinator_bp, url_prefix="/coordinator")
app.register_blueprint(warehouse_bp, url_prefix="/warehouse")


@app.route("/")
def welcome_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
