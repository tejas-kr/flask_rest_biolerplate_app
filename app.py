from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# INIT APP
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# INIT SCHEMA
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route("/product", methods=["POST"])
def add_product():
    try:
        name = request.json["name"]
        description = request.json["description"]
        price = request.json["price"]
        qty = request.json["qty"]

        new_product = Product(name, description, price, qty)

        db.session.add(new_product)
        db.session.commit()

        return product_schema.jsonify(new_product)
    except Exception as e:
        print(e)
        return jsonify({"message": "error"})

# GET ALL Products
@app.route("/all_products", methods=["GET"])
def get_all_products():
    try:
        all_products = Product.query.order_by(db.desc(Product.id)).all()
        return products_schema.jsonify(all_products)
    except:
        return jsonify({"message": "error"})

# Get Single product
@app.route("/product/<int:id>", methods=["GET"])
def get_single_product(id):
    try:
        product = Product.query.filter_by(id=id).first()
        return product_schema.jsonify(product)
    except:
        return jsonify({"message": "error"})

# Updating a product 
@app.route("/product/<int:id>", methods=["PUT"])
def update_product(id):
    try:
        product = Product.query.filter_by(id=id).first()
        
        name = request.json["name"]
        description = request.json["description"]
        price = request.json["price"]
        qty = request.json["qty"]

        product.name = name
        product.description = description
        product.price = price
        product.qty = qty

        db.session.commit()

        return product_schema.jsonify(product)
    except:
        return jsonify({"message": "error"})

@app.route("/product/<int:id>", methods=["DELETE"])
def delete_prodeuct(id):
    try:
        product = Product.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()

        return product_schema.jsonify(product)
    except:
        return jsonify({"message": "error"})

# front page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)