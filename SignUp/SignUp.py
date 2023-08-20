from flask import Blueprint, render_template, redirect

SignUp_bp = Blueprint('su', __name__, template_folder="templates", static_folder="static")

@SignUp_bp.route("/")
def index():
    print("Signup")
    return render_template("Signup1.html")
