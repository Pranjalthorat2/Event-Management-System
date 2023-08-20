from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import pymysql
pymysql.install_as_MySQLdb()

from Login.Login import Login
from HomePage.HomePage import Homepage_bp
from InsertCards.insertCards import insertCards_bp
from UpdateCards.UpdateCards import UpdateCards_bp
from ContactUs.ContactUs import ContactUs_bp
from AboutUs.AboutUs import AboutUs_bp
from SignUp.SignUp import SignUp_bp
from Logout.Logout import Logout_bp

app = Flask(__name__)

app.register_blueprint(Login, url_prefix="/login")
app.register_blueprint(Homepage_bp, url_prefix="/homepage")
app.register_blueprint(insertCards_bp, url_prefix="/mycards")
app.register_blueprint(UpdateCards_bp, url_prefix="/updatecards")
app.register_blueprint(ContactUs_bp, url_prefix="/contact")
app.register_blueprint(AboutUs_bp, url_prefix="/aboutus")
app.register_blueprint(SignUp_bp, url_prefix="/signup")
app.register_blueprint(Logout_bp, url_prefix="/logout")


app.config['SECRET_KEY'] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:1234@127.0.0.1:3306/fsd"
app.config['SQLALCHEMY_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

class LoginUsers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Eusername = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, unique=False)

class MyEvents(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Eventname = db.Column(db.String(50), nullable=False, unique=False)
    location = db.Column(db.String(30), nullable=False, unique=False)
    date = db.Column(db.String(10), nullable=False, unique=False)
    time = db.Column(db.String(10), nullable=False, unique=False)
    Eusername = db.Column(db.String(30), nullable=False, unique=False)


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

@app.route("/updateLogin", methods = ["POST"])
def updateLogin():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        entry = LoginUsers(Eusername=username, password=password)
        db.session.add(entry)
        db.session.commit()

    except Exception as e:
        return render_template("/Error.html")

    return redirect("/login")

@app.route("/createCard", methods = ["POST"])
def createcard():
    db.create_all()
    Ename = request.form.get("Ename")
    location = request.form.get("location")
    date = request.form.get("date")
    time = request.form.get("time")
    entry = MyEvents(Eventname=Ename, location=location, date=date, time=time, Eusername=session.get("name"))
    db.session.add(entry)
    db.session.commit()
    print("create cards")

    return redirect("/readCards")


@app.route("/updateCards/<Uid>", methods = ["POST"])
def updateCard(Uid):
    #session.query(MyEvents).filter(MyEvents.username == request.form.get("Ename")).update({"Eventname": "Updated"})
    MyEvents.query.filter(MyEvents.id == Uid).update({"Eventname":request.form.get("Ename")})
    MyEvents.query.filter(MyEvents.id == Uid).update({"location": request.form.get("location")})
    MyEvents.query.filter(MyEvents.id == Uid).update({"time": request.form.get("time")})
    MyEvents.query.filter(MyEvents.id == Uid).update({"date": request.form.get("date")})

    db.session.commit()
    print("Updated", Uid)
    return redirect("/readCards")


@app.route("/deleteEvent/<int:eventId>")
def deletevent(eventId):

    MyEvents.query.filter(MyEvents.id==eventId).delete()
    db.session.commit()

    return redirect("/readCards")


@app.route("/readCards")
def readCards():

    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    items = []
    eve = MyEvents.query.filter(MyEvents.Eusername == session.get("name"))

    for i in eve:
        print(i.Eventname)
        items.append((i.id, i.Eventname, i.location, i.date, i.time))

    images = {"Birthday": "https://as2.ftcdn.net/v2/jpg/05/74/31/67/1000_F_574316772_7VHyWnkUm2o9Yg00ORWSSBzwaWaViHk4.jpg",
        "Wedding": "https://img.freepik.com/free-photo/hands-indian-bride-groom-intertwined-together-making-authentic-wedding-ritual_8353-10047.jpg?w=740&t=st=1690654371~exp=1690654971~hmac=25c6cc7d4d1e783190f8a64f4b8079c96e41f86f278b2ac805dd77212da406d7",
        "Haldi": "https://img.freepik.com/premium-photo/onam-photo_948735-4235.jpg?w=2000",
        "Exhibition": "https://as2.ftcdn.net/v2/jpg/05/36/13/99/1000_F_536139994_HfGEQTsriJV5jbObmk93KJtN3HRacPww.jpg",
        "Food Festival": "https://as1.ftcdn.net/v2/jpg/06/13/14/62/1000_F_613146281_2mf1yjXosXaMxMP2ODMVYXE4ECQjzbXY.jpg"}

    return render_template("EventPage.html", items=items, image=images)



@app.route("/Verify",  methods = ["POST"])
def verify():
    valid = LoginUsers.query.filter(LoginUsers.Eusername == request.form.get("username"), LoginUsers.password == request.form.get("password")).first()
    if valid != None:
        session["name"] = request.form.get("username")
        return redirect("/homepage") # bp

    return redirect("/login") #bp


@app.route("/")
def index():
    db.create_all()
    return redirect("/login") # bp


if __name__ == "__main__":
    app.run(debug=True)
