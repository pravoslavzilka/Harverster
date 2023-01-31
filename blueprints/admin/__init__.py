from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from database import db_session
from functools import wraps
from models import *
from sqlalchemy import desc
import datetime


admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


def check_admin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "permit" in session:
            if session["permit"] == 1:
                return func(*args, **kwargs)
        return render_template("404.html")
    return inner


@admin_bp.route("/")
@check_admin
def main_page():
    to_check_orders = Order.query.filter(Order.status == 2).all()
    to_ship_orders = Order.query.filter(Order.status == 4).all()
    pending_orders = len(Order.query.filter(Order.status == 3).all())

    return render_template("admin/main_dashboard.html", to_check_orders=to_check_orders, to_ship_orders=to_ship_orders, pending_orders=pending_orders)


@admin_bp.route("/new-order", methods=['GET'])
@check_admin
def new_order_view():
    items = Item.query.all()
    return render_template("admin/new_order.html", items=items)


@admin_bp.route("/new-order", methods=['POST'])
@check_admin
def new_order_fun():
    items = request.form["items_total"].split(",")
    maxes = request.form["maxes_total"].split(",")

    order_content = {items[i]: maxes[i] for i in range(len(items))}
    print(order_content)
    hubs = Hub.query.all()
    for hub in hubs:
        new_order = Order()
        new_order.hub = hub
        new_order.status = 1
        new_order.content = order_content
        new_order.time = datetime.datetime.now()
        db_session.add(new_order)

    db_session.commit()

    flash("New order was placed", "success")
    return redirect(url_for('admin_bp.main_page'))


@admin_bp.route("/edit-order/<order_id>/", methods=['GET'])
@check_admin
def edit_order_view(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    return render_template("admin/edit_order.html", order=order)


@admin_bp.route("/new-order/<order_id>/", methods=['POST'])
@check_admin
def edit_order_fun(order_id):
    maxes = request.form["maxes_total"].split(",")
    order = Order.query.filter(Order.id == order_id).first()

    items_content = order.content

    for i, (k, v) in enumerate(order.content.items()):
        items_content[k] = str(maxes[i])

    order.status = 3
    del order.content
    order.content = items_content
    order.weight = sum([int(x) for x in maxes])
    db_session.commit()

    flash("Order was sent for admin check", "success")
    return redirect(url_for('admin_bp.main_page'))


@admin_bp.route("/delivery/")
@check_admin
def delivery_page():
    orders = Order.query.filter(Order.status == 3).all()
    return render_template("admin/delivery_page.html", orders=orders)


@admin_bp.route("/hubs")
@check_admin
def hubs_page():

    hubs = Hub.query.all()
    return render_template("admin/hubs_management.html", hubs=hubs)


@admin_bp.route("/hub/<int:hub_id>/")
@check_admin
def hub_page(hub_id):

    hub = Hub.query.filter(Hub.id == hub_id).first()
    idp_history = Idp.query.filter(Idp.hub == hub).order_by(desc(Idp.id)).limit(10).all()
    idp_history = idp_history[::-1]
    idp_values = [record.value for record in idp_history]
    idp_dates = [record.date.strftime("%d %B") for record in idp_history]
    return render_template("admin/hub_page.html", hub=hub, idp_values=idp_values, idp_dates=idp_dates)


@admin_bp.route("/hub/idp/<int:hub_id>/", methods=['POST'])
@check_admin
def hub_change_idp(hub_id):
    new_idp = request.form["idp-number"]
    hub = Hub.query.filter(Hub.id == hub_id).first()
    hub.idp = new_idp

    new_idp_record = Idp()
    new_idp_record.value = new_idp
    new_idp_record.hub = hub
    new_idp_record.date = datetime.datetime.now()

    db_session.add(new_idp_record)
    db_session.commit()

    flash("Current IDP was updated", "success")
    return redirect(url_for("admin_bp.hub_page", hub_id=hub.id))


@admin_bp.route("/hub/info/<int:hub_id>/", methods=['POST'])
@check_admin
def hub_change_info(hub_id):

    hub = Hub.query.filter(Hub.id == hub_id).first()

    if hub:
        hub.name = request.form["name"]
        hub.institution = request.form["institution"]
        hub.address = request.form["address"]
        hub.phone = request.form["phone"]
        hub.contact_name = request.form["contact_name"]

        db_session.commit()
        flash("Hub's info was updated", "success")
        return redirect(url_for("admin_bp.hub_page", hub_id=hub.id))

    flash("Invalid ID", "danger")
    return redirect(url_for("admin_bp.hubs_page"))


@admin_bp.route("/hub/new/", methods=['POST'])
@check_admin
def hub_change_new():

    hub = Hub(request.form["name"])

    hub.institution = request.form["institution"]
    hub.address = request.form["address"]
    hub.phone = request.form["phone"]
    hub.contact_name = request.form["contact_name"]

    db_session.add(hub)
    db_session.commit()

    flash(f"Hub {hub.name} was created", "success")
    return redirect(url_for("admin_bp.hubs_page"))


@admin_bp.route("/coordinators/")
@check_admin
def coordinators_page():
    coordinators = Coordinator.query.all()

    return render_template("admin/users_management.html", coordinators=coordinators)


@admin_bp.route("/coordinator/new/", methods=['POST'])
@check_admin
def coordinator_new():

    email_check = Coordinator.query.filter(Coordinator.email == request.form["email"]).first()
    if email_check:
        flash("Email already in use ", "danger")
        return redirect(url_for("admin_bp.coordinators_page"))

    new_coor = Coordinator(request.form["name"], request.form["email"], request.form["phone"])
    new_coor.set_password(request.form["password"])

    db_session.add(new_coor)
    db_session.commit()

    flash("New user was added", "success")
    return redirect(url_for("admin_bp.coordinators_page"))




