from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models import User, Coordinator, Hub, Order, Idp
import datetime
from database import db_session
from functools import wraps


coordinator_bp = Blueprint("coordinator_bp", __name__, template_folder="templates")


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "roles" in session:
            return func(*args, **kwargs)
        return render_template("404.html")
    return inner


@coordinator_bp.route("/")
@login_required
def main_page():
    coordinator = Coordinator.query.filter(Coordinator.email == session["user"]).first()
    return render_template("coordinator/landing_page.html", coordinator=coordinator)


@coordinator_bp.route("/hub-page/<hub_id>/")
@login_required
def hub_page(hub_id):
    hub = Hub.query.filter(Hub.id == hub_id).first()
    if hub.coordinator.email == session["user"]:
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

    if hub.coordinator.email != session["user"]:
        return redirect(url_for("main_page"))

    hub.idp = int(new_idp)
    hub.last_idp_update = datetime.datetime.now()

    new_idp_record = Idp()
    new_idp_record.value = new_idp
    new_idp_record.hub = hub
    new_idp_record.date = datetime.datetime.now()

    db_session.add(new_idp_record)

    db_session.commit()

    flash("IDP was updated", "success")
    return redirect(url_for("coordinator_bp.hub_page", hub_id=hub_id))


@coordinator_bp.route("/sign-in", methods=['GET'])
def sign_in_view():
    if "user" in session:
        if "roles" in session:
            if session['roles'] == 'order':
                print(session["roles"])
                return redirect(url_for("coordinator_bp.main_page"))

        return redirect(url_for("admin_bp.main_page"))
    return render_template("coordinator/sign_in_page.html")


@coordinator_bp.route("/sign-in", methods=['POST'])
def sign_in_fun():
    email = request.form["email"]
    password = request.form["password"]

    coordinator = Coordinator.query.filter(Coordinator.email == email).first()

    if coordinator and coordinator.check_password(password):

        session["user"] = coordinator.email
        session["roles"] = "order"
        flash("Welcome back", "success")
        return redirect(url_for("coordinator_bp.main_page"))

    admin = User.query.filter(User.email == email).first()
    if admin and admin.check_password(password):

        session["user"] = admin.email
        session["roles"] = "admin"
        flash("Welcome back", "success")
        return redirect(url_for("admin_bp.main_page"))

    flash("Invalid credentials", "danger")
    return render_template("coordinator/sign_in_page.html")


@coordinator_bp.route("/logoff")
@login_required
def sign_off():
    if "roles" in session:
        session.pop("roles")

    session.pop("user")
    flash("You've been signed off", "success")
    return redirect(url_for("welcome_page"))

