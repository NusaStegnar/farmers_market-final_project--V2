from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, session
from sqlalchemy.sql import text
import sqlalchemy as sa




db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "my super secret key"
db.init_app(app)


class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    #farm_product = db.relationship("Product", backref="farmer", lazy=True)

    def __init__(self, name, location):
        self.name = name
        self.location = location
        

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    #parent_id = db.Column(db.Integer, db.ForeignKey("farmer.id"), nullable=False)

    def __init__(self, item, quantity, price):
        self.item = item
        self.quantity = quantity
        self.price = price


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    farmers = Farmer.query.all()
    return render_template("index.html", farmers=farmers)


@app.route("/new", methods = ["GET", "POST"])
def new():
    if request.method == "POST":
        if not request.form["name"] or not request.form["location"]:
            flash("Please enter all the fields", "error")
        else:
            farmers = Farmer(request.form["name"], request.form["location"])
            db.session.add(farmers)
            db.session.commit()
            flash("Records was successfully added")

    return render_template("new.html")


@app.route("/farm/<id>", methods = ["GET", "POST"])
def farm(id):
    farm = Farmer.query.get(id)
    products = Product.query.all()

    return render_template("farm.html", farm=farm, products=products)


@app.route("/farm/<id>/products", methods = ["GET", "POST"])
def products(id):
    if request.method == "POST":
        if not request.form["product"] or not request.form["quantity"] or not request.form["price"]:
            flash("Please enter all the fields", "error")
        else:
            product = Product(request.form["product"], request.form["quantity"], request.form["price"])
            db.session.add(product)
            db.session.commit()
            flash("Records was successfully added")

    return render_template("products.html", id=id)
    

if __name__ == "__main__":
    app.run(debug=True)
