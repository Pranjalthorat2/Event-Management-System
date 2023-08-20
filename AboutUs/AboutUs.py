from flask import Blueprint, render_template, redirect, url_for, session

AboutUs_bp = Blueprint('au', __name__, template_folder="templates", static_folder="static")

@AboutUs_bp.route("/")
def index():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        #print("NO")
        return redirect(url_for("lg.index"))

    return render_template("AboutUs.html")
