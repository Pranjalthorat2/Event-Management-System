from flask import Blueprint, render_template, redirect, request

Login = Blueprint('lg', __name__, template_folder="templates", static_folder="static")

@Login.route("/")
def index():
    return render_template("Mylogin.html")

