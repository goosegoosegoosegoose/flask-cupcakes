"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "whatnow"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/api/cupcakes', methods=['GET', 'POST'])
def get_create_cupcakes():
    """post json of new cupcake, get json of all cupcakes"""

    if request.method == 'POST':
        new_cupcake = Cupcake(
            flavor=request.json["flavor"],
            size=request.json["size"],
            rating=request.json["rating"],
            image=request.json["image"]
            )
        db.session.add(new_cupcake)
        db.session.commit()

        return (jsonify(cupcake=new_cupcake.serialize()), 201)
    else:
        all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_cupcake(cupcake_id):
    """patch json of single cupcake, delete cupcake json, get json of single cupcake"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if request.method == 'PATCH':
        cupcake.flavor=request.json.get('flavor', cupcake.flavor),
        cupcake.size=request.json.get('size', cupcake.size),
        cupcake.rating=request.json.get('rating', cupcake.rating),
        cupcake.image=request.json.get('image', cupcake.image)
        db.session.commit()

        return jsonify(cupcake=cupcake.serialize())
    
    if request.method == 'DELETE':
        db.session.delete(cupcake)
        db.session.commit()
        
        return jsonify(msg='deleted')

    else:
        return jsonify(cupcake=cupcake.serialize())

@app.route('/')
def homepage():
    """homepage?"""
    cupcakes = Cupcake.query.all()

    return render_template("homepage.html", cupcakes=cupcakes)
