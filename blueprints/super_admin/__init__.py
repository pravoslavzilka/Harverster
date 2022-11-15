from flask import Blueprint, render_template, redirect, url_for, request, flash, session


super_admin_bp = Blueprint("super_admin_bp", __name__, template_folder="templates")


@super_admin_bp.route("/")
def main_page():
    return "hello super admin"
