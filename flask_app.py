# save this as app.py

from asyncore import read
from flask import Flask, escape, render_template, request
from flask_sqlalchemy import SQLAlchemy
from markupsafe import re
from enum import Enum
import configparser
import os

from sqlalchemy import create_engine
import sqlalchemy

class EnumDevEnv(Enum): #Enivirronement de developpement
    DEV = 1
    PROD = 2


dev_env = EnumDevEnv.DEV;

app = Flask(__name__)
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
config.read(os.path.join(dirname, 'config_db.ini'))

if dev_env== EnumDevEnv.PROD:
    
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username= config["PROD"]["username"],
        password= config["PROD"]["password"],
        hostname= config["PROD"]["hostname"],
        databasename= config["PROD"]["databasename"],
    )
elif dev_env == EnumDevEnv.DEV:
    SQLALCHEMY_DATABASE_URI = "mariadb+mysql+pymysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username= config["DEV"]["username"],
        password= config["DEV"]["password"],
        hostname= config["DEV"]["hostname"],
        databasename= config["DEV"]["databasename"],
    )

"""
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
print(engine.table_names())
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@host/dbname'

# Test if it works
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
print(engine.table_names())
"""


app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#engine = db.create_engine(SQLALCHEMY_DATABASE_URI)


class Reponse(db.Model):
    __tablename__ = "reponses"
    id = db.Column(db.Integer, primary_key=True)
    self_generated_id = db.Column(db.String(80), nullable=False)
    chemin = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<Self generated id: %r>' % self.self_generated_id

@app.route('/')
@app.route('/index')
def index():
    name = request.args.get("name", "World")
    return render_template("index.html",  title='Mobilites IUAR')
    return f'Hello, {escape(name)}!'

@app.route('/success')
def success():
    return "success !"

