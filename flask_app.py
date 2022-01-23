# save this as app.py
from flask import Flask, escape, render_template, request
from markupsafe import re

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    name = request.args.get("name", "World")
    #return render_template("index.html",  title='Mobilites IUAR')
    return f'Hello, {escape(name)}!'
    