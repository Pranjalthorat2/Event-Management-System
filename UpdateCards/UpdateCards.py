from flask import Blueprint, render_template, redirect, request, session, url_for

UpdateCards_bp = Blueprint('uc', __name__, template_folder="templates", static_folder="static")

@UpdateCards_bp.route("/<uid>")
def index(uid):
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        #print("NO")
        return redirect(url_for("lg.index"))

    return render_template("Update.html", Uid = uid)


