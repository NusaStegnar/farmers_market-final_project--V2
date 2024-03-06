from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "my super secret key"
db.init_app(app)


class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    product = db.Column(db.String(100), nullable=False)

    def __init__(self, name, location, product):
        self.name = name
        self.location = location
        self.product = product


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    farmers = Farmer.query.all()
    return render_template("index.html", farmers=farmers)


@app.route("/new", methods = ["GET", "POST"])
def new():
    if request.method == "POST":
        if not request.form["name"] or not request.form["location"] or not request.form["product"]:
            flash("Please enter all the fields", "error")
        else:
            farmers = Farmer(request.form["name"], request.form["location"], request.form["product"])
            db.session.add(farmers)
            db.session.commit()
            flash("Records was successfully added")

    return render_template("new.html")


@app.route("/farm/{farmer.id}", methods = ["GET", "POST"])
def farm(id):
    farm = db.session.get(Farmer, id)
    # farm_info = []
    # for fi in farm:
    #     farm_info.append(fi.name)
    #     farm_info.append(fi.location)
    #     farm_info.append(fi.product)
    return render_template("farm.html")
    

if __name__ == "__main__":
    app.run(debug=True)
