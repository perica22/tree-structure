from os import environ
from flask import Flask
from elasticsearch import Elasticsearch


APP = Flask(__name__)
ES = Elasticsearch()
ENVIRONMENT = environ.get("MODE")


from app import routes
