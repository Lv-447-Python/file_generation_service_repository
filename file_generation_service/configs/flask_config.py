"""Configuration Flask app"""
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow


app = Flask(__name__)
api = Api(app)
marshmallow = Marshmallow(app)
