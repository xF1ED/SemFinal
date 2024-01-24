from flask import Flask, render_template, request, json, jsonify
import os
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, text

app = Flask(__name__)
# Connect to the database
engine = create_engine("mysql+mysqlconnector://root:1234@localhost/flask_final")
# Test the connection
connection = engine.connect()

import routes


@app.route('/')
def index():  # put application's code here
    return render_template('admin/dashboard.html', modul='dashboard')


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('errorPage/pageNotFound.html')


@app.errorhandler(500)
def internalServerError(e):
    return render_template('errorPage/500Page.html')


if __name__ == '__main__':
    app.run()
