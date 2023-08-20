from flask import Blueprint, render_template, redirect, request, url_for, session

Homepage_bp = Blueprint('hp', __name__, template_folder="templates", static_folder="static")

@Homepage_bp.route("/")
def index():
    from main import session
    if not session.get("name"):
        return redirect(url_for("lg.index"))

    return render_template("Homepage.html", Eusername=session.get("name"))

