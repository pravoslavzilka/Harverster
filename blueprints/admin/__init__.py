from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from database import db_session
from functools import wraps
from models import *
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
    return render_template("admin/main_dashboard.html")


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
