from flask import Blueprint, render_template, redirect, url_for

helloworld_bp2 = Blueprint("myblueprint2", __name__, template_folder="templates")

@helloworld_bp2.route("/")
def index2():
    return ("My world from index 2!!!")

@helloworld_bp2.route("/hello2")
def hello2():
    return redirect(url_for("myblueprint.hello"))

