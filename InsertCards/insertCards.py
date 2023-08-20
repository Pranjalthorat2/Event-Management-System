from flask import Blueprint, render_template, redirect, session, url_for

insertCards_bp = Blueprint('ic', __name__, template_folder="templates", static_folder="static")

@insertCards_bp.route("/")
def index():
    print("Insert")
    if not session.get("name"):
        return redirect(url_for("lg.index"))

    return render_template("insertCards.html")
