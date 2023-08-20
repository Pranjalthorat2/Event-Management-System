from flask import Blueprint, render_template, redirect, request, session, url_for

ContactUs_bp = Blueprint('cu', __name__, template_folder="templates", static_folder="static")

@ContactUs_bp.route("/")
def index():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        #print("NO")
        return redirect(url_for("lg.index"))

    return render_template("Contact.html")


