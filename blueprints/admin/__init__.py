from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps


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
