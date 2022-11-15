from flask import Blueprint, render_template, redirect, url_for, request, flash, session


admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


@admin_bp.route("/")
def main_page():
    return "hello admin"
