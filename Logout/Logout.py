from flask import Blueprint, render_template, redirect, session, url_for

Logout_bp = Blueprint('lo', __name__, template_folder="templates", static_folder="static")

@Logout_bp.route("/")
def index():
    session["name"] = None
    return redirect(url_for("lg.index"))