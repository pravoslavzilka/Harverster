from flask import Blueprint, render_template, redirect, url_for, request, flash, session


coordinator_bp = Blueprint("coordinator_bp", __name__, template_folder="templates")


@coordinator_bp.route("/")
def main_page():
    return "hello coordinator"
