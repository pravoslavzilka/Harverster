from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from models import User, Coordinator, Hub, Order
import datetime
from database import db_session


coordinator_bp = Blueprint("coordinator_bp", __name__, template_folder="templates")


@coordinator_bp.route("/")
@login_required
def main_page():
    return render_template("coordinator/landing_page.html")


@coordinator_bp.route("/hub-page/<hub_id>/")
@login_required
def hub_page(hub_id):
    hub = Hub.query.filter(Hub.id == hub_id).first()
    if hub.coordinator.email == current_user.email:
        return render_template("coordinator/hub_page.html", hub=hub)
    return redirect(url_for("main_page"))


@coordinator_bp.route("/new-order/<order_id>/", methods=['GET'])
@login_required
def new_order(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    return render_template("coordinator/edit_order.html", order=order)


@coordinator_bp.route("/new-order/<order_id>/", methods=['POST'])
@login_required
def new_order_fun(order_id):
    maxes = request.form["maxes_total"].split(",")
    order = Order.query.filter(Order.id == order_id).first()

    for i, (k, v) in enumerate(order.content.items()):
        order.content[k] = maxes[i]

    order.status = 2
    order.weight = sum([int(x) for x in maxes])
    db_session.commit()

    flash("Order was sent for admin check", "success")
    return redirect(url_for('coordinator_bp.main_page'))


@coordinator_bp.route("/view-order/<order_id>/", methods=['GET'])
@login_required
def view_order(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    return render_template("coordinator/view_order.html", order=order)


@coordinator_bp.route("/update-idp/<hub_id>/", methods=["POST"])
@login_required
def update_idp(hub_id):

    new_idp = request.form["idp-number"]
    hub = Hub.query.filter(Hub.id == hub_id).first()

    if hub.coordinator.email != current_user.email:
        return redirect(url_for("main_page"))

    hub.idp = int(new_idp)
    hub.last_idp_update = datetime.datetime.now()

    db_session.commit()

    flash("IDP was updated", "success")
    return redirect(url_for("coordinator_bp.hub_page", hub_id=hub_id))


@coordinator_bp.route("/sign-in", methods=['GET'])
def sign_in_view():
    if current_user.is_authenticated:
        return redirect(url_for("welcome_page"))

    return render_template("coordinator/sign_in_page.html")


@coordinator_bp.route("/sign-in", methods=['POST'])
def sign_in_fun():
    email = request.form["email"]
    password = request.form["password"]

    coordinator = Coordinator.query.filter(Coordinator.email == email).first()

    if coordinator and coordinator.check_password(password):

        login_user(coordinator)
        flash("Welcome back", "success")
        return redirect(url_for("coordinator_bp.main_page"))

    admin = User.query.filter(User.email == email).first()
    if admin and admin.check_password(password):

        login_user(admin)

        session["permit"] = 1

        flash("Welcome back", "success")
        return redirect(url_for("admin_bp.main_page"))

    flash("Invalid credentials", "danger")
    return render_template("coordinator/sign_in_page.html")


@coordinator_bp.route("/logoff")
@login_required
def sign_off():
    if "permit" in session:
        session.pop("permit")

    logout_user()
    flash("You've been signed off", "success")
    return redirect(url_for("welcome_page"))

