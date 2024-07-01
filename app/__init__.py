import requests
from flask import Flask

from flask_restful import Api
from flask_cors import CORS

# creating the flask app
app = Flask(__name__)

# creating an API object
api = Api(app)

CORS(app)




from app import views