from flask import Blueprint, render_template, redirect, url_for, request, flash, session


warehouse_bp = Blueprint("warehouse_bp", __name__, template_folder="templates")


@warehouse_bp.route("/")
def main_page():
    return "hello warehouse"
