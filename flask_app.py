# save this as app.py

from asyncore import read
from flask import Flask, escape, redirect, render_template, request, url_for
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


app = Flask(__name__)
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
config.read(os.path.join(dirname, 'config_db.ini'))

dev_env =  EnumDevEnv(int(config["ENVIRONMENT"]["dev"]))

if dev_env== EnumDevEnv.PROD:
    
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username= config["PROD"]["username"],
        password= config["PROD"]["password"],
        hostname= config["PROD"]["hostname"],
        databasename= config["PROD"]["databasename"],
    )
elif dev_env == EnumDevEnv.DEV:
    SQLALCHEMY_DATABASE_URI = "mariadb+mariadbconnector://{username}:{password}@{hostname}/{databasename}".format(
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
    chemin = db.Column(db.String(4096), nullable=False)

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

@app.route('/traitement', methods=["POST"])
def traitement():


    reponse = Reponse(self_generated_id=request.form["self_id"], chemin=request.form["chemin"])
    db.session.add(reponse)
    db.session.commit()
    return redirect(url_for('success'))
    return request.form


